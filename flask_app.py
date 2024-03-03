from flask import Flask, request, jsonify
from reports_generation import *

app = Flask(__name__)


@app.route('/generate_reports', methods=['POST'])
def handle_generate_reports():
    users = request.json  # Assuming the incoming data is JSON formatted
    reports = generate_reports(users)
    return jsonify(reports)


if __name__ == '__main__':
    app.run(port=5000)
