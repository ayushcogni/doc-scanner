import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://doc_user:doc@123@localhost/doc_scanner')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INPUT_FOLDER = '/home/azureuser/doc_scanner/doc-scanner/inpput'
    ERRORS_FOLDER = '/home/azureuser/doc_scanner/doc-scanner/error'
    PROCESSED_FOLDER = '/home/azureuser/doc_scanner/doc-scanner/processed'
