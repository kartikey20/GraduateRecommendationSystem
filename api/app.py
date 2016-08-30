#!flask/bin/python
from flask import Flask, jsonify, request
from flask.ext.cors import CORS, cross_origin
import create_list


app = Flask(__name__)
CORS(app);
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/wake', methods=['GET'])
@cross_origin()
def wake():
    return jsonify({'result' : 0});

@app.route('/api/classify', methods=['POST'])
@cross_origin()
def classify():
    
    gre_q = request.json['gre_q'];
    gre_v = request.json['gre_v'];
    gre_w = request.json['gre_w'];
    toefl = request.json['toefl'];
    uni_rank = request.json['uni_rank'];
    gpa = request.json['gpa'];
    major = request.json['major'];
    uni_imp = request.json['uni_imp'];
    cost_imp = request.json['cost_imp'];

    universities = create_list.create_list(gre_q, gre_v, gre_w, toefl, uni_rank, gpa, major, uni_imp, cost_imp);

    return jsonify({'results' : universities});

if __name__ == '__main__':
    app.run(debug=True)
