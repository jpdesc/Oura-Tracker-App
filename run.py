from dotenv import load_dotenv

load_dotenv()
import os

os.getenv('SQLALCHEMY_DATABASE_URI')

from ouraapp import create_app
import logging

app = create_app()

# from ouraapp import routes
