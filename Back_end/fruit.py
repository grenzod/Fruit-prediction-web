from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np

app = Flask(__name__)

model = load_model('vgg16_fruit_classifier.h5')

class_labels = ['apple', 'avocado', 'banana', 'cherry', 'kiwi', 'mango', 'orange', 'pineapple', 'strawberries',
                'watermelon']


def recognize_fruit(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]

    return class_labels[predicted_class]


@app.route('/recognize-fruit', methods=['POST'])
def recognize():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    image_path = f"temp_image.jpg"
    image_file.save(image_path)

    recognized_fruit = recognize_fruit(image_path)

    return jsonify({"fruit": recognized_fruit})


CORS(app, resources={r"/recognize-fruit": {"origins": "http://localhost:4200"}})

if __name__ == '__main__':
    app.run(debug=True)
