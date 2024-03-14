import pymc3 as pm
import numpy as np

def perform_bayesian_analysis(data):
    with pm.Model() as model:
        # Using data provided in the dictionary
        p_A = pm.Beta('p_A', alpha=data['alphaA'], beta=data['betaA'])
        p_B = pm.Beta('p_B', alpha=data['alphaB'], beta=data['betaB'])

        delta = pm.Deterministic('delta', p_A - p_B)

        obs_A = pm.Binomial('obs_A', n=data['trialsA'], p=p_A, observed=data['successesA'])
        obs_B = pm.Binomial('obs_B', n=data['trialsB'], p=p_B, observed=data['successesB'])

        trace = pm.sample(1000, tune=500, step=pm.Metropolis(), return_inferencedata=False, progressbar=True)

    p_A_samples = trace['p_A']
    p_B_samples = trace['p_B']
    delta_samples = trace['delta']

    cred_interval = np.percentile(delta_samples, [2.5, 97.5])
    prob = np.mean(delta_samples > 0)

    return {
        #'p_A_samples': p_A_samples.tolist(),
        #'p_B_samples': p_B_samples.tolist(),
        #'delta_samples': delta_samples.tolist(),
        'cred_interval': cred_interval.tolist(),
        'prob': prob
    }
