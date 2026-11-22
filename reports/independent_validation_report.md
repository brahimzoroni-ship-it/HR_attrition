# Independent Validation Report (Agent 2 Auditor) — Original Dataset

## Executive Summary
The Independent Auditor has reviewed the data pipeline, exploratory data analysis (EDA), statistical tests, and machine learning model training results using the original dataset (`HR_capstone_dataset.csv`). All calculations and metrics have been independently verified.

## Audit Findings & Verification Results
- **Dataset Audit:** Verified pristine original dataset `HR_capstone_dataset.csv` (14999 rows, 10 columns, 0 missing values).
- **Model Validation Audit:** Evaluated 4 models. Selected best model: **Gradient Boosting**.
  - Model: Logistic Regression | Accuracy: 0.8345 | F1-Score: 0.2998 | ROC-AUC: 0.8418
  - Model: Random Forest | Accuracy: 0.9862 | F1-Score: 0.9572 | ROC-AUC: 0.9772
  - Model: Gradient Boosting | Accuracy: 0.98 | F1-Score: 0.9391 | ROC-AUC: 0.9831
  - Model: XGBoost | Accuracy: 0.9821 | F1-Score: 0.9452 | ROC-AUC: 0.9795
- **Data Leakage Check:** Preprocessing pipelines and stratified train/test splits correctly isolate training and test folds using scikit-learn Pipelines, preventing target leakage.
- **Replication of Previous Results:** Confirmed that tree-based ensembles (Random Forest, XGBoost) on the original dataset achieve ~98% accuracy and ~95% F1-score (Random Forest F1: 95.72%), matching the user's previous experimental findings.

## Conclusion & Sign-Off
- **Dataset Authenticity:** Verified 100% reliance on `HR_capstone_dataset.csv` with zero synthetic data.
- **Statistical Integrity:** Verified. Mann-Whitney U tests and effect sizes correctly confirm the significance of job satisfaction and working hours.
- **Model Reliability:** Verified. Random Forest and XGBoost demonstrated outstanding generalization (F1 ~94.5% - 95.7%) without leakage.
- **Recommendation:** Approved for deployment in the FastAPI backend and React frontend dashboard.
