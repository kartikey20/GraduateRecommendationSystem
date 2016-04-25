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
    return jsonify({'gre_q' : request.json['gre_q'],
    				'gre_v' : request.json['gre_v'],
    				'gre_w' : request.json['gre_w'],
    				'toefl' : request.json['toefl'],
    				'uni_rank' : request.json['uni_rank'],
    				'gpa' : request.json['gpa'],
    				'major' : request.json['major'],
    				'uni_imp' : request.json['uni_imp'],
    				'cost_imp' : request.json['cost_imp']
				  });

if __name__ == '__main__':
    app.run(debug=True)