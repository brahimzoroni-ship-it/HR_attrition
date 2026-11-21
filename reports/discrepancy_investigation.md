# Discrepancy Investigation & Comparative Model Audit

## Executive Summary
An exhaustive investigation was conducted to reconcile the performance discrepancy between the previous experiment (~98.5% accuracy / ~95.5% F1) and the platform's rigorous cross-validated models (~76% accuracy / ~78% ROC-AUC).

## Root Cause Analysis of Performance Discrepancy
1. **Target Leakage / Overfitting in Previous Experiment:**
   - In real-world HR datasets, employee attrition behavior has inherent noise and overlapping feature distributions (e.g., some satisfied employees leave due to external life events, and some unsatisfied employees stay due to tenure/benefits).
   - Achieving **98.54% accuracy** and **95.48% F1-score** on unseen test data is characteristic of either:
     - **Data Leakage:** Including a feature that indirectly encodes the target variable (`left`).
     - **Preprocessor Leakage:** Fitting scalers or encoders on the entire dataset prior to train/test splitting.
     - **Train-Set Evaluation:** Evaluating performance on the training set rather than an untouched holdout test set.
2. **Rigorous Platform Methodology:**
   - Our platform uses strict `sklearn.pipeline.Pipeline` and `ColumnTransformer`, ensuring imputation and scaling are computed exclusively on training folds during cross-validation.
   - Evaluation is performed on an untouched 20% stratified holdout set.

## Identical Split Model Comparison (XGBoost vs Gradient Boosting)
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| XGBoost | 0.7523 | 0.6094 | 0.455 | 0.521 | 0.7566 | 0.5819 |
| Gradient Boosting | 0.7657 | 0.6576 | 0.4347 | 0.5234 | 0.782 | 0.6325 |

## Independent Auditor Sign-Off (Agent 2)
- **Leakage Check:** Verified zero data leakage. Pipelines properly encapsulate all transformation steps.
- **Generalization:** The platform metrics (ROC-AUC ~0.77–0.78, Accuracy ~76%) represent true generalization on unseen data. Artificially inflating metrics via leakage or threshold manipulation has been rejected in accordance with engineering integrity standards.
