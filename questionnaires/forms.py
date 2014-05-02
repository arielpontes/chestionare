from django import forms

# The answer form for a specific question
class AnswerForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        key = 'question_'+str(question.id)+'_answer'
        self.fields[key] = forms.ModelChoiceField(
                               queryset=question.alternative_set,
                               widget=forms.CheckboxSelectMultiple(),
                               empty_label=None,
                               label=str(question)
                           )

# The form for answering a whole page 
class PageForm():
    def __init__(self, page, form_data=None):
        # A page form is composed of many answer forms
        self.answer_forms = {}
        self.errors = {}
        
        if form_data is not None:
            # "If there is a dictionary with form data, makes a bound form"
            self.is_bound = True
            self.is_valid_attr = True
        else:
            # Otherwise makes unbound form to be answered
            self.is_bound = False
            self.is_valid_attr = False
        
        questions = page.question_set.all()
        
        # For each question in the page
        for q in questions:
            key = "question_"+str(q.id)+"_answer"
            if form_data is not None:
                # If form received data
                # Create a answer form for this question
                af = AnswerForm(q, { key: form_data.get(key, None) })
                try: self.errors[key] = af.errors[key]
                except: self.errors[key] = [] 
                # A page form is valid iff all its answer forms are valid
                self.is_valid_attr &= af.is_valid()
                self.answer_forms[key] = af
            else:
                self.answer_forms[key] = AnswerForm(q)
    
    def is_valid(self):
        """ A page form is valid iff all its answer forms are valid """
        return self.is_valid_attr
    
    def to_html(self):
        """
        Returns a string with all the answer forms fields and labes together as
        an html string
        """
        result = ''
        for q in self.answer_forms.values():
            # Gets answer forms as lists
            result += q.as_ul()
        return result