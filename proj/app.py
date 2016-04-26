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
    universities = [ {
                    'university' : 'Georgia Tech',
                    'chance' : '0.9',
                    'url' : 'http://www.gatech.edu',
                    'cost' : '15000',
                    'ranking' : '1'
                },
                {
                    'university' : 'University of Georgia',
                    'chance' : '0.7',
                    'url' : 'http://www.uga.edu',
                    'cost' : '12000',
                    'ranking' : '2'
                },
                {   'university' : 'Emory University',
                    'chance' : '0.5',
                    'url' : 'http://www.emory.edu',
                    'cost' : '9000',
                    'ranking' : '3'
                },
                {   'university' : 'Kennesaw State University',
                    'chance' : '0.3',
                    'url' : 'http://www.kennesaw.edu',
                    'cost' : '6000',
                    'ranking' : '4'
                },
                {
                    'university' : 'Georgia State University',
                    'chance' : '0.1',
                    'url' : 'http://www.gsu.edu',
                    'cost' : '3000',
                    'ranking' : '5'
                }
              ]

    return jsonify({'results' : universities});

if __name__ == '__main__':
    app.run(debug=True)