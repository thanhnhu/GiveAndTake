import json
import os
from typing import Dict, Any, Optional


class CredentialsManager:
    """
    A utility class to manage credentials from a JSON file following best practices.
    Supports environment variable overrides for security.
    """
    
    def __init__(self, credentials_file: str = None):
        """
        Initialize the credentials manager.
        
        Args:
            credentials_file: Path to the credentials JSON file. 
                            Defaults to 'credentials.json' in the server directory.
        """
        if credentials_file is None:
            # Get the server directory (parent of backend)
            server_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            credentials_file = os.path.join(server_dir, 'credentials.json')
            print("server_dir", server_dir)
            print("credentials_file", credentials_file)
        
        self.credentials_file = credentials_file
        self._credentials = None
    
    def load_credentials(self) -> Dict[str, Any]:
        """
        Load credentials from the JSON file.
        
        Returns:
            Dictionary containing all credentials
            
        Raises:
            FileNotFoundError: If credentials file doesn't exist
            json.JSONDecodeError: If credentials file is invalid JSON
        """
        if self._credentials is None:
            if not os.path.exists(self.credentials_file):
                raise FileNotFoundError(
                    f"Credentials file not found: {self.credentials_file}. "
                    "Please create this file with your service credentials."
                )
            
            with open(self.credentials_file, 'r', encoding='utf-8') as f:
                self._credentials = json.load(f)
        
        return self._credentials
    
    def get_cloudinary_config(self) -> Dict[str, str]:
        """
        Get Cloudinary configuration with environment variable overrides.
        
        Returns:
            Dictionary with cloudinary configuration
        """
        credentials = self.load_credentials()
        cloudinary_config = credentials.get('cloudinary', {})
        
        # Allow environment variable overrides for security
        return {
            'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME', cloudinary_config.get('cloud_name')),
            'api_key': os.getenv('CLOUDINARY_API_KEY', cloudinary_config.get('api_key')),
            'api_secret': os.getenv('CLOUDINARY_API_SECRET', cloudinary_config.get('api_secret'))
        }
    
    def get_google_drive_config(self) -> Dict[str, Any]:
        """
        Get Google Drive configuration.
        
        Returns:
            Dictionary with Google Drive configuration
        """
        credentials = self.load_credentials()
        return credentials.get('google_drive', {})
    
    def get_database_config(self) -> Dict[str, str]:
        """
        Get database configuration with environment variable overrides.
        
        Returns:
            Dictionary with database configuration
        """
        credentials = self.load_credentials()
        db_config = credentials.get('database', {})
        
        # Allow environment variable overrides for security
        return {
            'host': os.getenv('DB_HOST', db_config.get('host', 'localhost')),
            'port': os.getenv('DB_PORT', db_config.get('port', '5432')),
            'name': os.getenv('DB_NAME', db_config.get('name', 'giveandtake')),
            'user': os.getenv('DB_USER', db_config.get('user', 'giveandtake')),
            'password': os.getenv('DB_PASSWORD', db_config.get('password', 'giveandtake'))
        }
    
    def get_django_config(self) -> Dict[str, Any]:
        """
        Get Django configuration with environment variable overrides.
        
        Returns:
            Dictionary with Django configuration
        """
        credentials = self.load_credentials()
        django_config = credentials.get('django', {})
        
        return {
            'secret_key': os.getenv('DJANGO_SECRET_KEY', django_config.get('secret_key')),
            'debug': os.getenv('DJANGO_DEBUG', 'true').lower() == 'true',
            'allowed_hosts': os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')
        }
    
    def get_storage_config(self) -> Dict[str, Any]:
        """
        Get storage configuration.
        
        Returns:
            Dictionary with storage configuration
        """
        credentials = self.load_credentials()
        return credentials.get('storage', {'type': 'local'})
    
    def validate_cloudinary_config(self) -> bool:
        """
        Validate that Cloudinary configuration is complete.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        config = self.get_cloudinary_config()
        required_fields = ['cloud_name', 'api_key', 'api_secret']
        
        for field in required_fields:
            if not config.get(field):
                return False
        
        return True
    
    def get_service_config(self, service_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific service.
        
        Args:
            service_name: Name of the service (e.g., 'cloudinary', 'google_drive')
            
        Returns:
            Service configuration dictionary or None if not found
        """
        credentials = self.load_credentials()
        return credentials.get(service_name)


# Global instance for easy access
credentials_manager = CredentialsManager() 