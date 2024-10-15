import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 100MB max-limit

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lobby')
def lobby():
    return render_template('index.html')

@app.route('/room.html')
def room():
    room_id = request.args.get('room')
    return render_template('room.html', room_id=room_id)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'success': True, 'url': '/' + file_path})

if __name__ == '__main__':
    app.run(debug=True)