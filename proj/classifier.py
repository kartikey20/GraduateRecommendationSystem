#!flask/bin/python
from flask import Flask, jsonify
from flask import request
from flask.ext.cors import CORS, cross_origin

app = Flask(__name__)
CORS(app);
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/classify', methods=['POST'])
@cross_origin()
def classify():
    return jsonify({'data': request.json['gpa']});

if __name__ == '__main__':
    app.run(debug=True)