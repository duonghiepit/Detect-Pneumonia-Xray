from flask import Flask, render_template, request, send_file
import os

from utils import allowed_file, process_image
import config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Route 
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']

        if file.filename == '':
            return 'No selected file'
        
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['OUTPUT_FOLDER'], file.filename)
            file.save(filename)

            output_filename = os.path.join(app.config['OUTPUT_FOLDER'], 'annotated_'+file.filename)

            process_image(filename, output_filename)

            return send_file(output_filename, mimetype='image/jpeg')
        
    return render_template('index.html')


if __name__ == "__main__":
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)

    app.run(debug=True)
            