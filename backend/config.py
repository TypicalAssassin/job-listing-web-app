import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Config:
    # Get credentials
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'job_listing_db')
    
    # URL-encode the password to handle special characters (since my password has special symbols)
    encoded_password = quote_plus(db_password)
    
    # MySQL Database URI
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{db_user}:{encoded_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # We set to False in production