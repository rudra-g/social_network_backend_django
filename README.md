# Django Social Network

This project is a simple social network built with Django and Django Rest Framework. It includes user registration, login, and a basic friend request system.

## Features

- User registration and authentication
- Sending and accepting friend requests
- Viewing pending and sent friend requests
- Paginated user search

## Requirements

- Python 3.8+
- Django 3.2+
- Django Rest Framework 3.12+
- SQLite (default database)

## Setup

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








