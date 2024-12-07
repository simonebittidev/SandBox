from flask import Flask, jsonify, request, render_template
from prompt import get_llm_response

app = Flask(__name__)

@app.route('/get-string', methods=['GET'])
def get_string():
    # Return a simple JSON response
    return get_llm_response()
    #return jsonify({"output": "Hello, this is a string from the backend!"})

@app.route('/')
def home():
    return render_template('tv.html')

if __name__ == '__main__':
    app.run(debug=True, port=5050)