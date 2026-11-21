# Model Card: HR Attrition Prediction (Optimized Pipeline)

## Overview
- **Task:** Binary classification to predict employee attrition (leave = 1, stay = 0).
- **Algorithm Selected:** Optimized Gradient Boosting (with advanced feature engineering & optimal decision threshold).
- **Data Source:** Cleaned HR Attrition Dataset (15,000 records, 80/20 stratified split, zero data leakage).

## Performance Summary (Optimized Models)
| Model | Optimal Threshold | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Optimized XGBoost** | 0.40 | 71.60% | 51.46% | 71.28% | 59.77% | 0.7778 | 0.6188 |
| **Optimized Gradient Boosting** | 0.26 | 71.10% | 50.84% | 71.85% | 59.54% | 0.7789 | 0.6213 |

## Advanced Feature Engineering
- `hours_per_project`: Ratio of monthly working hours to assigned projects.
- `sat_eval_diff`: Discrepancy between satisfaction level and performance evaluation.
- `burnout_risk`: Flag for excessive hours (>220) and high projects (>=5).
- `under_challenged`: Flag for low hours (<140) and low projects (<=2).
- `tenure_sq`: Squared tenure term for non-linear career milestone risk.

## Preprocessing & Validation
- **Missing Values:** Median imputation for numerical features, most frequent imputation for categorical.
- **Scaling:** Standard scaling applied to numerical variables.
- **Encoding:** One-hot encoding with drop-first for categorical features.
- **Validation:** Stratified 80/20 train-test split preserving class distribution (~29.6% attrition rate). Threshold optimized out-of-fold to maximize F1-score.
