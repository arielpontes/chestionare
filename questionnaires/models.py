from django.db import models

class Questionnaire(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=255) # Not enforced on Model/Database level, only affects HTML
    
    def __unicode__(self):
        return self.name

class Page(models.Model):
    questionaire = models.ForeignKey(Questionnaire)
    title = models.CharField(max_length=30)

class Question(models.Model):
    description = models.TextField(max_length=255) # Not enforced on Model/Database level, only affects HTML
    page = models.ForeignKey(Page)

class Answer(models.Model):
    question = models.ForeignKey(Question)
    score = models.SmallIntegerField()

class Outcome(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    title = models.CharField(max_length=30)
    message = models.TextField(max_length=255) # Not enforced on Model/Database level, only affects HTML
    