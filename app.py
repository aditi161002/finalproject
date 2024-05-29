import os
import sys
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import subprocess

# Ensure the working directory is correctly set
working_dir = '/content/drive/MyDrive/yolov5'
try:
    os.chdir(working_dir)
    sys.path.append(working_dir)
except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(working_dir, 'uploads')
OUTPUT_FOLDER = os.path.join(working_dir, 'outputs')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output_' + filename)
        command = f'python detect.py --source {filepath} --weights last.pt --save-txt --save-conf --project {app.config["OUTPUT_FOLDER"]} --name output_{filename}'
        subprocess.run(command, shell=True)
        
        return send_from_directory(app.config['OUTPUT_FOLDER'], 'output_' + filename + '.mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
