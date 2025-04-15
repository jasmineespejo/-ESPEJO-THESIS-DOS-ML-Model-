import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb

from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

def load_pca_transformed_data(filepath):
    try:
        # Read the data from the txt file
        pca_data = pd.read_csv(filepath, sep='\t')

        return pca_data
    
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None, None
    
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

def adsorption_energy_for_dataset(pca_data):

    all_adsorption_energy = pd.read_excel('Adsorption_energies_additives.xlsx')

    merged_data_df = pca_data.merge(all_adsorption_energy, left_on='Molecule', right_on='System', how='left')
    merged_data_df = merged_data_df.drop(columns=['System'])
    merged_data_df = merged_data_df.dropna(subset=['Ads.'])

    return merged_data_df 

def perform_xgboost(transformed_data_dir, filename):
    filepath = os.path.join(transformed_data_dir, filename)

    # Load and process the data
    pca_data = load_pca_transformed_data(filepath)
    merged_data = adsorption_energy_for_dataset(pca_data)

    # Prepare the data
    x = merged_data.drop(columns=['Molecule','Ads.'])
    y = merged_data['Ads.']

    # Split the data
    x_train, x_test, y_train, y_test = train_test_split(x, y,test_size=0.2, random_state=42)

    ## Train the XGBoost Model

    # Initialize and fit the model
    xgb_model = xgb.XGBRegressor(
        objective="reg:squarederror",   # Regression task
        n_estimators=500,               # Number of boosting rounds
        learning_rate=0.05,             # Step size shrinkage
        max_depth=6,                    # Maximum tree depth
        subsample=0.8,                  # Fraction of data used for training
        colsample_bytree=0.8,           # Fraction of features used per tree
        random_state=42
    )
    
    xgb_model.fit(x_train, y_train)

    ## Make predictions and evaluate the model

    # Predictions
    y_pred = xgb_model.predict(x_test) 

    return x_train, x_test, y_train, y_test, y_pred

def plot_xgb_results(y_test, y_pred, energy_range, variance):
    # Extract sample indices from the first column of y_test (if it's a DataFrame)
    y_actual = y_test.values

    # Calculate axis limits for equal scaling
    min_val = min(y_actual.min(), y_pred.min()) - 0.2
    max_val = max(y_actual.max(), y_pred.max()) + 0.2

    # Plot actual vs predicted with y=x line
    plt.figure(figsize=(8, 8))
    plt.plot(y_actual, y_pred, 'o', markersize=6, label='Predictions')
    plt.plot([min_val, max_val], [min_val, max_val], 'r-', label='$y = x$', linewidth=2)  # y=x line

    plt.xlabel('Actual Adsorption Energy')
    plt.ylabel('Predicted Adsorption Energy')
    plt.title(f'Actual vs Predicted Adsorption Energy for {energy_range} and {variance * 100}% variance')
    plt.legend()
    plt.xlim(min_val, max_val)
    plt.ylim(min_val, max_val)
    plt.grid(True)
    plt.show()

def obtain_xgb_evaluations(x_train, y_test, y_pred):
    # Evaluation
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    # Number of samples and predictors
    n = len(y_test)  # number of data points
    p = x_train.shape[1]  # number of predictors (features)

    # Calculate Adjusted R-squared
    adjusted_r2 = 1 - ((1 - r2) * (n - 1)) / (n - p - 1)

    return mae, mse, rmse, r2, adjusted_r2