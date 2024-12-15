from flask import Flask, jsonify, request, render_template
from prompt import get_llm_response

app = Flask(__name__)

cache = {}

@app.route('/get-string', methods=['GET'])
def get_string():
    # Retrieve the 'date' query parameter from the request
    date_param = request.args.get('date')

    if date_param:
        try:
            # Parse the date parameter to a Python datetime object
            from datetime import datetime
            parsed_date = datetime.fromisoformat(date_param)
            parsed_date = parsed_date.date()
            if cache.get(str(parsed_date), False):
                return cache[str(parsed_date)]
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO 8601 format, e.g., YYYY-MM-DDTHH:MM:SS"}), 400
    else:
        parsed_date = None

    # Pass the parsed date to the get_llm_response function (if applicable)
    response = get_llm_response(date=parsed_date)

    if parsed_date:
        cache[str(parsed_date)] = response

    return response
    #return jsonify({"output": "Hello, this is a string from the backend!"})

@app.route('/')
def home():
    return render_template('tv.html')

if __name__ == '__main__':
    app.run(debug=True, port=5050)