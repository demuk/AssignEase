from app import app
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx', 'accdb', 'doc', 'xls', 'xlsx', 'ppt', 'pptx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB maximum file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return 'No selected file'
        
        # Check if the file has an allowed extension
        if not allowed_file(file.filename):
            return 'Invalid file extension'

        # Save the file with its original filename to the uploads folder
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # You can process the file here, if needed

        return 'File successfully uploaded'

    # If GET request, render the upload form
    return render_template('file_upload.html'), 200

@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413

@app.errorhandler(Exception)
def handle_error(error):
    return 'Internal Server Error', 500
