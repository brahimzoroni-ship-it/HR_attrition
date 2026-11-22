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

def investigate_leakage():
    print("=== INVESTIGATING PREVIOUS 95.48% F1 RESULT (DUPLICATE LEAKAGE HYPOTHESIS) ===")
    df_raw = pd.read_csv('HR_capstone_dataset.csv')
    
    # --- EXPERIMENT 1: Train-test split on RAW data (WITH duplicates) ---
    print("\n[Experiment 1] Train-test split WITHOUT dropping duplicates (Data Leakage)")
    X_raw = df_raw.drop(columns=['left'])
    y_raw = df_raw['left']
    
    X_tr1, X_te1, y_tr1, y_te1 = train_test_split(
        X_raw, y_raw, test_size=0.2, random_state=42, stratify=y_raw
    )
    
    num_feat = ['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company']
    cat_feat = ['Department', 'salary', 'Work_accident', 'promotion_last_5years']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), num_feat),
            ('cat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))]), cat_feat)
        ]
    )
    
    xgb1 = xgb.XGBClassifier(n_estimators=200, max_depth=5, random_state=42)
    pipe1 = Pipeline([('preprocessor', preprocessor), ('classifier', xgb1)])
    pipe1.fit(X_tr1, y_tr1)
    
    y_pred1 = pipe1.predict(X_te1)
    y_prob1 = pipe1.predict_proba(X_te1)[:, 1]
    
    print(f"Accuracy:  {accuracy_score(y_te1, y_pred1):.4f}")
    print(f"Precision: {precision_score(y_te1, y_pred1, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_te1, y_pred1, zero_division=0):.4f}")
    print(f"F1-score:  {f1_score(y_te1, y_pred1, zero_division=0):.4f}")
    print(f"ROC-AUC:   {roc_auc_score(y_te1, y_prob1):.4f}")
    
    # --- EXPERIMENT 2: Train-test split AFTER dropping duplicates (Clean holdout) ---
    print("\n[Experiment 2] Train-test split AFTER dropping duplicates (No Leakage)")
    df_clean = df_raw.drop_duplicates().copy()
    X_clean = df_clean.drop(columns=['left'])
    y_clean = df_clean['left']
    
    X_tr2, X_te2, y_tr2, y_te2 = train_test_split(
        X_clean, y_clean, test_size=0.2, random_state=42, stratify=y_clean
    )
    
    xgb2 = xgb.XGBClassifier(n_estimators=200, max_depth=5, random_state=42)
    pipe2 = Pipeline([('preprocessor', preprocessor), ('classifier', xgb2)])
    pipe2.fit(X_tr2, y_tr2)
    
    y_pred2 = pipe2.predict(X_te2)
    y_prob2 = pipe2.predict_proba(X_te2)[:, 1]
    
    print(f"Accuracy:  {accuracy_score(y_te2, y_pred2):.4f}")
    print(f"Precision: {precision_score(y_te2, y_pred2, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_te2, y_pred2, zero_division=0):.4f}")
    print(f"F1-score:  {f1_score(y_te2, y_pred2, zero_division=0):.4f}")
    print(f"ROC-AUC:   {roc_auc_score(y_te2, y_prob2):.4f}")

if __name__ == '__main__':
    investigate_leakage()
