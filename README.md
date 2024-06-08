# Django Social Network

This project is a simple social network built with Django and Django Rest Framework. It includes user registration, login, and a basic friend request system.

## Features

- User registration and authentication
- Sending and accepting friend requests
- Viewing pending and sent friend requests
- Paginated user search

##Brief API descriptions

1. **Register**
   - Endpoint: `users/register/`
   - Description: Register a new user.
   - Required Data:  `password`, `email`.
   - optional Data: `first_name`,`last_name`.
   - Returns: 
     - Success: `token` (Authentication token for the registered user).
     - Error: `error` message for invalid or incomplete data.

2. **Login**
   - Endpoint: `users/login/`
   - Description: Log in an existing user.
   - Required Data: `email`, `password`.
   - Returns: 
     - Success: `token` (Authentication token for the logged-in user).
     - Error: `error: 'Invalid credentials'` for incorrect login credentials.

3. **User Details**
   - Endpoint: `users/user/`
   - Description: Retrieve details of the authenticated user.
   - Required Data: None (Authentication token is required).
   - Returns: 
     - Details of the authenticated user.

4. **Search Users**
    - Endpoint: `users/search/`
    - Description: Search for users by email or username.
    - Required Data: `keyword` (Search keyword for email or username).
    - Returns: 
      - List of users matching the search criteria.

5. **Send Friend Request**
   - Endpoint: `connections/send_friend_request/`
   - Description: Send a friend request from the authenticated user to another user.
   - Required Data: `to_user_id` (ID of the user to whom the friend request is sent).
   - Returns: 
     - Success: `message: 'Friend request sent successfully.'`
     - Error: `error: 'You cannot send a friend request to yourself.'`, `error: 'Friend request already sent.'`, or other relevant error messages.

6. **Accept Friend Request**
   - Endpoint: `connections/accept_friend_request/`
   - Description: Accept a friend request sent to the authenticated user.
   - Required Data: `from_user_id` (ID of the user who sent the friend request).
   - Returns: 
     - Success: `message: 'Friend request accepted successfully.'`
     - Error: `error: 'Friend request already accepted.'`, or other relevant error messages.

7. **Reject Friend Request**
   - Endpoint: `connections/reject_friend_request/`
   - Description: Reject a friend request sent to the authenticated user.
   - Required Data: `from_user_id` (ID of the user who sent the friend request).
   - Returns: 
     - Success: `message: 'Friend request rejected successfully.'`
     - Error: `error: 'Friend request already accepted.'`, or other relevant error messages.

8. **Check Pending Requests**
   - Endpoint: `connections/pending_requests/`
   - Description: Retrieve pending friend requests sent to the authenticated user.
   - Required Data: None (Authentication token is required).
   - Returns: 
     - List of pending friend requests.

9. **Check Sent Requests**
   - Endpoint: `connections/sent_requests/`
   - Description: Retrieve sent friend requests by the authenticated user.
   - Required Data: None (Authentication token is required).
   - Returns: 
     - List of sent friend requests.

10. **Check Friends**
   - Endpoint: `connections/check_friends/`
   - Description: Retrieve friends of the authenticated user.
   - Required Data: None (Authentication token is required).
   - Returns: 
     - List of friends.


## Docker set up

### 1. Go to the location where you want your code to be

### 2. Clone the Repository
```bash
git clone https://github.com/rudra-g/social_network_backend_django.git
cd my-django-project
```
### 3. docker compose
```bash
docker-compose build
```
### 4. starting
```bash
docker-compose up
```
### 5. ending
```bash
docker-compose down
```


## Normal Setup

### 1. Go to the location where you want your code to be

### 2. Clone the Repository
```bash
git clone https://github.com/rudra-g/social_network_backend_django.git
cd my-django-project
```
### 3. Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```
### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
### 5. Apply Migrations
```bash
python manage.py migrate
```
### 6. Create a Superuser
```bash
python manage.py createsuperuser
```
### 7. Run the Development Server
```bash
python manage.py runserver
```
### 8. Run Tests
```bash
python manage.py test
```

License
This project is licensed under the MIT License. See the LICENSE file for details.








