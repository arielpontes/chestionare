from django.contrib import admin
from models import Questionnaire, Page, Question, Answer

class PageInline(admin.TabularInline):
    model = Page

class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [
        PageInline,
    ]

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('description', 'page')
    inlines = [
        AnswerInline,
    ]

admin.site.register(Questionnaire, QuestionnaireAdmin)
#admin.site.register(Page, PageAdmin)
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Answer, AnswerAdmin)