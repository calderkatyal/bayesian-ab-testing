from flask import render_template, request, jsonify
from . import app  
from .bayesian import perform_bayesian_analysis

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Extracting data from the form, make sure the indentation is correct
        def to_float(value, default):
            try:
                return float(value)
            except ValueError:
                return default

        # Extracting and converting data from the form
        trialsA = int(request.form.get('trialsA', 0))
        successesA = int(request.form.get('successesA', 0))
        alphaA = to_float(request.form.get('alphaA', ''), 1.0)
        betaA = to_float(request.form.get('betaA', ''), 1.0)
        trialsB = int(request.form.get('trialsB', 0))
        successesB = int(request.form.get('successesB', 0))
        alphaB = to_float(request.form.get('alphaB', ''), 1.0)
        betaB = to_float(request.form.get('betaB', ''), 1.0)

        data = {
            'trialsA': int(trialsA),
            'successesA': int(successesA),
            'alphaA': float(alphaA),
            'betaA': float(betaA),
            'trialsB': int(trialsB),
            'successesB': int(successesB),
            'alphaB': float(alphaB),
            'betaB': float(betaB)
        }

        results = perform_bayesian_analysis(data)
        return jsonify(results)  # or use render_template to show results

    return render_template('index.html')
