import os

class Config:
    # Secret key for encrypting sessions and JWT tokens
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')

    # Database URI
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///project_tracker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'myjwtsecretkey')

    # Additional configurations can be added here

    # Example: To enable debugging mode based on an environment variable
    DEBUG = os.getenv('DEBUG', 'false').lower() in ['true', '1']

    DEBUG = os.getenv('DEBUG', 'false').lower() in ['true', '1']

