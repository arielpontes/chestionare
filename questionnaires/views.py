from django.http import HttpResponse
from django.shortcuts import render, redirect

from models import Questionnaire, OpenQuestionnaire

def index(request):
    questionnaires = Questionnaire.objects.all()
    return render(request, 'index.html', {'questionnaires': questionnaires})

def show(request, id):
    answer = OpenQuestionnaire(request, id)
    # If the questionnaire doesn't have pages or questions, show page for invalid questionnaire
    if answer.invalid_questionnaire: return render(request, 'invalid.html')
    if request.method == "POST":
        if answer.is_valid() and not answer.go_to_next_page():
            # If the answer to the open questionnaire is valid and there is no next page, show the results
            return render(request, 'results.html', { "outcome": answer.outcome() })
    return render(request, 'show.html', { 'answer': answer })

def clear_test(request):
    try: request.session.pop("open_questionnaires")
    except: print "whatever"
    return HttpResponse("Clear")

def results(request):
    request.session.pop("open_questionnaires")
    questionnaire = Questionnaire.objects.get(id=id)
    return render(request, 'results.html', { 'questionnaire': questionnaire })