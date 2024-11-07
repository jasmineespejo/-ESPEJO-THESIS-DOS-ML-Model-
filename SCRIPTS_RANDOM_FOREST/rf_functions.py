import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
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

def adsorption_energy_for_dataset(pca_data, all_adsorption_energy):
    merged_data_df = pca_data.merge(all_adsorption_energy, left_on='Molecule', right_on='System', how='left')
    merged_data_df = merged_data_df.drop(columns=['System'])
    merged_data_df = merged_data_df.dropna(subset=['Ads.'])

    return merged_data_df

def perform_random_forest(merged_data_df):
    # Prepare the data
    x = merged_data_df.drop(columns=['Molecule','Ads.'])
    y = merged_data_df['Ads.']

    # Split the data

    x_train, x_test, y_train, y_test = train_test_split(x, y,test_size=0.2, random_state=42)

    ## Train the Random Forest Model

    # Initialize and fit the model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(x_train, y_train)

    ## Make predictions and evaluate the model

    # Predictions
    y_pred = rf_model.predict(x_test)

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