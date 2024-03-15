from flask import render_template, request, redirect, url_for, session, flash
from . import app
from .bayesian import perform_bayesian_analysis, create_histogram

def safe_convert_to_int(value):
    try:
        # Convert to integer, ensuring float strings are handled correctly
        return int(float(value))
    except (ValueError, TypeError):
        # If the conversion fails, raise an error
        raise ValueError("Invalid input: Expected an integer or a float that can be converted to an integer.")

def safe_convert_to_float(value, default=1.0):
    try:
        # Return the float value or default if the input is empty
        return float(value) if value else default
    except ValueError:
        # Use default if the conversion fails
        return default

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            data = {
                'trialsA': safe_convert_to_int(request.form.get('trialsA')),
                'successesA': safe_convert_to_int(request.form.get('successesA')),
                'alphaA': safe_convert_to_float(request.form.get('alphaA')),
                'betaA': safe_convert_to_float(request.form.get('betaB')),
                'trialsB': safe_convert_to_int(request.form.get('trialsB')),
                'successesB': safe_convert_to_int(request.form.get('successesB')),
                'alphaB': safe_convert_to_float(request.form.get('alphaB')),
                'betaB': safe_convert_to_float(request.form.get('betaB'))
            }

            results = perform_bayesian_analysis(data)
            if not results:
                flash('Analysis failed. Please check the input values.', 'error')
                return redirect(url_for('home'))

            plot_path = create_histogram(results['p_A_samples'], results['p_B_samples'])
            session['plot_path'] = plot_path

        except Exception as e:
            flash(str(e), 'error')
            return redirect(url_for('home'))

        return redirect(url_for('results'))

    return render_template('index.html')

@app.route('/results')
def results():
    plot_path = session.get('plot_path')
    if not plot_path:
        flash('No plot to display. Please try submitting the form again.', 'error')
        return redirect(url_for('home'))

    return render_template('results.html', plot_path=plot_path)
