from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image']
        if image_file:
            # Save uploaded image
            input_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}.jpg")
            image_file.save(input_path)

            # Compress image using PIL
            output_path = os.path.join(COMPRESSED_FOLDER, f"compressed_{os.path.basename(input_path)}")
            img = Image.open(input_path)
            img.save(output_path, "JPEG", optimize=True, quality=30)

            return send_file(output_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
