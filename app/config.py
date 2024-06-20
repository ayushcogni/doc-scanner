import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///file_metadata.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INPUT_FOLDER = 'input'
    ERRORS_FOLDER = 'errors'
    PROCESSED_FOLDER = 'processed'
