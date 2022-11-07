from flask import Flask, render_template, request
from os import listdir
import cv2
from flask_cors import CORS


def compare(test_path, data1path, data2path):
    # test image
    print(test_path)
    image = cv2.imread(test_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

    # data1 image
    print(data1path)
    image = cv2.imread(data1path)
    gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram1 = cv2.calcHist([gray_image1], [0], None, [256], [0, 256])

    # data2 image
    print(data2path)
    image = cv2.imread(data2path)
    gray_image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram2 = cv2.calcHist([gray_image2], [0], None, [256], [0, 256])


    c1, c2 = 0, 0

    # Euclidean Distance between data1 and test
    i = 0
    while i < len(histogram) and i < len(histogram1):
        c1 += (histogram[i]-histogram1[i])**2
        i += 1
    c1 = c1**(1 / 2)


    # Euclidean Distance between data2 and test
    i = 0
    while i < len(histogram) and i < len(histogram2):
        c2 += (histogram[i]-histogram2[i])**2
        i += 1
    c2 = c2**(1 / 2)

    if (c1 < c2):
        return data1path
    else:
        return data2path



app = Flask(__name__)
CORS(app)

@app.route('/')
def upload_file():
    return render_template(r'./upload.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        file_name = f'temp.{f.filename.split(".")[-1]}'
        f.save(file_name)

        best_path = "./static/Not_Found/not_found.jpg"

        folders = listdir('./static')
        folders.remove('Upload_Image')
        for folder in folders:
            images = listdir(f'./static/{folder}')
            for image in images:
                image_path = f'./static/{folder}/{image}'
                best_path = compare(file_name, image_path, best_path)

        relative_img_path = "." + best_path
        person_name = best_path.split('/')[-2].replace("_", " ")

        return render_template(r'./dashboard.html', name=person_name, img_path=relative_img_path)


if __name__ == '__main__':
    app.run(debug=True)
