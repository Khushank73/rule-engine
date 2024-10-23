from flask import Flask, request, jsonify
from rules import create_rule, evaluate_rule
from database import store_rule, load_rule

from flask_cors import CORS

app = Flask(__name__)
CORS(app)



# API to create a rule and store it in the database
@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_string = request.json['rule']
    ast = create_rule(rule_string)
    rule_id = store_rule(rule_string, ast)
    return jsonify({"rule_id": rule_id})

# API to evaluate a rule against user data
@app.route('/evaluate_rule/<int:rule_id>', methods=['POST'])
def evaluate_rule_api(rule_id):
    data = request.json['data']
    rule = load_rule(rule_id)
    result = evaluate_rule(rule['ast'], data)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
