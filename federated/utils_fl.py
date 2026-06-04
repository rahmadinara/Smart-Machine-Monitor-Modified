import numpy as np

def federated_average(models):
    """Average parameters from multiple models"""
    avg_model = {}

    for key in models[0].keys():
        avg_model[key] = np.mean([m[key] for m in models], axis=0)

    return avg_model