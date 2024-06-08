from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse


@api_view(['GET'])
@permission_classes([AllowAny])
def api_doc(request):
    api_docs = [
        {
            "name": "Register",
            "endpoint": request.build_absolute_uri('/users/register/'),
            "description": "Register a new user.",
            "required_data": ["password", "email"],
            "optional_data": ["first_name", "last_name"],
            "returns": {
                "success": "token (Authentication token for the registered user)",
                "error": "error message for invalid or incomplete data"
            }
        },
        {
            "name": "Login",
            "endpoint": request.build_absolute_uri('/users/login/'),
            "description": "Log in an existing user.",
            "required_data": ["email", "password"],
            "returns": {
                "success": "token (Authentication token for the logged-in user)",
                "error": "error: 'Invalid credentials' for incorrect login credentials"
            }
        },
        {
            "name": "User Details",
            "endpoint": request.build_absolute_uri('/users/user/'),
            "description": "Retrieve details of the authenticated user.",
            "required_data": None,
            "returns": "Details of the authenticated user"
        },
        {
            "name": "Search Users",
            "endpoint": request.build_absolute_uri('/users/search/'),
            "description": "Search for users by email or username.",
            "required_data": ["keyword"],
            "returns": "List of users matching the search criteria"
        },
        {
            "name": "Send Friend Request",
            "endpoint": request.build_absolute_uri('/connections/send_friend_request/'),
            "description": "Send a friend request from the authenticated user to another user.",
            "required_data": ["to_user_id"],
            "returns": {
                "success": "message: 'Friend request sent successfully.'",
                "error": [
                    "error: 'You cannot send a friend request to yourself.'",
                    "error: 'Friend request already sent.'",
                    "other relevant error messages"
                ]
            }
        },
        {
            "name": "Accept Friend Request",
            "endpoint": request.build_absolute_uri('/connections/accept_friend_request/'),
            "description": "Accept a friend request sent to the authenticated user.",
            "required_data": ["from_user_id"],
            "returns": {
                "success": "message: 'Friend request accepted successfully.'",
                "error": [
                    "error: 'Friend request already accepted.'",
                    "other relevant error messages"
                ]
            }
        },
        {
            "name": "Reject Friend Request",
            "endpoint": request.build_absolute_uri('/connections/reject_friend_request/'),
            "description": "Reject a friend request sent to the authenticated user.",
            "required_data": ["from_user_id"],
            "returns": {
                "success": "message: 'Friend request rejected successfully.'",
                "error": [
                    "error: 'Friend request already accepted.'",
                    "other relevant error messages"
                ]
            }
        },
        {
            "name": "Check Pending Requests",
            "endpoint": request.build_absolute_uri('/connections/pending_requests/'),
            "description": "Retrieve pending friend requests sent to the authenticated user.",
            "required_data": None,
            "returns": "List of pending friend requests"
        },
        {
            "name": "Check Sent Requests",
            "endpoint": request.build_absolute_uri('/connections/sent_requests/'),
            "description": "Retrieve sent friend requests by the authenticated user.",
            "required_data": None,
            "returns": "List of sent friend requests"
        },
        {
            "name": "Check Friends",
            "endpoint": request.build_absolute_uri('/connections/check_friends/'),
            "description": "Retrieve friends of the authenticated user.",
            "required_data": None,
            "returns": "List of friends"
        }
    ]
    
    return Response(api_docs, status=status.HTTP_200_OK)
