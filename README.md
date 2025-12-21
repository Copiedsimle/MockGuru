# Mock Exam Project

A Django-based mock exam application with blog functionality.

## Features

- Exam management with questions and sections
- Blog posts and notes
- User authentication
- Admin interface

## Cloudinary Setup

This project uses Cloudinary for media file storage. To set it up:

1. Create a [Cloudinary account](https://cloudinary.com/)
2. Get your API credentials from the Cloudinary dashboard
3. Copy `.env.example` to `.env` and fill in your credentials:
   ```
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```
4. For production deployment, add these as environment variables in your hosting platform

### Testing Cloudinary Setup

Run the test script to verify your configuration:

```bash
python test_cloudinary.py
```

## Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`

## Production Deployment on Render

This project is configured for deployment on Render using a `Procfile`.

### Deployment Steps

1. Connect your GitHub repository to Render
2. Create a new **Web Service** from your repository
3. Configure the service with these settings:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python3 manage.py collectstatic --noinput && python3 manage.py migrate`
   - **Start Command**: Will be auto-detected from `Procfile` (`gunicorn mockexam.wsgi:application --bind 0.0.0.0:$PORT`)
4. Add environment variables:
   - `DEBUG=false`
   - `SECRET_KEY` (generate a secure random key)
   - `ALLOWED_HOSTS` (your Render service URL)
   - `CLOUDINARY_CLOUD_NAME` (from Cloudinary dashboard)
   - `CLOUDINARY_API_KEY` (from Cloudinary dashboard)
   - `CLOUDINARY_API_SECRET` (from Cloudinary dashboard)
5. Enable **PostgreSQL** database in the service settings

### Environment Variables

Set these in your Render service:

- `DEBUG=false` (disables debug mode)
- `SECRET_KEY` (use a long random string)
- `ALLOWED_HOSTS` (your Render domain, e.g., `yourapp.onrender.com`)
- `DATABASE_URL` (automatically provided by Render's PostgreSQL)
- `CLOUDINARY_CLOUD_NAME` (from Cloudinary dashboard)
- `CLOUDINARY_API_KEY` (from Cloudinary dashboard)
- `CLOUDINARY_API_SECRET` (from Cloudinary dashboard)

### Database

Render provides PostgreSQL automatically. The application automatically switches to PostgreSQL in production when `DATABASE_URL` is present.

### Static Files

Static files are collected during the build process and served by Render.

## Project Structure

- `mockexam/`: Main Django project settings
- `exam/`: Exam management app
- `blog/`: Blog and notes app
- `media/`: User-uploaded media files
- `staticfiles/`: Collected static files for production