import os
from datetime import timedelta

class Config:
    # Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sanskar-public-school-production-secret-key-2026-v1')

    # Database setup
    # Uses DATABASE_URL for Postgres in production, falls back to SQLite
    # On Vercel, filesystem is read-only except /tmp
    _db_url = os.environ.get('DATABASE_URL')
    if _db_url:
        if _db_url.startswith('postgres://'):
            _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = _db_url
    elif os.environ.get('VERCEL'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/sanskar_school.db'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///sanskar_school.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session & Security
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max

    # School branding default settings
    SCHOOL_NAME = "Sanskar Public School"
    SCHOOL_MOTTO = "विद्या ददाति विनयम्"
    SCHOOL_TAGLINE = "Nurturing Knowledge. Building Character."
    SCHOOL_PHONE = "+91 79790 48493"
    SCHOOL_EMAIL = "sanskarpublicskl2000@gmail.com"
    SCHOOL_ADDRESS = "MGW7+J27, Bongawar, Bharechnagar, Jharkhand 829117"
