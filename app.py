from flask import Flask, render_template, request
from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

url_prediction_url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/7bd9302a-58cb-427a-9371-c2742101fbaa/classify/iterations/Iteration3/url"
url_prediction_key = "aaf0caa8cf394b549b817edfb1ea76d6"

file_prediction_url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/7bd9302a-58cb-427a-9371-c2742101fbaa/classify/iterations/Iteration3/image"
file_prediction_key ="aaf0caa8cf394b549b817edfb1ea76d6"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'image' in request.files:
            file = request.files['image']
            if file:
                image_bytes = file.read()
                headers = {
                    'Prediction-Key': file_prediction_key,
                    'Content-Type': 'application/octet-stream'
                }
                response = requests.post(file_prediction_url, headers=headers, data=image_bytes)
                response.raise_for_status()
                prediction = response.json()
                predictions = prediction['predictions']
                if predictions:
                    tag_name = predictions[0]['tagName']
                    return render_template('result.html', tag_name=tag_name)
                else:
                    return render_template('result.html', tag_name='No predictions found.')
            else:
                return render_template('result.html', tag_name='No image uploaded.')
        elif 'image' in request.form:  # Handle camera-captured image
            img_data = request.form['image']
            if img_data:
                headers = {
                    'Prediction-Key': file_prediction_key,
                    'Content-Type': 'application/octet-stream'
                }
                image_bytes = base64.b64decode(img_data.split(',')[1])  # Convert base64 to bytes
                response = requests.post(file_prediction_url, headers=headers, data=image_bytes)
                response.raise_for_status()
                prediction = response.json()
                predictions = prediction['predictions']
                if predictions:
                    tag_name = predictions[0]['tagName']
                    return render_template('result.html', tag_name=tag_name)
                else:
                    return render_template('result.html', tag_name='No predictions found.')
            else:
                return render_template('result.html', tag_name='No image captured.')
        elif 'img_url' in request.form:
            img_url = request.form['img_url']
            headers = {
                'Prediction-Key': url_prediction_key,
                'Content-Type': 'application/json'
            }
            data = {
                'url': img_url
            }
            response = requests.post(url_prediction_url, headers=headers, json=data)
            response.raise_for_status()
            prediction = response.json()
            predictions = prediction['predictions']
            if predictions:
                tag_name = predictions[0]['tagName']
                return render_template('result.html', tag_name=tag_name)
            else:
                return render_template('result.html', tag_name='No predictions found.')
        else:
            return render_template('result.html', tag_name='No input provided.')
    except Exception as e:
        app.logger.error(f"An error occurred during image analysis: {e}")
        return render_template('result.html', tag_name='Error during image analysis.')

@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()
    accuracy = data.get("accuracy")
    feedback = data.get("feedback")

    # You can store the feedback and rating in a database
    # For simplicity, we'll just print the data
    print("Received feedback:", feedback)
    print("Received accuracy rating:", accuracy)

    return jsonify({"message": "Thank you for your feedback!"})
if __name__ == '__main__':
    app.run(debug=True)
