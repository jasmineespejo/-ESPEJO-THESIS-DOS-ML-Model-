# Machine Learning Model for Predicting Adsorption Energy

## Overview

This repository contains code and resources for building a machine learning (ML) model to predict the adsorption energy of various adsorbates on zinc surfaces. 
The goal is to optimise electrolyte additives in zinc-ion batteries to prevent corrosion and improve anode stability.

## Thesis Objectives
- Extract and preprocess DOS data from DFT-calculated DOSCAR files.
- Apply dimensionality reduction techniques (e.g., PCA) to transform high-dimensional DOS data.
- Train regression models (Random Forest, XGBoost, etc.) to predict adsorption energy.
- Evaluate and interpret model performance to identify promising molecular additives.

## Project Structure
```text
ESPEJO-THESIS-DOS-ML-Model-/
├── .venv                          # Python virtual environment
├── DOSCAR_Files/                  # Parsed DOSCARs ready for ML
├── DOSCAR_Files_Initial/          # Parsed DOSCARs of smaller dataset ready for ML
├── RESULTS/                       # Model outputs, reports, figures
├── SCRIPTS_DOSCAR_Separation/     # DOSCAR parsing & feature extraction
├── SCRIPTS_PCA/                   # PCA dimensionality-reduction scripts
├── SCRIPTS_RANDOM_FOREST/         # Random Forest training & eval  
├── SCRIPTS_XGBOOST/               # XGBoost training & eval  
├── .gitattributes                 # Git attributes (EOL, diff rules, etc.)
└── README.md                      # This file
```
## Installation

To set up the environment for this project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/jasmineespejo/-ESPEJO-THESIS-DOS-ML-Model-.git
    ```

2. Create and activate virtual environment
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate      # macOS/Linux
    .\.venv\Scripts\activate       # Windows PowerShell
    ```

3. Install dependencies
    ```bash
    pip install numpy scipy pandas scikit-learn xgboost matplotlib seaborn
    ```

## Usage

1. DOSCAR Separation 
Parse raw DOSCAR files into a sizable matrix for PCA-reduction

    ```bash
    ./SCRIPTS_DOSCAR_Separation/sp__run.sh
    ```

2. PCA Analysis
Perform PCA on DOS features to reduce dimensionality.
- Workflow laid out in jupiter notebook 'SCRIPTS_PCA/x_PCA_perform multiple.ipynb'

3. Random Forest Modelling
Train and evaluate a Random Forest regressor on PCA-features DOS data.
- Workflow laiD out in jupiter notebook 'SCRIPTS_RANDOM_FOREST/x_RANDOM_FOREST.ipynb'

4. XGBoost Modelling
Train and evaluate an XGBoost regressor as an alternative.
- Workflow laiD out in jupiter notebook 'SCRIPTS_XGBOOST/x_XGBOOST.ipynb'

## Acknowledgements
Raw DOSCAR data was obtained from the UNSW Zinc Anode Research Team, specifically provided through DFT calculations conducted by Ravindra Kokate.

## Contact

For any questions or inquiries, please contact Jasmine Eliza Bernabe Espejo at z5256944@ad.unsw.edu.au
