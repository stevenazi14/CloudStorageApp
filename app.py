import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    flash('File uploaded successfully!')
    return redirect(url_for('index'))

@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('File deleted successfully!')
    else:
        flash('File not found!')
    return redirect(url_for('index'))

@app.route('/rename/<filename>', methods=['POST'])
def rename_file(filename):
    new_name = request.form['new_name']
    old_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    new_file = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
    
    if os.path.exists(old_file):
        os.rename(old_file, new_file)
        flash('File renamed successfully!')
    else:
        flash('File not found!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
