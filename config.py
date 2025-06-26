import os
from datetime import timedelta

TMP_DIR = '/tmp'

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-generated-key')
    STATIC_FOLDER = 'static'
    
    # Cache settings
    CACHE_TYPE = 'filesystem'
    CACHE_DIR = os.path.join(TMP_DIR, 'cache')
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_THRESHOLD = 1000
    CACHE_OPTIONS = {
        'mode': 0o600,
    }
    
    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Compression settings
    COMPRESS_MIMETYPES = [
        'text/html',
        'text/css',
        'text/xml',
        'application/json',
        'application/javascript',
        'image/svg+xml'
    ]
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    
    # Static file caching
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(days=7)
    
    # Database settings
    DATABASE_URL = os.environ.get('DATABASE_URL', f'sqlite:///{TMP_DIR}/database.db')
    MAX_CONNECTIONS = 10
    POOL_TIMEOUT = 30
    
    # Image settings
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
    IMAGE_QUALITY = 85
    
    # Pagination
    ITEMS_PER_PAGE = 12
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Create necessary directories
        os.makedirs(os.path.join(TMP_DIR, 'static', 'images'), exist_ok=True)
        os.makedirs(os.path.join(TMP_DIR, 'data'), exist_ok=True)
        os.makedirs(os.path.join(TMP_DIR, 'cache'), exist_ok=True)
        os.makedirs(os.path.join(TMP_DIR, 'logs'), exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    
class ProductionConfig(Config):
    DEBUG = False
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Production specific settings
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 