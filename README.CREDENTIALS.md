# Credentials Management System

This project uses a centralized credentials management system to handle sensitive configuration data following security best practices.

## Overview

The credentials system consists of:
- `credentials.json` - Central configuration file (gitignored for security)
- `backend/utils/credentials.py` - Credentials manager utility
- Environment variable overrides for production deployments

## Setup

### 1. Create credentials.json

Copy the example file and fill in your actual credentials:

```bash
# Copy the example file
cp server/credentials.example.json server/credentials.json

# Then edit the file with your actual credentials
```

```json
{
  "cloudinary": {
    "cloud_name": "your_cloudinary_cloud_name",
    "api_key": "your_cloudinary_api_key",
    "api_secret": "your_cloudinary_api_secret"
  },
  "google_drive": {
    "service_account_file": "path/to/service-account.json",
    "scopes": ["https://www.googleapis.com/auth/drive"],
    "folder_id": "your_google_drive_folder_id"
  },
  "database": {
    "host": "localhost",
    "port": "3306",
    "name": "giveandtake",
    "user": "giveandtake",
    "password": "giveandtake"
  },
  "django": {
    "secret_key": "your_django_secret_key_here",
    "debug": true,
    "allowed_hosts": ["*"]
  },
  "storage": {
    "type": "cloudinary",
    "options": {
      "folder": "giveandtake",
      "resource_type": "image"
    }
  }
}
```

### 2. Environment Variables (Optional)

For production deployments, you can override credentials using environment variables:

```bash
# Cloudinary
export CLOUDINARY_CLOUD_NAME="your_cloud_name"
export CLOUDINARY_API_KEY="your_api_key"
export CLOUDINARY_API_SECRET="your_api_secret"

# Database
export DB_HOST="your_db_host"
export DB_PORT="5432"
export DB_NAME="your_db_name"
export DB_USER="your_db_user"
export DB_PASSWORD="your_db_password"

# Django
export DJANGO_SECRET_KEY="your_secret_key"
export DJANGO_DEBUG="false"
export DJANGO_ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"

# Production specific
export STORAGE_TYPE="cloudinary"
export GOOGLE_SERVICE_ACCOUNT_FILE="/path/to/service-account.json"
export GOOGLE_DRIVE_FOLDER_ID="your_folder_id"
```

## Security Best Practices

### 1. Never Commit Credentials
- `credentials.json` is already in `.gitignore`
- Never commit real credentials to version control
- Use environment variables in production

### 2. Use Strong Secrets
- Generate strong Django secret keys
- Use unique API keys for each service
- Rotate credentials regularly

### 3. Environment-Specific Configuration
- Use different credentials for development, staging, and production
- Use environment variables for production deployments
- Keep development credentials separate from production

### 4. Access Control
- Limit access to credentials files
- Use service accounts with minimal required permissions
- Regularly audit access and permissions

## Usage in Code

### Basic Usage

```python
from backend.utils.credentials import credentials_manager

# Get Cloudinary configuration
cloudinary_config = credentials_manager.get_cloudinary_config()

# Get database configuration
db_config = credentials_manager.get_database_config()

# Get specific service configuration
google_config = credentials_manager.get_service_config('google_drive')
```

### Validation

```python
# Validate Cloudinary configuration
if credentials_manager.validate_cloudinary_config():
    # Use Cloudinary
    pass
else:
    # Fallback to local storage
    pass
```

### Error Handling

The system gracefully handles missing credentials files:

```python
try:
    config = credentials_manager.get_cloudinary_config()
except FileNotFoundError:
    # Fallback to environment variables or default values
    config = {
        'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'api_key': os.getenv('CLOUDINARY_API_KEY'),
        'api_secret': os.getenv('CLOUDINARY_API_SECRET')
    }
```

## Production Deployment

### Environment Variables for Production

In production environments, it's recommended to use environment variables instead of the `credentials.json` file for enhanced security:

```bash
# Required for production
export SECRET_KEY="your_strong_secret_key"
export DEBUG="false"
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"

# Database
export DB_HOST="your_production_db_host"
export DB_PORT="3306"
export DB_NAME="your_production_db_name"
export DB_USER="your_production_db_user"
export DB_PASSWORD="your_production_db_password"

# Cloudinary
export CLOUDINARY_CLOUD_NAME="your_cloudinary_cloud_name"
export CLOUDINARY_API_KEY="your_cloudinary_api_key"
export CLOUDINARY_API_SECRET="your_cloudinary_api_secret"

# Storage configuration
export STORAGE_TYPE="cloudinary"

# Google Drive (if using)
export GOOGLE_SERVICE_ACCOUNT_FILE="/path/to/service-account.json"
export GOOGLE_DRIVE_FOLDER_ID="your_folder_id"
```

### Production Settings

The production settings (`backend/settings/prod.py`) are configured to:
- Always use environment variables for sensitive data
- Disable DEBUG mode for security
- Use Cloudinary as the default storage type
- Support flexible ALLOWED_HOSTS configuration

## Services Supported

### Cloudinary
- Image upload and management
- Automatic image optimization
- CDN delivery

### Google Drive
- File storage and sharing
- Service account authentication
- Folder organization

### Database
- PostgreSQL configuration
- Connection pooling support
- Unicode support

### Django
- Secret key management
- Debug mode configuration
- Allowed hosts configuration

## Troubleshooting

### Common Issues

1. **FileNotFoundError**: Make sure `credentials.json` exists in the server directory
2. **Invalid JSON**: Check that your JSON file is properly formatted
3. **Missing Credentials**: Ensure all required fields are filled in
4. **Environment Variables**: Verify environment variables are set correctly

### Validation

```python
# Test credentials loading
python -c "from backend.utils.credentials import credentials_manager; print(credentials_manager.load_credentials())"
```

## Migration from Old System

If you're migrating from the old hardcoded credentials system:

1. Create `credentials.json` with your current values
2. Update your settings files to use the credentials manager
3. Test thoroughly in development
4. Deploy with environment variables in production

## Contributing

When adding new services:

1. Add configuration section to `credentials.json` template
2. Add getter method to `CredentialsManager` class
3. Update this README with usage examples
4. Add validation if needed 