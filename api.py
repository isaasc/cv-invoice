from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import develop
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/invoice', methods=['POST'])
@cross_origin()
def invoice():
    try:
        image_data = request.json['image']
        # decoded_data = base64.b64decode(image_data).decode('utf-8')
        valor, dados = develop.run_tesseract(image_data)
        parsed = json.loads(dados)
        return jsonify({'total': valor, 'empresa': parsed})  # jsonify({'valor-total': valor})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)