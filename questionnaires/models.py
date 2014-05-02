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
    description = models.TextField(max_length=255)
    page = models.ForeignKey(Page)
    
    def __unicode__(self):
        return self.description
    
    def selected_alternatives(self):
        return [a for a in self.alternatives if a.selected ]
    
    def alternatives_left_selected(self):
        return [a for a in self.alternatives if (a.selected and not a.removed) or (a.post_selected)]
    
    def post_selected_alternatives(self):
        return [a for a in self.alternatives if a.post_selected]
    
    def removed_alternatives(self):
        return [a for a in self.alternatives if a.removed]

class Alternative(models.Model):
    question = models.ForeignKey(Question)
    description = models.CharField(max_length=255)
    score = models.SmallIntegerField()
    
    # Non db
    selected = False
    removed = False
    post_selected = False
    
    def formatted_score(self):
        return "%+d" % self.score
    
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

class OpenQuestionnaire(object):
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
            self.info["answers"][str(self.page.id)] = dict(request.POST)
        else:
            # Else create unbound form to be displayed and answered
            self.page_form = PageForm(self.page)
    
    def go_to_next_page(self):
        """
        Goes to next page and returns True if there is a next page.
        Sets the questionnaire as done and returns False if there isn't.
        """
        previous_page = self.page
        # The next page is the first one in the page_set with an id > the current
        self.page = self.questionnaire.page_set.filter(id__gt=previous_page.id).first()
        if self.page:
            self.info["page"] = self.page.id
            # Update page form with the form for the next page
            self.page_form = PageForm(self.page)
        else:
            # If there is no such page,the questionnaire is done
            self.page = None
            self.info["done"] = True
            return False
        return True
    
    def is_valid(self):
        return self.page_form.is_valid()
    
    def calculate_outcome(self):
        """
        Finish open questionnaire and returns outcome
        """
        # Get list of open questionnaires being answered by a user
        open_questionnaires = self.request.session.get("open_questionnaires", None)
        # If it is found, remove the current questionnaire from it
        if open_questionnaires: open_questionnaires.pop(str(self.questionnaire.id))
        
        # Loop through the selected answers to determine the score
        # and save all children objects in the questionnaire
        self.questionnaire.score = 0
        self.questionnaire.pages = list(self.questionnaire.page_set.all())
        # A list with the questions that have the most potential to GIVE points if changed, one per page 
        most_profitable_questions = []
        # A list with the questions that have the most potential to TAKE points if changed, one per page 
        most_prejudicial_questions = []
        for page in self.questionnaire.pages:
            page.score = 0
            page.questions = list(page.question_set.all())
            page.most_profitable_question = page.questions[0]
            page.most_prejudicial_question = page.questions[0]
            for question in page.questions:
                # Get ids of the selected alternatives for the question
                selected_ids = self.info["answers"][str(page.id)]["question_"+str(question.id)+"_answer"]
                selected_ids = [ int(id) for id in selected_ids ]
                # Get all alternatives
                question.alternatives = list(question.alternative_set.all())
                # Calculate max and min punctuation possible for a question
                question.score = 0
                question.max_score = 0
                question.min_score = 0
                question.best_alternative = question.alternatives[0]
                question.worst_alternative = question.alternatives[0]
                for alt in question.alternatives:
                    if alt.score > question.best_alternative:
                        question.best_alternative = alt
                    if alt.score < question.worst_alternative:
                        question.worst_alternative = alt
                    
                    if alt.score > 0:
                        question.max_score += alt.score
                    elif alt.score < 0:
                        question.min_score += alt.score
                    if alt.id in selected_ids:
                        # Set selected alternatives as selected
                        alt.selected = True
                        #question.selected.append(alt)
                        # add score gained from this answer
                        question.score += alt.score
                        page.score += alt.score
                        self.questionnaire.score += alt.score
                        #print "selected alternative score: "+str(alt.score)
                
                # The most a user could gain from changing the answer to this question
                question.can_gain = question.max_score - question.score
                # The most a user could lose from changing the answer to this question
                question.can_lose = question.score - question.min_score
                
                if question.can_gain > page.most_profitable_question.can_gain:
                    page.most_profitable_question = question
                if question.can_lose > page.most_prejudicial_question.can_lose:
                    page.most_prejudicial_question = question
            
            most_profitable_questions.append(page.most_profitable_question)
            most_prejudicial_questions.append(page.most_prejudicial_question)
        # print "Score: "+str(self.questionnaire.score)
        # Order by potential gain
        mpf = sorted(most_profitable_questions,
                     key=lambda question: question.can_gain)
        
        self.questionnaire.most_profitable_questions = list(reversed(mpf))
        
        # Order by potential loss
        mpf = sorted(most_prejudicial_questions,
                     key=lambda question: question.can_lose)
        
        self.questionnaire.most_prejudicial_questions = list(reversed(mpf))
        better_score = self.questionnaire.score
        better_outcome = None
        
        worse_score = self.questionnaire.score
        worse_outcome= None
        
        # Determine the outcome of the response to the questionnaire
        # For each possible outcome (from best to worst)
        result = None
        outcomes = list(self.questionnaire.outcome_set.order_by('-minimum_score'))
        i = 0
        self.outcome = None
        for outcome in outcomes:
            if self.questionnaire.score >= outcome.minimum_score:
                # This is the outcome the user got
                outcome.total_score = self.questionnaire.score
                # The score necessary to get a worse outcome
                worse_score = outcome.minimum_score -1
                self.outcome = outcome
                try: worse_outcome = outcomes[i+1]
                except: worse_outcome = outcome
                break
            # The score necessary to get a better outcome
            better_score = outcome.minimum_score
            better_outcome = outcome
            i+=1
        #if not self.outcome: return None
        if self.questionnaire.score == better_score:
            # If no score could result in a higher outcome,
            # look for a worse solution
            self.outcome.alternative_outcome = worse_outcome
            self.calculate_alternative_solution(worse_score, -1)
        else:
            # Else, look for a better solution
            self.outcome.alternative_outcome = better_outcome
            self.calculate_alternative_solution(better_score, 1)
        return self.outcome
        #outcomes = Outcome.objects.
    
    def calculate_alternative_solution(self, other_score, better):
        """
        Calculates the minimum number of alternatives that have to be changed
        in order for the resulting outcome to be different, marking the
        alternative objects as "removed" or "post selected" 
        """
        if better+1:
            question_list = self.questionnaire.most_profitable_questions
        else:
            question_list = self.questionnaire.most_prejudicial_questions
        # A list with the questions that had to be changed
        other_solution = []
        would_have_got = self.questionnaire.score
        for question in question_list:
            other_solution.append(question)
            # Deselect undesired answers
            for alternative in question.alternatives:
                if alternative.selected and alternative.score*better < 0:
                    would_have_got -= alternative.score
                    #alternative.selected = False
                    alternative.removed = True
                    if would_have_got >= other_score: break
            if question.alternatives_left_selected() and would_have_got >= other_score:
                # If enough points have been accumulated in order to pass the
                # user to another outcome, stop looking for more questions
                # to change
                break
            # Select desired answers
            for alternative in question.alternatives:
                if (not alternative.selected) and alternative.score*better > 0:
                    would_have_got += alternative.score
                    alternative.post_selected = True
            # If changing answers to this question is enough, break
            if would_have_got >= other_score:
                break
        else:
            self.outcome.alternative_outcome = self.outcome
        
        self.outcome.would_have_got = would_have_got
        self.outcome.alternative_solution = other_solution
        #print other_solution