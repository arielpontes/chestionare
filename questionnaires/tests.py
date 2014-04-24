from django.test import TestCase, TransactionTestCase
from django.core.urlresolvers import reverse
from django.core import management

from questionnaires.models import Questionnaire

def create_questionnaire(name, description):
    # Create questionnaire
    return Questionnaire.objects.create(name=name, description=description)

class QuestionnaireViewTests(TestCase):
    def test_index_view_with_no_questionnaires(self):
        # If no questionnaire exist, an appropriate message should be displayed.
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There is no questionnaire available yet.")
        self.assertQuerysetEqual(response.context['questionnaires'], [])

    def test_index_view_with_a_questionnaire(self):
        create_questionnaire(name="How well does this test work?", description="A questionnaire for testing purposes.")
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['questionnaires'],
            ['<Questionnaire: How well does this test work?>']
        )
    
    def test_solve_view_with_invalid_questionnaire(self):
        q = create_questionnaire(name="How something are you?", description="A questionnaire to determine how something you are.")
        response = self.client.get(reverse('solve', args=(q.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, but the questionnaire you selected has no questions and can therefore not be answered.")
    
    def test_solve_view_with_valid_questionnaire(self):
        management.call_command('loaddata', 'questionnaires/fixtures/sample_data.json')
        response = self.client.get(reverse('solve', args=(3,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Demographics")
    