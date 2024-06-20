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
    for subdir, dirs, files in os.walk(app.config['INPUT_FOLDER']):
        if subdir == app.config['INPUT_FOLDER']:  # Skip the root input folder
            continue

        if len(files) != 6:
            move_folder(subdir, app.config['ERRORS_FOLDER'])
            continue

        # Validate files
        validation_status = validate_files(subdir, files)
        
        # Move folder based on validation status
        if validation_status == 'processed':
            move_folder(subdir, app.config['PROCESSED_FOLDER'])
        else:
            move_folder(subdir, app.config['ERRORS_FOLDER'])

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
