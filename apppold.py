from flask import Flask, render_template, request
import requests

app = Flask(__name__)

url_prediction_url = "https://mluhqq1-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/766779d8-f96b-4c8c-acf7-2054ca54666d/classify/iterations/Iteration2/url"
url_prediction_key = "a3c10540dbf544418318873aed6aee85"

file_prediction_url = "https://mluhqq1-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/766779d8-f96b-4c8c-acf7-2054ca54666d/classify/iterations/Iteration2/image"
file_prediction_key = "a3c10540dbf544418318873aed6aee85"

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

if __name__ == '__main__':
    app.run(debug=True)
