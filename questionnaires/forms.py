from django import forms
from models import Answer

class PageForm(forms.Form):
    def __init__(self, page, *args, **kwargs):
        print "hello"
        

class AnswerQuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(AnswerQuestionForm, self).__init__(*args, **kwargs)
        self.fields['selected'] = forms.ModelChoiceField(queryset=question.answer_set, widget=forms.CheckboxSelectMultiple())