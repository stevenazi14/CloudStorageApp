import os
from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flashing messages

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))
        
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            flash('File uploaded successfully!')
        except Exception as e:
            flash(f'Error uploading file: {str(e)}')
        
        return redirect(url_for('index'))
    
    flash('Invalid request method.')
    return redirect(url_for('index'))

@app.route('/rename/<filename>', methods=['POST'])
def rename_file(filename):
    new_name = request.form['new_name']
    old_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
    
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        flash('File renamed successfully!')
    else:
        flash('File not found!')
    
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

if __name__ == '__main__':
    app.run(debug=True)
