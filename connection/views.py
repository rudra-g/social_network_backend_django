from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Connection, UserConnectionIntermediateTable
from .throttling import SendFriendRequestThrottle


@api_view(['POST'])
@throttle_classes([SendFriendRequestThrottle])
def send_friend_request(request):
    """
    Send a friend request from the authenticated user to another user.

    This view handles the creation of a friend request. It ensures that a user
    cannot send a friend request to themselves or duplicate an existing request.
    The request is also rate-limited to prevent spamming.

    Args:
        request (HttpRequest): The request object containing the authenticated user token
                               and 'to_user_id' in the POST data.

    Returns:
        Response: A Response object containing a success message if the request is
                  sent successfully, or an error message if the request fails.
    """

    to_user_id = request.data.get('to_user_id')
    to_user = get_object_or_404(User, id=to_user_id)

    if request.user == to_user:
        return Response({'error': 'You cannot send a friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    connection, created = Connection.objects.get_or_create(from_user=request.user, to_user=to_user)

    if not created:
        return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

    # Update UserConnectionIntermediateTable for both users
    from_user_connections, created = UserConnectionIntermediateTable.objects.get_or_create(user=request.user)
    to_user_connections, created = UserConnectionIntermediateTable.objects.get_or_create(user=to_user)

    from_user_connections.sent_requests.add(to_user)
    to_user_connections.pending_requests.add(request.user)

    from_user_connections.save()
    to_user_connections.save()

    return Response({'message': 'Friend request sent successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def accept_friend_request(request):
    """
    Accept a friend request sent to the authenticated user.

    This view marks a friend request as accepted and updates the
    UserConnectionIntermediateTable for both users involved.

    Args:
        request (HttpRequest): The request object containing the authenticated user token
                               and 'from_user_id' in the POST data.

    Returns:
        Response: A Response object containing a success message if the request
                  is accepted successfully, or an error message if the request fails.
    """
    from_user_id = request.data.get('from_user_id')
    from_user = get_object_or_404(User, id=from_user_id)

    connection = get_object_or_404(Connection, from_user=from_user, to_user=request.user)

    if connection.accepted:
        return Response({'error': 'Friend request already accepted.'}, status=status.HTTP_400_BAD_REQUEST)

    connection.accepted = True
    connection.save()

    # Update UserConnectionIntermediateTable for both users
    request_user_connections, created = UserConnectionIntermediateTable.objects.get_or_create(user=request.user)
    from_user_connections, created = UserConnectionIntermediateTable.objects.get_or_create(user=from_user)

    request_user_connections.pending_requests.remove(from_user)
    from_user_connections.sent_requests.remove(request.user)

    request_user_connections.friends.add(from_user)
    from_user_connections.friends.add(request.user)

    request_user_connections.save()
    from_user_connections.save()

    return Response({'message': 'Friend request accepted successfully.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def reject_friend_request(request):
    """
    Reject a friend request sent to the authenticated user.

    This view deletes a friend request and updates the UserConnectionIntermediateTable
    for both users involved.

    Args:
        request (HttpRequest): The request object containing the authenticated user token
                               and 'from_user_id' in the POST data.

    Returns:
        Response: A Response object containing a success message if the request
                  is rejected successfully, or an error message if the request fails.
    """
    from_user_id = request.data.get('from_user_id')
    from_user = get_object_or_404(User, id=from_user_id)

    connection = get_object_or_404(Connection, from_user=from_user, to_user=request.user)

    if connection.accepted:
        return Response({'error': 'Friend request already accepted.'}, status=status.HTTP_400_BAD_REQUEST)
    
    connection.delete()

    # Update UserConnectionIntermediateTable for both users
    request_user_connections, created = UserConnectionIntermediateTable.objects.get_or_create(user=request.user)
    from_user_connections, created = UserConnectionIntermediateTable.objects.get_or_create(user=from_user)

    request_user_connections.pending_requests.remove(from_user)
    from_user_connections.sent_requests.remove(request.user)

    request_user_connections.save()
    from_user_connections.save()

    return Response({'message': 'Friend request rejected successfully.'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def check_pending_requests(request):
    """
    Retrieve pending friend requests for the authenticated user.

    This view returns a list of pending friend requests sent to the
    authenticated user.

    Args:
        request (HttpRequest): The request object containing the authenticated user token.

    Returns:
        Response: A Response object containing a list of pending friend requests.
    """
    user_connections, created = UserConnectionIntermediateTable.objects.get_or_create(user=request.user)
    pending_requests = user_connections.pending_requests.all()
    pending_requests_list = [{'id': user.id, 'username': user.username} for user in pending_requests]

    return Response({'pending_requests': pending_requests_list}, status=status.HTTP_200_OK)

@api_view(['GET'])
def check_sent_requests(request):
    """
    Retrieve sent friend requests for the authenticated user.

    This view returns a list of friend requests sent by the
    authenticated user.

    Args:
        request (HttpRequest): The request object containing the authenticated user token.

    Returns:
        Response: A Response object containing a list of sent friend requests.
    """
    user_connections, created = UserConnectionIntermediateTable.objects.get_or_create(user=request.user)
    sent_requests = user_connections.sent_requests.all()
    sent_requests_list = [{'id': user.id, 'username': user.username} for user in sent_requests]

    return Response({'sent_requests': sent_requests_list}, status=status.HTTP_200_OK)

@api_view(['GET'])
def check_friends(request):
    """
    Retrieve friends for the authenticated user.

    This view returns a list of friends for the
    authenticated user.

    Args:
        request (HttpRequest): The request object containing the authenticated user token.

    Returns:
        Response: A Response object containing a list of friends.
    """
    user_connections, created = UserConnectionIntermediateTable.objects.get_or_create(user=request.user)
    friends = user_connections.friends.all()
    friends_list = [{'id': user.id, 'username': user.username} for user in friends]

    return Response({'friends': friends_list}, status=status.HTTP_200_OK)

