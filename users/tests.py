from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from .serializers import UserSerializer

class UserAccountTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create a user
        self.user1 = User.objects.create_user(first_name='user1', 
                                              password='pass', 
                                              email='user1@example.com',
                                              username='user1@example.com')
        self.user1_token = Token.objects.create(user=self.user1)

        # Set up URLs
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_details_url = reverse('user_details')
        self.search_users_url = reverse('search_users')

    def test_register_success(self):
        data = {
            'password': 'newpass',
            'first_name': 'new',
            'last_name': 'user',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)

    def test_register_missing_fields(self):
        data = {
            'email': 'newuser'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Please provide all required fields')

    def test_login_success(self):
        data = {
            'email': 'user1@example.com',
            'password': 'pass'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        data = {
            'email': 'user1@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    def test_user_details_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(self.user_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'user1@example.com')
        self.assertEqual(response.data['email'], 'user1@example.com')

    def test_search_users_by_email(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(self.search_users_url, {'keyword': 'user1@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'user1@example.com')
        self.assertEqual(response.data['email'], 'user1@example.com')

    def test_search_users_by_name(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(self.search_users_url, {'keyword': 'user1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['username'], 'user1@example.com')

    def test_search_users_no_keyword(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(self.search_users_url, {'keyword': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Search keyword is required.')
