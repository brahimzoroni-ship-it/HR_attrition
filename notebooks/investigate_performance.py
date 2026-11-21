import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix
)
import xgboost as xgb

def investigate():
    print("=== INVESTIGATING XGBOOST PERFORMANCE DISCREPANCY ===")
    df = pd.read_csv('data/hr_attrition.csv').drop_duplicates().copy()
    
    # Feature Engineering
    df['overworked'] = ((df['average_montly_hours'] > 220) & (df['number_project'] >= 5)).astype(int)
    df['underchallenged'] = ((df['average_montly_hours'] < 140) & (df['number_project'] <= 2)).astype(int)
    df['sat_x_eval'] = df['satisfaction_level'] * df['last_evaluation']
    df['tenure_risk'] = ((df['time_spend_company'] >= 3) & (df['time_spend_company'] <= 5)).astype(int)
    
    X = df.drop(columns=['left'])
    y = df['left']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    numeric_features = ['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company', 'sat_x_eval']
    categorical_features = ['Department', 'salary', 'Work_accident', 'promotion_last_5years', 'overworked', 'underchallenged', 'tenure_risk']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), numeric_features),
            ('cat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))]), categorical_features)
        ]
    )
    
    # Train XGBoost with tuned hyperparameters
    xgb_model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=1.0,
        eval_metric='logloss',
        random_state=42
    )
    
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', xgb_model)])
    pipeline.fit(X_train, y_train)
    
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    
    # Try different thresholds to see if 95%+ F1 / Precision can be achieved naturally
    print("\n--- Threshold Tuning Experiment ---")
    best_f1 = 0
    best_thresh = 0.5
    for thresh in np.arange(0.1, 0.9, 0.05):
        y_pred_t = (y_prob >= thresh).astype(int)
        acc = accuracy_score(y_test, y_pred_t)
        prec = precision_score(y_test, y_pred_t, zero_division=0)
        rec = recall_score(y_test, y_pred_t, zero_division=0)
        f1 = f1_score(y_test, y_pred_t, zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_thresh = thresh
        print(f"Threshold {thresh:.2f} | Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f}")
        
    print(f"\nBest Threshold: {best_thresh:.2f} with F1: {best_f1:.4f}")
    
    # Default 0.5 evaluation
    y_pred = (y_prob >= 0.5).astype(int)
    print("\n[Default 0.5 Threshold Results]")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"Recall: {recall_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"F1-score: {f1_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")
    print(f"PR-AUC: {average_precision_score(y_test, y_prob):.4f}")
    print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

if __name__ == '__main__':
    investigate()
