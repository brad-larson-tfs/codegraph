from flask import Flask, render_template, request, jsonify
from sympy import sympify
from sympy.core.sympify import SympifyError

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expr = data.get('expression', '')
    try:
        result = sympify(expr)
        return jsonify({'result': str(result.evalf())})
    except (SympifyError, Exception):
        return jsonify({'result': 'Error'}), 400

if __name__ == '__main__':
    app.run(debug=True)
