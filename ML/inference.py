import pandas as pd
import numpy as np
import scipy.stats
import joblib

# Load the saved model and lambdas
import os
model_path = os.path.join(os.path.dirname(__file__), 'best_model.pkl')
lambdas_path = os.path.join(os.path.dirname(__file__), 'boxcox_lambdas.pkl')
model = joblib.load(model_path)
lambdas = joblib.load(lambdas_path)

def preprocess_single_data(data):
    """
    Preprocess a single data point.
    data: dict with keys: 'ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity'
    """
    # Convert to DataFrame
    df = pd.DataFrame([data])

    # Fill nulls if any (though for single data, assume complete)
    # For simplicity, assume no nulls

    # Apply boxcox transformations
    features_to_transform = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']

    for feature in features_to_transform:
        if feature in df.columns:
            df[feature] = scipy.stats.boxcox(df[feature], lmbda=lambdas[feature])

    return df

def predict_potability(data):
    """
    Predict if water is potable.
    data: dict of features
    Returns: 0 (not potable) or 1 (potable)
    """
    processed_data = preprocess_single_data(data)
    prediction = model.predict(processed_data)
    return int(prediction[0])

# Example usage
if __name__ == "__main__":
    # Example data (replace with actual values)
    sample_data = {
        'ph': 7.0,
        'Hardness': 200.0,
        'Solids': 20000.0,
        'Chloramines': 3.0,
        'Sulfate': 300.0,
        'Conductivity': 400.0,
        'Organic_carbon': 10.0,
        'Trihalomethanes': 50.0,
        'Turbidity': 3.0
    }

    result = predict_potability(sample_data)
    print(f"Prediction: {'Potable' if result == 1 else 'Not Potable'}")