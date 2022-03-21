from django.test import TestCase, Client
from django.urls import reverse

from forum.models import User
from rest_framework.authtoken.models import Token

client = Client()


class AuthTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@gmail.com',
            password='test'
        )

    def test_session_auth(self):
        self.assertTrue(client.login(email='test@gmail.com', password='test'))

    def test_token_auth(self):
        auth_data = {
            'email': 'test@gmail.com',
            'password': 'test',
        }
        auth_response = client.post(reverse('token-auth'), data=auth_data)
        token = auth_response.json()['token']
        token_db = Token.objects.get(user=self.user)
        self.assertEqual(token, token_db.key)
