"""
This is where we define global variables that can be imported by every module in the application.
"""
import os

from dotenv import load_dotenv, find_dotenv


# Load values from .env file
load_dotenv(find_dotenv())

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Google API integration
GOOGLE_MAPS_API_URL = "https://maps.googleapis.com"
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
