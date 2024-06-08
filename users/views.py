from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Value as V
from django.db.models.functions import Concat 
import re

from .serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user.

    This view handles user registration by creating a new user with the provided
    name, password, and email. It also generates an authentication token for
    the newly registered user.

    Args:
        request (HttpRequest): The request object containing 'first_name','last_name',  'password',
                               and 'email' in the POST data.

    Returns:
        Response: A Response object containing the authentication token if the
                  registration is successful, or an error message if the registration
                  fails.
    """

    first_name = request.data.get('first_name',"")
    last_name = request.data.get('last_name',"")
    password = request.data.get('password')
    email = request.data.get('email')
    username = email

    if not username or not password or not email:
        return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).first():
        return Response({'error': 'Email already in use, please login.'}, status=status.HTTP_400_BAD_REQUEST)
    
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not (re.fullmatch(regex, email)):
        return Response({'error': 'Email invalid, please retry.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, 
                                    password=password, 
                                    email=email, 
                                    first_name= first_name, 
                                    last_name=last_name)
    user.save()
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Log in an existing user.

    This view handles user login by authenticating the provided email and password.
    If the credentials are valid, it returns an authentication token.

    Args:
        request (HttpRequest): The request object containing 'email' and 'password'
                               in the POST data.

    Returns:
        Response: A Response object containing the authentication token if the
                  login is successful, or an error message if the login fails.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, username=email, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_details(request):
    """
    Retrieve details of the authenticated user.

    This view returns the details of the authenticated user.

    Args:
        request (HttpRequest): The request object containing the authenticated user token.

    Returns:
        Response: A Response object containing the user's details.
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
    


@api_view(['GET'])
def search_users(request):
    """
    Search for users by email or username.

    This view allows searching for users by a keyword, which can match the exact email
    or any part of the username.

    Args:
        request (HttpRequest): The request object containing the 'keyword' in the
                               query parameters.

    Returns:
        Response: A Response object containing the search results.
    """
    keyword = request.query_params.get('keyword', '').strip()
    page = int(request.query_params.get('page', 1))
    page_size = 10

    if not keyword:
        return Response({'error': 'Search keyword is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Search by email
    user = User.objects.filter(email=keyword).first()
    if user:
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # Search by name
    users = User.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(full_name__icontains=keyword)
    total_users = users.count()

    # Paginate
    start = (page - 1) * page_size
    end = start + page_size
    paginated_users = users[start:end]

    # Construct next page URL
    if end < total_users:
        next_page_url = request.build_absolute_uri(f"?keyword={keyword}&page={page + 1}")
    else:
        next_page_url = None

    serializer = UserSerializer(paginated_users, many=True)

    return Response({
        'total': total_users,
        'page': page,
        'page_size': page_size,
        'results': serializer.data,
        'next': next_page_url
    }, status=status.HTTP_200_OK)

