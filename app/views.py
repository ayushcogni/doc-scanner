from flask import request, jsonify
from . import db
from .models import FileMetadata
from .utils import calculate_checksum, monitor_and_process_files
from flask import current_app as app
import os

@app.route('/files-by-status', methods=['GET'])
def get_files_by_status():
    status = request.args.get('status')
    if status not in ['processed', 'error']:
        return jsonify({'error': 'Invalid status parameter'}), 400

    files = FileMetadata.query.filter_by(validation_status=status).all()
    file_list = [{'file_path': f.file_path, 'file_name': f.file_name, 'checksum': f.checksum,
                  'upload_time': f.upload_time, 'validation_status': f.validation_status,
                  'process_status': f.process_status} for f in files]

    return jsonify(file_list), 200

@app.route('/upload-file', methods=['POST'])
def upload_file():
    file = request.files['file']
    folder_name = request.form['folder']
    destination_folder = os.path.join(app.config['INPUT_FOLDER'], folder_name)
    os.makedirs(destination_folder, exist_ok=True)

    file_path = os.path.join(destination_folder, file.filename)
    file.save(file_path)
    checksum = calculate_checksum(file_path)

    new_file = FileMetadata(file_path=file_path, checksum=checksum,
                            validation_status='pending', file_name=file.filename)
    db.session.add(new_file)
    db.session.commit()

    return jsonify({'message': 'File uploaded successfully'}), 201
