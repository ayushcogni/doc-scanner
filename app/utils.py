import os
import hashlib
import shutil
from .models import FileMetadata
from . import db
from flask import current_app as app

def calculate_checksum(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()

def monitor_and_process_files():
    input_folder = app.config['INPUT_FOLDER']
    errors_folder = app.config['ERRORS_FOLDER']
    processed_folder = app.config['PROCESSED_FOLDER']
    print("inside monitor function")
    for subdir, dirs, files in os.walk(input_folder):
        print("value of files ==", subdir, dirs, files)
        if subdir == input_folder:  # Skip the root input folder
            continue

        if len(files) != 6:
            move_folder(subdir, errors_folder)
            continue

        # Validate files
        validation_status = validate_files(subdir, files)
        
        # Move folder based on validation status
        if validation_status == 'processed':
            move_folder(subdir, processed_folder)
        else:
            move_folder(subdir, errors_folder)

        # Save file metadata to the database
        for file in files:
            file_path = os.path.join(subdir, file)
            checksum = calculate_checksum(file_path)
            file_metadata = FileMetadata(
                file_path=file_path,
                file_name=file,
                checksum=checksum,
                upload_time=db.func.now(),
                validation_status=validation_status,
                process_status='processed' if validation_status == 'processed' else 'error'
            )
            db.session.add(file_metadata)
        db.session.commit()
        
    # Retrieve all file metadata from the database
    files_metadata = FileMetadata.query.order_by(FileMetadata.upload_time).all()

    #files_metadata = FileMetadata.query.all()
    file_list = [{'file_path': f.file_path, 'file_name': f.file_name, 'checksum': f.checksum,
                  'upload_time': f.upload_time, 'validation_status': f.validation_status,
                  'process_status': f.process_status} for f in files_metadata]

    return file_list

def move_folder(folder_path, destination_folder):
    folder_name = os.path.basename(folder_path)
    destination_path = os.path.join(destination_folder, folder_name)
    shutil.move(folder_path, destination_path)

def validate_files(folder_path, files):
    docx_files = [f for f in files if f.endswith('.docx')]
    odt_files = [f for f in files if f.endswith('.odt')]
    pdf_files = [f for f in files if f.endswith('.pdf')]

    if len(docx_files) != 1 or len(odt_files) != 2 or len(pdf_files) != 3:
        return 'error'

    # Extract filename and language codes
    docx_file = docx_files[0]
    odt_file1, odt_file2 = odt_files
    pdf_file1, pdf_file2, pdf_file3 = pdf_files

    base_name = os.path.splitext(docx_file)[0]
    odt_base1, lang_code1 = os.path.splitext(odt_file1)[0].rsplit('_', 1)
    odt_base2, lang_code2 = os.path.splitext(odt_file2)[0].rsplit('_', 1)
    
    if lang_code1 == lang_code2:
        return 'error'
    
    if sorted([lang_code1, lang_code2]) != sorted(['en', 'de', 'fr']):
        return 'error'

    if not (pdf_file1 == docx_file.replace('.docx', '.pdf') and
            pdf_file2 == f"{odt_base1}_odt_{lang_code1}.pdf" and
            pdf_file3 == f"{odt_base2}_odt_{lang_code2}.pdf"):
        return 'error'

    return 'processed'
