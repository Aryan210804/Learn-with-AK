import os

class Config:
    """Application configuration"""
    
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-2026'
    
    # Database configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'learn_with_ak.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Super admin email (hardcoded as per requirements)
    SUPER_ADMIN_EMAIL = 'aryankumar735588@gmail.com'
    
    # Flask-Login settings
    REMEMBER_COOKIE_DURATION = 86400  # 1 day in seconds
    SESSION_PROTECTION = 'strong'
