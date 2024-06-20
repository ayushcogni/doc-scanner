# app/models.py

from datetime import datetime
from app import db

class FileMetadata(db.Model):
    __tablename__ = 'uploadDocumentsV1'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(50))
    docName = db.Column(db.String(255))
    docType = db.Column(db.String(50))
    publish = db.Column(db.Boolean, default=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    process_st_time = db.Column(db.DateTime)
    process_en_time = db.Column(db.DateTime)
    process_stats = db.Column(db.String(50))
    filepath = db.Column(db.String(255))
    metainfo = db.Column(db.Text)
    project_name = db.Column(db.String(255))
    subscription = db.Column(db.String(255))
    batch_name = db.Column(db.String(255))
