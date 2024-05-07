from flask import Flask, flash, request, redirect, render_template

from werkzeug.utils import secure_filename

from PIL import Image

import io

import base64

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')

def upload_form():

    return render_template('upload.html')

@app.route('/', methods=['POST'])

def upload_image():

    images = []

    for file in request.files.getlist("file[]"):

        print("***************************")

        print("image: ", file)

        if file.filename == '':

            flash('No image selected for uploading')

            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            filestr = file.read()

            img = Image.open(io.BytesIO(filestr))

            width, height = img.size

            ratio = height / 500.0

            img = img.resize((int(width / ratio), 500), Image.ANTIALIAS)

            gray = img.convert('L')

            fm = cv2.Laplacian(np.array(gray), cv2.CV_64F).var()

            result = "Not Blurry"

            if fm < 100:

                result = "Blurry"

            sharpness_value = "{:.0f}".format(fm)

            message = [result,sharpness_value]

            file_object = io.BytesIO()

            img.save(file_object, format='PNG')

            base64img = "data:image/png;base64,"+base64.b64encode(file_object.getvalue()).decode('ascii')

            images.append([message,base64img])

    print("images:", len(images))

    return render_template('upload.html', images=images )

if __name__ == "__main__":

    app.run(debug=True)

