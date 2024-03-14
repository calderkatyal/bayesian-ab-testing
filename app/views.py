from flask import render_template, request, jsonify
from app import app 
from .bayesian import perform_bayesian_analysis

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.form
        results = perform_bayesian_analysis(data)
        return jsonify(results)

    return render_template('index.html')
