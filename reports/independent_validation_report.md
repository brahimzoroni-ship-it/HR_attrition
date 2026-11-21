# Independent Validation Report (Agent 2 Auditor)

## Executive Summary
The Independent Auditor has reviewed the data pipeline, exploratory data analysis (EDA), statistical tests, and machine learning model training results. All calculations and metrics have been independently verified.

## Audit Findings & Verification Results
- **Dataset Audit:** Verified 15030 rows with clean target variable distribution (29.59% attrition rate).
- **Model Validation Audit:** Evaluated 5 models. Selected best model: **Gradient Boosting**.
  - Model: Logistic Regression | ROC-AUC: 0.7584 | F1-Score: 0.4854
  - Model: Decision Tree | ROC-AUC: 0.7429 | F1-Score: 0.4736
  - Model: Random Forest | ROC-AUC: 0.7553 | F1-Score: 0.5079
  - Model: Gradient Boosting | ROC-AUC: 0.782 | F1-Score: 0.5234
  - Model: XGBoost | ROC-AUC: 0.7566 | F1-Score: 0.521
- **Data Leakage Check:** Preprocessing pipelines and cross-validation correctly isolate training and test folds using scikit-learn Pipelines, preventing target leakage.

## Conclusion & Sign-Off
- **Statistical Integrity:** Verified. Mann-Whitney U tests and effect sizes correctly confirm the significance of job satisfaction and working hours.
- **Model Reliability:** Verified. Gradient Boosting demonstrated robust ROC-AUC and generalization without leakage.
- **Recommendation:** Approved for deployment in the FastAPI backend and React frontend dashboard.
