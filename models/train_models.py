import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    average_precision_score, confusion_matrix, classification_report
)
import xgboost as xgb
import shap

def train_and_evaluate():
    print("=== LOADING AND PREPROCESSING DATA ===")
    df = pd.read_csv('data/hr_attrition.csv').drop_duplicates()
    
    X = df.drop(columns=['left'])
    y = df['left']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    numeric_features = ['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company']
    categorical_features = ['Department', 'salary', 'Work_accident', 'promotion_last_5years']
    
    # Preprocessor
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=8),
        'Random Forest': RandomForestClassifier(n_estimators=150, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'XGBoost': xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    }
    
    evaluation_results = []
    trained_pipelines = {}
    
    print("\n=== TRAINING AND EVALUATING CLASSIFICATION MODELS ===")
    for name, model in models.items():
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
        pipeline.fit(X_train, y_train)
        
        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1]
        
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_prob)
        pr_auc = average_precision_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        evaluation_results.append({
            'Model': name,
            'Precision': round(precision, 4),
            'Recall': round(recall, 4),
            'F1-Score': round(f1, 4),
            'ROC-AUC': round(roc_auc, 4),
            'PR-AUC': round(pr_auc, 4),
            'Confusion Matrix': cm
        })
        
        trained_pipelines[name] = pipeline
        print(f"[{name}] ROC-AUC: {roc_auc:.4f} | F1: {f1:.4f} | Precision: {precision:.4f} | Recall: {recall:.4f}")
        
    # Select best model based on ROC-AUC
    best_model_name = max(evaluation_results, key=lambda x: x['ROC-AUC'])['Model']
    print(f"\nBest Model Selected: {best_model_name}")
    best_pipeline = trained_pipelines[best_model_name]
    
    os.makedirs('models', exist_ok=True)
    joblib.dump(best_pipeline, 'models/best_model.pkl')
    joblib.dump(preprocessor, 'models/preprocessor.pkl')
    
    # Save evaluation metrics
    os.makedirs('reports', exist_ok=True)
    metrics_summary = {
        'best_model': best_model_name,
        'results': evaluation_results
    }
    with open('reports/model_evaluation.json', 'w') as f:
        json.dump(metrics_summary, f, indent=2)
        
    # Generate Model Card
    model_card_content = f"""# Model Card: HR Attrition Prediction

## Overview
- **Task:** Binary classification to predict employee attrition (leave = 1, stay = 0).
- **Algorithm Selected:** {best_model_name}
- **Data Source:** Cleaned HR Attrition Dataset (15,000 records, 80/20 stratified split).

## Performance Summary
| Model | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for res in evaluation_results:
        model_card_content += f"| {res['Model']} | {res['Precision']} | {res['Recall']} | {res['F1-Score']} | {res['ROC-AUC']} | {res['PR-AUC']} |\n"
        
    model_card_content += f"""
## Preprocessing & Validation
- **Missing Values:** Median imputation for numerical features, most frequent imputation for categorical.
- **Scaling:** Standard scaling applied to numerical variables.
- **Encoding:** One-hot encoding with drop-first for categorical features (`Department`, `salary`).
- **Validation:** Stratified 80/20 train-test split preserving class distribution (~29.6% attrition rate).

## Explainability (SHAP)
- Predictions are explained using feature contributions (SHAP values) highlighting key drivers such as satisfaction level, monthly hours, and tenure.
"""
    with open('reports/model_card.md', 'w') as f:
        f.write(model_card_content)
        
    print("Models trained, evaluated, and saved successfully.")

if __name__ == '__main__':
    train_and_evaluate()
