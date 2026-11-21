# Model Card: HR Attrition Prediction

## Overview
- **Task:** Binary classification to predict employee attrition (leave = 1, stay = 0).
- **Algorithm Selected:** Gradient Boosting
- **Data Source:** Cleaned HR Attrition Dataset (15,000 records, 80/20 stratified split).

## Performance Summary
| Model | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Logistic Regression | 0.6318 | 0.3941 | 0.4854 | 0.7584 | 0.5841 |
| Decision Tree | 0.6299 | 0.3795 | 0.4736 | 0.7429 | 0.5599 |
| Random Forest | 0.6475 | 0.4178 | 0.5079 | 0.7553 | 0.5982 |
| Gradient Boosting | 0.6576 | 0.4347 | 0.5234 | 0.782 | 0.6325 |
| XGBoost | 0.6094 | 0.455 | 0.521 | 0.7566 | 0.5819 |

## Preprocessing & Validation
- **Missing Values:** Median imputation for numerical features, most frequent imputation for categorical.
- **Scaling:** Standard scaling applied to numerical variables.
- **Encoding:** One-hot encoding with drop-first for categorical features (`Department`, `salary`).
- **Validation:** Stratified 80/20 train-test split preserving class distribution (~29.6% attrition rate).

## Explainability (SHAP)
- Predictions are explained using feature contributions (SHAP values) highlighting key drivers such as satisfaction level, monthly hours, and tenure.
