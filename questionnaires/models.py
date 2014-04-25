from django.db import models
from django.db import connection
from django.conf import settings

class Questionnaire(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255) # Not enforced on Model/Database level, only affects HTML
    
    def __unicode__(self):
        return self.name
    
    def is_valid(self):
        pages = list(self.page_set.all())
        if not pages: return False
        for p in pages:
            questions = list(p.question_set.all())
            if not questions: return False
            for q in questions:
                if not q.alternative_set.exists(): return False
        if not self.outcome_set.exists(): return False
        return True

class Page(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    title = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.title

class Question(models.Model):
    description = models.TextField(max_length=255) # Not enforced on Model/Database level, only affects HTML
    page = models.ForeignKey(Page)
    
    def __unicode__(self):
        return self.description

class Alternative(models.Model):
    question = models.ForeignKey(Question)
    description = models.CharField(max_length=255)
    score = models.SmallIntegerField()
    
    # Non db
    selected = False
    
    def __unicode__(self):
        return self.description

class Outcome(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    title = models.CharField(max_length=30)
    minimum_score = models.SmallIntegerField(default=-32768)
    message = models.TextField(max_length=255) # Not enforced on Model/Database level, only affects HTML
    
    def __unicode__(self):
        return self.title

# Non database classes
from forms import PageForm

# This class represents an 'open' questionnaire, one that a user has started answering.
# It is instanciated based on session data.

class OpenQuestionnaire():
    def __init__(self, request, questionnaire_id):
        # The request where we store session data about the questionnaire being answered
        self.request = request
        # A Questionnaire instance of the current open questionnaire
        self.questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        # The current page of the questionnaire being answered
        self.page = None
        # Validity of the questionnaire: Invalid if it doesn't have pages, questions or alternatives
        self.invalid_questionnaire = not self.questionnaire.is_valid()
        if self.invalid_questionnaire: return None
        # A list of the open questionnaires (in case the user is answering multiple ones at the same time)
        open_questionnaires = request.session.get("open_questionnaires", {})
        # Current questionnaire data taken from request
        current_questionnaire = open_questionnaires.get(str(questionnaire_id), None)
        # If the user is starting test right now
        if not current_questionnaire:
            # Start from the first page
            self.page = self.questionnaire.page_set.first()
            # Else, set initial information
            current_questionnaire = {
                                        "answers": {},
                                        "page": self.page.id,
                                        "page_valid": False,
                                        "done": False
                                     }
        else:
            # If the user has already started answering the questionnaire, get current page
            # from session data
            self.page = self.questionnaire.page_set.get(id=current_questionnaire["page"])
        # Set status information about questionnaire being answered
        self.info = current_questionnaire
        # And save it to the session
        open_questionnaires[str(questionnaire_id)] = current_questionnaire
        request.session["open_questionnaires"] = open_questionnaires
        
        if request.method == 'POST':
            # If user has posted data, use it to create a bound form 
            self.page_form = PageForm(self.page, request.POST)
            self.info["answers"][str(self.page.id)] = request.POST
        else:
            # Else create unbound form to be displayed and answered
            self.page_form = PageForm(self.page)
    
    # Goes to next page and returns True if there is a next page
    # Sets the questionnaire as done and returns False if there isn't  
    def go_to_next_page(self):
        previous_page = self.page
        try:
            # The next page is the first one in the page_set with an id > the current
            self.page = self.questionnaire.page_set.filter(id__gt=previous_page.id).first()
            self.info["page"] = self.page.id
            # Update page form with the form for the next page
            self.page_form = PageForm(self.page)
        except:
            # If there is no such page,the questionnaire is done
            self.page = None
            self.info["done"] = True
            return False
        return True
    
    def is_valid(self):
        return self.page_form.is_valid()
    
    # Finish open questionnaire and returns outcome
    def outcome(self):
        # Get list of open questionnaires being answered by a user
        open_questionnaires = self.request.session.get("open_questionnaires", None)
        # If it is found, remove the current questionnaire from it
        if open_questionnaires: open_questionnaires.pop(str(self.questionnaire.id))
        
        # Loop through the selected answers to determine the score
        score = 0
        # Array with better alternatives. Each alternative is in a different page
        better_alternatives = []
        # Array with worse alternatives. Each alternative is in a different page
        worse_alternatives = []
        
        for page in self.questionnaire.page_set.all():
            better_question = None
            worse_question = None
            for question in page.question_set.all():
                if not better_question: better_question = question
                if not worse_question: worse_question = question
                # Get id of the selected alternative for the question
                selected_id = self.info["answers"][str(page.id)]["question_"+str(question.id)+"_answer"]
                alternatives = question.alternative_set.all()
                # Get the selected alternative object 
                selected = alternatives.get(id=selected_id) 
                # Remove selected question alternative from list
                alternatives = list(alternatives)
                alternatives.remove(selected)
                # and set it as the selected one
                selected.selected = True
                # add score gained from this answer
                score += selected.score
                # The difference in points if the user selected the alternative he already selected is zero
                selected.difference = 0
                # If the user could change the answer to this question,
                # 'better_alternative' would give him the most points 
                better_alternative = selected
                # If the user could change the answer to this question,
                # 'worse_alternative' would take the most points from him 
                worse_alternative = selected
                # For each alternative, compare with the selected one and see if it's a big positive or negative difference 
                for alternative in alternatives:
                    alternative.difference = alternative.score - selected.score
                    if alternative.difference > better_alternative.difference:
                        better_alternative = alternative
                    if alternative.difference < worse_alternative.difference:
                        worse_alternative = alternative
                
                question.better_alternative = better_alternative
                question.worse_alternative = worse_alternative
                
                if question.better_alternative.difference > better_question.better_alternative.difference:
                    better_question = question
                if question.worse_alternative < worse_question.worse_alternative.difference:
                    worse_question = question
                
            better_alternatives.append(better_question.better_alternative)
            worse_alternatives.append(worse_question.worse_alternative)
        
        result = None
        better_score = score
        worse_score = score
        
        # Determine the outcome of the response to the questionnaire
        # For each possible outcome (from best to worst)
        result = None
        outcomes = list(self.questionnaire.outcome_set.order_by('-minimum_score'))
        i = 0
        for outcome in outcomes:
            if score >= outcome.minimum_score:
                # This is the outcome the user got
                outcome.total_score = score
                # The score necessary to get a worse outcome
                worse_score = outcome.minimum_score # -1
                result = outcome
                try: worse_outcome = outcomes[i+1]
                except: worse_outcome = outcome
                break
            # The score necessary to get a better outcome
            better_score = outcome.minimum_score
            better_outcome = outcome
            i+=1
        if not result: return None
        if score == better_score:
            # If no score could result in a higher outcome, look for a worse solution
            result.alternative_outcome = worse_outcome
            result.alternative_solution = self.calculate_alternative_solution(result, worse_score, worse_alternatives, -1)
        else:
            # Else, look for a better solution
            result.alternative_outcome = better_outcome
            result.alternative_solution = self.calculate_alternative_solution(result, better_score, better_alternatives, 1)
        
        return result
        #outcomes = Outcome.objects. 
    
    def calculate_alternative_solution(self, outcome, other_score, other_alternatives, better):
        # If 'better' is 1, look for a better solution. If it's -1, look for a worse solution. 
        # The alternatives in 'other_alternatives' are in
        # the order that they appear in the questionnaire
        
        # Get the indices of 'other_alternatives'
        indices = range(len(other_alternatives))
        # Order them by 'difference' desc: Now the first index will take to the alternative 
        # with that gives the most points in the original 'other_alternatives' list
        # or that takes the most points
        ordered_indices = list(reversed(sorted(indices, key=lambda i: other_alternatives[i].difference)))
        would_have_got = outcome.total_score
        other_indices = []
        i = 0
        # Loop through the questions with most potential to change the score
        # And change the selected answer (for better or worse) until the score
        # crosses the threshold to another outcome
        while would_have_got*better < other_score*better:
            other_index = ordered_indices[i]
            other_indices.append(other_index)
            would_have_got += other_alternatives[other_index].difference
            i+=1
        outcome.would_have_got = would_have_got
        other_indices.sort()
        # Populate array with the questions that had to be changed,
        # in the order they appear in the questionnaire
        other_solution = []
        for i in other_indices:
            other_solution.append(other_alternatives[i])
        return other_solution