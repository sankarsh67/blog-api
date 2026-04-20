# Blog API
A REST API built with Django and Django REST Framework.
## Features
- User registration and token authentication
- Blog post CRUD (author-only edit/delete)
- Categories with post count
- Comments on posts
- Like / Unlike toggle
- Search, filter, and pagination
- Django admin panel
## Tech Stack
- Python 3.12
- Django 4.x
- Django REST Framework 3.x
- SQLite
## Setup
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
## API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/register/ | Register new user |
| POST | /api/login/ | Login — returns token |
| GET | /api/posts/ | List all posts |
| POST | /api/posts/ | Create post |
| POST | /api/posts/{id}/like/ | Like/unlike |