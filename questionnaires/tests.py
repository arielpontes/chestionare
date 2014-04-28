# coding=utf8
from django.test import TestCase, TransactionTestCase
from django.core.urlresolvers import reverse
from django.core import management

from questionnaires.models import Questionnaire

def create_questionnaire(name, description):
    # Create questionnaire
    return Questionnaire.objects.create(name=name, description=description)

class QuestionnaireViewTests(TestCase):
    def test_index_view_with_no_valid_questionnaires(self):
        # If no valid questionnaire exist, an appropriate message should be displayed.
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There is no questionnaire available yet.")
        self.assertQuerysetEqual(response.context['questionnaires'], [])

    def test_index_view_with_a_valid_questionnaire(self):
        management.call_command('loaddata', 'questionnaires/fixtures/sample_data.json')
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['questionnaires'],
            ['<Questionnaire: How much do you know about Brazil?>']
        )
    
    def test_solve_view_with_invalid_questionnaire(self):
        q = create_questionnaire(name="How something are you?", description="A questionnaire to determine how something you are.")
        response = self.client.get(reverse('solve', args=(q.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, but the questionnaire you selected has no questions or alternatives and can therefore not be answered.")
    
    def test_solve_view_with_valid_questionnaire(self):
        management.call_command('loaddata', 'questionnaires/fixtures/sample_data.json')
        response = self.client.get(reverse('solve', args=(3,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Demographics")
    
    def test_post_form_with_invalid_data_to_solve_view(self):
        management.call_command('loaddata', 'questionnaires/fixtures/sample_data.json')
        response = self.client.post("/questionnaires/3/", {})
        self.assertContains(response, "Demographics") # Stays in the first page
        self.assertContains(response, "This field is required") # Warns about required fields
    
    def test_post_form_with_valid_data_to_solve_view(self):
        management.call_command('loaddata', 'questionnaires/fixtures/sample_data.json')
        response = self.client.post("/questionnaires/3/",
                                    {
                                        'question_1_answer':1,
                                        'question_2_answer':5,
                                        'question_3_answer':9
                                    }
                                   )
        self.assertContains(response, "Culture") # Goes to next page
        self.assertNotContains(response, "This field is required") # Doesn't warn about required fields
    
    def test_post_all_page_forms_with_valid_data_to_solve_view(self):
        management.call_command('loaddata', 'questionnaires/fixtures/sample_data.json')
        response = self.client.post("/questionnaires/3/",
                                    {
                                        'question_1_answer':1,
                                        'question_2_answer':5,
                                        'question_3_answer':9
                                    }
                                   )
        response = self.client.post("/questionnaires/3/",
                                    {
                                        'question_4_answer':14,
                                        'question_5_answer':15,
                                        'question_6_answer':24
                                    }
                                   )
        response = self.client.post("/questionnaires/3/",
                                    {
                                        'question_7_answer':25
                                    }
                                   )
        # Shows outcome
        self.assertContains(response, 'You finished the questionnaire "How much do you know about Brazil?"')
        self.assertNotContains(response, "This field is required") # Doesn't warn about required fields
        
        # Clears session allowing user to solve the questionnaire again
        response = self.client.get(reverse('solve', args=(3,)))
        self.assertContains(response, "Demographics")
    
    def test_post_all_page_forms_with_best_possible_answers_to_solve_view(self):
        management.call_command('loaddata', 'questionnaires/fixtures/sample_data.json')
        response = self.client.post("/questionnaires/3/",
                                    {
                                        'question_1_answer':3,
                                        'question_2_answer':5,
                                        'question_3_answer':11
                                    }
                                   )
        response = self.client.post("/questionnaires/3/",
                                    {
                                        'question_4_answer':14,
                                        'question_5_answer': [15, 16, 18],
                                        'question_6_answer':22
                                    }
                                   )
        response = self.client.post("/questionnaires/3/",
                                    {
                                        'question_7_answer':26
                                    }
                                   )
        # Shows outcome
        self.assertContains(response, 'You finished the questionnaire "How much do you know about Brazil?"')
        #print response
        self.assertContains(response, 'You scored 18: Mandou muito!')
        self.assertContains(response, u'If only you had answered the following questions differently…')
        self.assertContains(response, 'The following Metal bands are Brazilian')
        self.assertContains(response, 'You could NOT have selected')
        self.assertContains(response, 'Angra')
        self.assertContains(response, u'Then you would have scored')
        self.assertContains(response, u'16 – Hum… mais ou menos…')
        self.assertNotContains(response, "This field is required") # Doesn't warn about required fields
        
        # Clears session allowing user to solve the questionnaire again
        response = self.client.get(reverse('solve', args=(3,)))
        self.assertContains(response, "Demographics")
        
    def test_post_all_page_forms_with_worst_possible_answers_to_solve_view(self):
        management.call_command('loaddata', 'questionnaires/fixtures/sample_data.json')
        response = self.client.post("/questionnaires/3/",
                                    {
                                        'question_1_answer':[1,2],
                                        'question_2_answer':[4,7],
                                        'question_3_answer':[8,10]
                                    }
                                   )
        response = self.client.post("/questionnaires/3/",
                                    {
                                        'question_4_answer':[12,13],
                                        'question_5_answer': [17, 19],
                                        'question_6_answer':[20,21,23,24]
                                    }
                                   )
        response = self.client.post("/questionnaires/3/",
                                    {
                                        'question_7_answer':[25,27]
                                    }
                                   )
        # Shows outcome
        self.assertContains(response, 'You finished the questionnaire "How much do you know about Brazil?"')
        #print response
        self.assertContains(response, 'You scored -25: Que M***')
        self.assertContains(response, u'If only you had answered the following questions differently…')
        self.assertContains(response, 'The following Metal bands are Brazilian')
        self.assertContains(response, 'You could have selected')
        self.assertContains(response, 'Angra')
        self.assertContains(response, 'Sepultura')
        self.assertContains(response, 'Krisiun')
        self.assertContains(response, 'You could NOT have selected')
        self.assertContains(response, 'Gorgoroth')
        self.assertContains(response, 'Gorod')
        self.assertContains(response, u'Then you would have scored')
        self.assertContains(response, u'-15 – Putz…')
        self.assertNotContains(response, "This field is required") # Doesn't warn about required fields
        
        # Clears session allowing user to solve the questionnaire again
        response = self.client.get(reverse('solve', args=(3,)))
        self.assertContains(response, "Demographics")
    