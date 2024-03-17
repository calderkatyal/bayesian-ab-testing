import pymc3 as pm
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from flask import current_app

def perform_bayesian_analysis(data):
    try:
        with pm.Model() as model:
            p_A = pm.Beta('p_A', alpha=data['alphaA'], beta=data['betaA'])
            p_B = pm.Beta('p_B', alpha=data['alphaB'], beta=data['betaB'])
            obs_A = pm.Binomial('obs_A', n=data['trialsA'], p=p_A, observed=data['successesA'])
            obs_B = pm.Binomial('obs_B', n=data['trialsB'], p=p_B, observed=data['successesB'])
            numDraws = data['numDraws']
            numTuningSteps = data['numTuningSteps']
            trace = pm.sample(numDraws, tune=numTuningSteps, step=pm.Metropolis())
            
        p_A_samples = trace['p_A']
        p_B_samples = trace['p_B']
        prob_B_better_than_A = np.mean(p_B_samples > p_A_samples)
        
        return {
            'p_A_samples': trace['p_A'].tolist(),
            'p_B_samples': trace['p_B'].tolist(),
            'prob_B_better_than_A': prob_B_better_than_A
            
        }
        
    except Exception as e:
        current_app.logger.error(f"Error in Bayesian analysis: {e}")
        return None

def create_histogram(p_A_samples, p_B_samples):
    try:
        plt.figure()
        plt.hist(p_A_samples, bins=30, alpha=0.5, label='p_A', color='red')
        plt.hist(p_B_samples, bins=30, alpha=0.5, label='p_B', color='blue')
        plt.legend()
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        #add confidence interval lines
        plt.axvline(x=np.percentile(p_A_samples, 2.5), color='red', linestyle='--')
        plt.axvline(x=np.percentile(p_A_samples, 97.5), color='red', linestyle='--')
        plt.axvline(x=np.percentile(p_B_samples, 2.5), color='blue', linestyle='--')
        plt.axvline(x=np.percentile(p_B_samples, 97.5), color='blue', linestyle='--')
        plt.title('Posterior distributions of p_A and p_B')
        plt.grid(True)
        
        # Ensure the static directory exists
        static_dir = os.path.join(current_app.root_path, 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)

        # Path for the plot
        plot_path = os.path.join(static_dir, 'histogram.png')

        # Save the figure
        plt.savefig(plot_path)
        plt.close()

        # Return the relative path to the saved image
        return 'histogram.png'
    except Exception as e:
        current_app.logger.error(f"Error creating histogram: {e}")
        return None