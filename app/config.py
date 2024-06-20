import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///file_metadata.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INPUT_FOLDER = '/home/azureuser/doc_scanner/doc-scanner/inpput'
    ERRORS_FOLDER = '/home/azureuser/doc_scanner/doc-scanner/error'
    PROCESSED_FOLDER = '/home/azureuser/doc_scanner/doc-scanner/processed'
