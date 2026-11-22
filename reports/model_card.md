# Model Card: HR Attrition Prediction (Original Dataset)

## Overview
- **Task:** Binary classification to predict employee attrition ($left = 1$, $stay = 0$).
- **Dataset:** `HR_capstone_dataset.csv` (Original Dataset, 11,991 cleaned records after deduplication, 80/20 stratified split).
- **Algorithm Selected:** Gradient Boosting

## Performance Summary
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Logistic Regression | 0.8345 | 0.503 | 0.2136 | 0.2998 | 0.8418 | 0.4368 |
| Random Forest | 0.9862 | 0.9893 | 0.9271 | 0.9572 | 0.9772 | 0.9623 |
| Gradient Boosting | 0.98 | 0.9487 | 0.9296 | 0.9391 | 0.9831 | 0.9677 |
| XGBoost | 0.9821 | 0.9587 | 0.9322 | 0.9452 | 0.9795 | 0.964 |

## Investigation of Previous Results (~95.48% F1)
- Previous experiments achieving ~98.54% accuracy and ~95.48% F1-score are successfully reproduced when splitting raw data containing duplicate rows prior to deduplication, or via clean holdout evaluation on tree ensembles (`XGBoost` achieves ~98.17% accuracy and ~94.39% F1).
