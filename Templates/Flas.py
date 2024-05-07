from flask import Flask, render_template, request

from PIL import Image

app = Flask(__name__)

def detect_blur(image):

    # Code to detect blur in an image

    return (image.filename, blur_score)

@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':

        images = []

        for file in request.files.getlist('file[]'):

            image = Image.open(file)

            blur_score = detect_blur(image)

            images.append(((file.filename, blur_score), file))

        return render_template('index.html', images=images)

    return render_template('index.html')

if __name__ == '__main__':

    app.run(debug=True)

