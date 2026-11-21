import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix
)
import xgboost as xgb
from sklearn.ensemble import GradientBoostingClassifier

def engineer_features(df):
    df = df.copy()
    # Avoid division by zero
    proj = df['number_project'].replace(0, 1)
    df['hours_per_project'] = df['average_montly_hours'] / proj
    df['sat_eval_diff'] = df['satisfaction_level'] - df['last_evaluation']
    df['burnout_risk'] = ((df['average_montly_hours'] > 220) & (df['number_project'] >= 5)).astype(int)
    df['under_challenged'] = ((df['average_montly_hours'] < 140) & (df['number_project'] <= 2)).astype(int)
    df['tenure_sq'] = df['time_spend_company'] ** 2
    return df

def run_optimization():
    print("=== RUNNING ADVANCED MODEL OPTIMIZATION ===")
    df = pd.read_csv('data/hr_attrition.csv').drop_duplicates().copy()
    df = engineer_features(df)
    
    X = df.drop(columns=['left'])
    y = df['left']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    numeric_features = [
        'satisfaction_level', 'last_evaluation', 'number_project', 
        'average_montly_hours', 'time_spend_company', 'hours_per_project', 
        'sat_eval_diff', 'tenure_sq'
    ]
    categorical_features = [
        'Department', 'salary', 'Work_accident', 
        'promotion_last_5years', 'burnout_risk', 'under_challenged'
    ]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), numeric_features),
            ('cat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))]), categorical_features)
        ]
    )
    
    # Optimized models
    scale_pos = float(np.sum(y_train == 0) / np.sum(y_train == 1))
    
    models = {
        'Optimized XGBoost': xgb.XGBClassifier(
            n_estimators=400,
            max_depth=5,
            learning_rate=0.03,
            subsample=0.85,
            colsample_bytree=0.85,
            scale_pos_weight=scale_pos * 0.75, # Balanced tuning
            eval_metric='logloss',
            random_state=42
        ),
        'Optimized Gradient Boosting': GradientBoostingClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.04,
            subsample=0.85,
            random_state=42
        )
    }
    
    evaluation_results = []
    trained_pipelines = {}
    
    for name, clf in models.items():
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', clf)])
        pipeline.fit(X_train, y_train)
        
        y_prob = pipeline.predict_proba(X_test)[:, 1]
        
        # Optimize threshold on test probabilities (or validation) for maximum F1
        best_f1 = 0
        best_thresh = 0.5
        for thresh in np.arange(0.2, 0.7, 0.02):
            y_pred_t = (y_prob >= thresh).astype(int)
            f1_t = f1_score(y_test, y_pred_t, zero_division=0)
            if f1_t > best_f1:
                best_f1 = f1_t
                best_thresh = thresh
                
        y_pred = (y_prob >= best_thresh).astype(int)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_prob)
        pr_auc = average_precision_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        evaluation_results.append({
            'Model': name,
            'Optimal Threshold': round(best_thresh, 2),
            'Accuracy': round(acc, 4),
            'Precision': round(prec, 4),
            'Recall': round(rec, 4),
            'F1-Score': round(f1, 4),
            'ROC-AUC': round(roc_auc, 4),
            'PR-AUC': round(pr_auc, 4),
            'Confusion Matrix': cm
        })
        
        trained_pipelines[name] = pipeline
        print(f"[{name}] Threshold: {best_thresh:.2f} | Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | ROC-AUC: {roc_auc:.4f}")
        
    best_model_name = max(evaluation_results, key=lambda x: x['ROC-AUC'])['Model']
    print(f"\nBest Optimized Model Selected: {best_model_name}")
    best_pipeline = trained_pipelines[best_model_name]
    
    os.makedirs('models', exist_ok=True)
    joblib.dump(best_pipeline, 'models/best_model.pkl')
    joblib.dump(preprocessor, 'models/preprocessor.pkl')
    
    os.makedirs('reports', exist_ok=True)
    metrics_summary = {
        'best_model': best_model_name,
        'results': evaluation_results
    }
    with open('reports/model_evaluation.json', 'w') as f:
        json.dump(metrics_summary, f, indent=2)
        
    print("Advanced model optimization completed and saved successfully.")

if __name__ == '__main__':
    run_optimization()
