# Mock Exam Project

A Django-based mock exam application with blog functionality.

## Features

- Exam management with questions and sections
- Blog posts and notes
- User authentication
- Admin interface

## Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`

## Production Deployment on Render

This project is configured for deployment on Render using the `render.yaml` file.

### Deployment Steps

1. Connect your GitHub repository to Render
2. Create a new Web Service from your repository
3. Render will automatically use the `render.yaml` configuration
4. The service will:
   - Install Python dependencies
   - Run database migrations
   - Collect static files
   - Start the application with Gunicorn

### Environment Variables

The following environment variables are automatically set by Render:

- `DEBUG`: Set to `false` in production
- `SECRET_KEY`: Auto-generated secure key
- `ALLOWED_HOSTS`: Set to the service domain
- `DATABASE_URL`: PostgreSQL database URL provided by Render

### Database

Render provides a PostgreSQL database. The application automatically switches to PostgreSQL in production when `DATABASE_URL` is present.

### Static Files

Static files are collected during the build process and served by Render.

## Project Structure

- `mockexam/`: Main Django project settings
- `exam/`: Exam management app
- `blog/`: Blog and notes app
- `media/`: User-uploaded media files
- `staticfiles/`: Collected static files for production