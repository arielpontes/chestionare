from django.contrib import admin
from models import Questionnaire, Page, Question, Alternative, Outcome

class PageInline(admin.TabularInline):
    model = Page

class OutcomeInline(admin.TabularInline):
    model = Outcome

class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [
        PageInline, OutcomeInline,
    ]

class AlternativeInline(admin.TabularInline):
    model = Alternative

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('description', 'page')
    inlines = [
        AlternativeInline,
    ]

admin.site.register(Questionnaire, QuestionnaireAdmin)
#admin.site.register(Page, PageAdmin)
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Answer, AnswerAdmin)