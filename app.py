from flask import Flask, render_template, request, redirect, send_file, jsonify
import subprocess
import os

app = Flask(__name__)

# Path to the Blender script
BLENDER_SCRIPT_PATH = "update_text_render.py"
# Path to the final rendered video
VIDEO_PATH = "final_video_with_musi.mp4"

# Track the rendering state
rendering = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    global rendering
    new_text = request.form['new_text']
    
    # Run Blender in background to render the video
    blender_command = f'blender --background --python {BLENDER_SCRIPT_PATH} -- {new_text}'
    subprocess.Popen(blender_command, shell=True)

    # Set rendering flag to True
    rendering = True
    
    return render_template('progress.html')

@app.route('/progress')
def progress():
    global rendering
    if os.path.exists(VIDEO_PATH):
        rendering = False
        return jsonify({'status': 'done'})
    else:
        return jsonify({'status': 'rendering'})

@app.route('/download')
def download_file():
    # Path to the final video
    return send_file(VIDEO_PATH, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
