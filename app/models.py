from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FileMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), unique=True, nullable=False)
    file_name = db.Column(db.String(100), nullable=False)
    checksum = db.Column(db.String(64), nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False)
    validation_status = db.Column(db.String(20), nullable=False)
    process_status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<FileMetadata {self.file_name}>'
