from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Connection, UserConnectionIntermediateTable
from django.urls import reverse

class FriendRequestTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create users
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        # Create tokens
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

        # Set up URLs
        self.send_request_url = reverse('send_friend_request')
        self.accept_request_url = reverse('accept_friend_request')
        self.reject_request_url = reverse('reject_friend_request')
        self.pending_requests_url = reverse('check_pending_requests')
        self.sent_requests_url = reverse('check_sent_requests')
        self.friends_url = reverse('check_friends')
    
    def authenticate(self, user):
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_send_friend_request(self):
        self.authenticate(self.user1)
        response = self.client.post(self.send_request_url, {'to_user_id': self.user2.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Friend request sent successfully.')

        # Test sending friend request to self
        response = self.client.post(self.send_request_url, {'to_user_id': self.user1.id})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'You cannot send a friend request to yourself.')

        # Test sending duplicate friend request
        response = self.client.post(self.send_request_url, {'to_user_id': self.user2.id})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Friend request already sent.')
    
    def test_accept_friend_request(self):
        # Send friend request from user1 to user2
        Connection.objects.create(from_user=self.user1, to_user=self.user2)

        self.authenticate(self.user2)
        response = self.client.post(self.accept_request_url, {'from_user_id': self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Friend request accepted successfully.')

        # Test accepting already accepted request
        response = self.client.post(self.accept_request_url, {'from_user_id': self.user1.id})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Friend request already accepted.')
    
    def test_reject_friend_request(self):
        # Send friend request from user1 to user2
        Connection.objects.create(from_user=self.user1, to_user=self.user2)

        self.authenticate(self.user2)
        response = self.client.post(self.reject_request_url, {'from_user_id': self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Friend request rejected successfully.')

        # Test rejecting already accepted request
        Connection.objects.create(from_user=self.user1, to_user=self.user2, accepted=True)
        response = self.client.post(self.reject_request_url, {'from_user_id': self.user1.id})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Friend request already accepted.')
    
    def test_check_pending_requests(self):
        self.authenticate(self.user2)
        response = self.client.get(self.pending_requests_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['pending_requests'], [])

        # Send friend request from user1 to user2
        user_connections, created = UserConnectionIntermediateTable.objects.get_or_create(user=self.user2)
        user_connections.pending_requests.add(self.user1)
        
        response = self.client.get(self.pending_requests_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['pending_requests']), 1)
        self.assertEqual(response.data['pending_requests'][0]['id'], self.user1.id)
    
    def test_check_sent_requests(self):
        self.authenticate(self.user1)
        response = self.client.get(self.sent_requests_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['sent_requests'], [])

        # Send friend request from user1 to user2
        user_connections, created = UserConnectionIntermediateTable.objects.get_or_create(user=self.user1)
        user_connections.sent_requests.add(self.user2)
        
        response = self.client.get(self.sent_requests_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['sent_requests']), 1)
        self.assertEqual(response.data['sent_requests'][0]['id'], self.user2.id)
    
    def test_check_friends(self):
        self.authenticate(self.user1)
        response = self.client.get(self.friends_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['friends'], [])

        # Accept friend request from user2 to user1
        user_connections, created = UserConnectionIntermediateTable.objects.get_or_create(user=self.user1)
        user_connections.friends.add(self.user2)
        user_connections.save()
        response = self.client.get(self.friends_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['friends']), 1) 
        self.assertEqual(response.data['friends'][0]['id'], self.user2.id)


