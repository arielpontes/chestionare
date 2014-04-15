from django.db import models

class Questionnaire(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255) # Not enforced on Model/Database level, only affects HTML
    
    def __unicode__(self):
        return self.name

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

class Answer(models.Model):
    question = models.ForeignKey(Question)
    description = models.CharField(max_length=255)
    score = models.SmallIntegerField()
    # non db field
    selected = False
    
    def __unicode__(self):
        return self.description

class Outcome(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    title = models.CharField(max_length=30)
    message = models.TextField(max_length=255) # Not enforced on Model/Database level, only affects HTML
    