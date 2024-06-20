from . import db
from datetime import datetime

class FileMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(256), unique=True, nullable=False)
    checksum = db.Column(db.String(64), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    validation_status = db.Column(db.String(10), nullable=False)  # 'processed' or 'error'
    process_status = db.Column(db.String(10), nullable=True)
    file_name = db.Column(db.String(256), nullable=False)
