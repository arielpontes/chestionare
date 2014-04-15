from django.http import HttpResponse
from django.shortcuts import render, redirect

from models import Questionnaire

def index(request):
    questionnaires = Questionnaire.objects.all()
    return render(request, 'index.html', {'questionnaires': questionnaires})

def show(request, id):
    questionnaire = Questionnaire.objects.get(id=id)
    currquest = request.session.get("current_questionnaire", False) #current_questionnaire
    
    # If is starting test, add test information to session
    if not currquest:
        currquest = {}
        currquest["answers"] = {}
        currquest["previous_page"] = 0
        currquest["done"] = False
        request.session["current_questionnaire"] = currquest
            
    previous_page = currquest["previous_page"]
    # Determines current page
    try: page = questionnaire.page_set.filter(id__gt=previous_page).first()
    except:
        if previous_page is 0:
            return render(request, 'show.html', {'page': None}) # Questionnaire has no pages
        else:
            # The questionnaire is over and the user is sent to the results page
            currquest["done"] = True
    if request.method == 'POST':
        # Updates previous page
        currquest["previous_page"] = page.id
        # Update answers and saves it in the session
        currquest["answers"][str(page.id)] = request.POST
        return redirect("show", id) # Go to next page
    else:
        page.answer_set
        # Renders the page
        return render(request, 'show.html', {'page': page})

def clear_test(request):
    try: request.session.pop("current_questionnaire")
    except: print "whatever"
    return HttpResponse("Clear")

def results(request, id):
    request.session.pop("current_questionnaire")
    questionnaire = Questionnaire.objects.get(id=id)
    return render(request, 'results.html', { 'questionnaire': questionnaire })