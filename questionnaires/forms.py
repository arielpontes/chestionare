from django import forms

# The answer form for a specific question
class AnswerForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['question_'+str(question.id)+'_answer'] = forms.ModelChoiceField(queryset=question.alternative_set, widget=forms.CheckboxSelectMultiple(), empty_label=None, label=str(question))

# The form for answering a whole page 
class PageForm():
    def __init__(self, page, dict=None):
        if dict is not None:
            # If there is a dictionary with form data, makes bound form
            self.is_bound = True
            self.is_valid_attr = True
        else:
            # Otherwise makes unbound form to be answered
            self.is_bound = False
            self.is_valid_attr = False
        # A page form is composed of many answer forms
        self.answer_forms = {}
        self.errors = {}
        
        # For each question in the page
        for q in page.question_set.all():
            key = "question_"+str(q.id)+"_answer"
            if dict is not None:
                # If form received data
                # Create a answer form for this question
                af = AnswerForm(q, { key: dict.get(key, None) })
                try: self.errors[key] = af.errors[key]
                except: self.errors[key] = [] 
                # A page form is valid iff all its answer forms are valid
                self.is_valid_attr &= af.is_valid()
                self.answer_forms[key] = af
            else:
                # Else just make an unbound form
                self.answer_forms[key] = AnswerForm(q)
    
    # A page form is valid iff all its answer forms are valid
    def is_valid(self):
        return self.is_valid_attr
    
    # Returns a string with all the answer forms fields and labes together as an html string
    def to_html(self):
        result = ''
        for q in self.answer_forms.values():
            # Gets answer forms as lists
            result += q.as_ul()
        return result