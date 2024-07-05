from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from video_splitter import split_video

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
SPLIT_FOLDER = 'split_videos'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SPLIT_FOLDER'] = SPLIT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    num_parts = int(request.form['num_parts'])
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        split_video(os.path.join(app.config['UPLOAD_FOLDER'], filename), num_parts)
        
        # Move split videos to split folder
        for i in range(num_parts):
            os.rename(f'split_videos/part_{i+1}.avi', os.path.join(app.config['SPLIT_FOLDER'], f'part_{i+1}.avi'))
        
        return jsonify({'message': 'Video split successfully!'})
    else:
        return jsonify({'error': 'No file uploaded.'})

@app.route('/split_videos/<filename>')
def split_video_file(filename):
    return send_from_directory(app.config['SPLIT_FOLDER'], filename)

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_video(filename):
    file_path = os.path.join(app.config['SPLIT_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully.'})
    else:
        return jsonify({'error': 'File not found.'})

if __name__ == '__main__':
    app.run(debug=True)
