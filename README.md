# Custom Your Spin - Ad Management System

A Django-based application for managing advertisements with automatic display functionality.

## Features

- Admin panel for ad management
- Automatic ad display system
- Image upload support
- RESTful API endpoints for ad retrieval

## Problem Solved

This application addresses the issue where ads disappear after system sleep/restart on Render deployment by implementing:

1. **PostgreSQL Database**: Persistent database storage instead of SQLite
2. **Cloud Storage**: Optional AWS S3 integration for media files
3. **Improved Admin Interface**: Better ad management with previews

## Local Development

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Deployment on Render

### Option 1: PostgreSQL Database (Recommended)

1. **Create a PostgreSQL Database on Render:**
   - Go to your Render dashboard
   - Create a new PostgreSQL database
   - Note down the database credentials

2. **Set Environment Variables in Render:**
   ```
   RENDER=true
   POSTGRES_DB=your_database_name
   POSTGRES_USER=your_database_user
   POSTGRES_PASSWORD=your_database_password
   POSTGRES_HOST=your_database_host
   POSTGRES_PORT=5432
   ```

3. **Deploy your application:**
   - Connect your GitHub repository to Render
   - Use the build script: `build.sh`
   - Set the start command: `gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`

### Option 2: Cloud Storage for Media Files

For persistent media storage, you can also set up AWS S3:

1. **Create an S3 Bucket:**
   - Create a bucket in AWS S3
   - Configure CORS if needed

2. **Set Additional Environment Variables:**
   ```
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_STORAGE_BUCKET_NAME=your_bucket_name
   AWS_S3_REGION_NAME=us-east-1
   ```

## API Endpoints

- `GET /ads/latest/` - Get the most recent ad
- `GET /ads/all/` - Get all ads
- `GET /admin/` - Admin interface

## Admin Interface

The improved admin interface includes:

- Image previews
- Creation timestamps
- Search and filtering
- Better organization with fieldsets

## Troubleshooting

### Ads Disappearing After Sleep

**Problem**: Ads disappear when the application goes to sleep on Render.

**Solutions**:
1. **Use PostgreSQL**: The application now automatically switches to PostgreSQL when deployed on Render
2. **Use Cloud Storage**: Configure AWS S3 for persistent media storage
3. **Upgrade Render Plan**: Consider upgrading to a paid plan that doesn't sleep

### Database Connection Issues

If you encounter database connection issues:

1. Check that all environment variables are set correctly
2. Ensure the PostgreSQL database is running
3. Verify network connectivity between your app and database

### Media Files Not Loading

If media files aren't loading:

1. Check that `MEDIA_URL` and `MEDIA_ROOT` are configured correctly
2. Ensure the media directory has proper permissions
3. If using S3, verify AWS credentials and bucket configuration

## File Structure

```
customyourspin/
├── ads/
│   ├── models.py          # Ad model definition
│   ├── views.py           # API views
│   ├── admin.py           # Admin interface
│   └── urls.py            # URL routing
├── backend/
│   ├── settings.py        # Django settings
│   └── urls.py            # Main URL configuration
├── media/                 # Uploaded files (local development)
├── requirements.txt       # Python dependencies
└── build.sh              # Render build script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. 