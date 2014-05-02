from django import forms

# The form for answering a whole page 
class PageForm(forms.Form):
    def __init__(self, page, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        # For each question in the page
        for question in page.question_set.all():
            key = "question_"+str(question.id)+"_answer"
            self.fields[key] = forms.ModelMultipleChoiceField(
                                   queryset=question.alternative_set,
                                   widget=forms.CheckboxSelectMultiple(),
                                   label=str(question)
                               )