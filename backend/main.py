import os
import json
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="HR Attrition Intelligence Platform API (Original Dataset)",
    version="2.0.0",
    description="Backend API powered by pristine HR_capstone_dataset.csv for Attrition Analysis, EDA, ML Models, and Predictions."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = 'HR_capstone_dataset.csv'
MODEL_PATH = 'models/best_model.pkl'

model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

@app.get("/")
def read_root():
    return {
        "status": "online",
        "platform": "HR Attrition Intelligence Platform",
        "dataset": "HR_capstone_dataset.csv",
        "version": "2.0.0"
    }

@app.get("/api/executive-summary")
def get_executive_summary():
    df = pd.read_csv(DATA_PATH).drop_duplicates()
    total_employees = int(len(df))
    attrition_rate = float(df['left'].mean())
    left_count = int(df['left'].sum())
    avg_satisfaction = float(df['satisfaction_level'].mean())
    
    return {
        "total_employees": total_employees,
        "attrition_rate": round(attrition_rate, 4),
        "departed_employees": left_count,
        "average_satisfaction": round(avg_satisfaction, 2),
        "key_findings": [
            "Employees leaving exhibit significantly lower job satisfaction (0.44 vs 0.67, p < 0.0001).",
            "Salary tier is a major driver: low salary employees face 20.45% attrition compared to 4.85% for high salary tier.",
            "Tenure at 3-5 years represents peak vulnerability for employee departure."
        ],
        "business_recommendations": [
            "Establish regular feedback loops and career progression milestones for employees reaching 3 years of tenure.",
            "Review compensation frameworks for low-salary tier staff in technical and sales departments.",
            "Monitor workload and working hours to prevent burnout among high-performing staff."
        ]
    }

@app.get("/api/hr-analytics")
def get_hr_analytics():
    df = pd.read_csv(DATA_PATH).drop_duplicates()
    
    dept_stats = df.groupby('Department')['left'].agg(['count', 'mean']).reset_index()
    dept_stats.columns = ['department', 'total', 'attrition_rate']
    dept_stats['attrition_rate'] = dept_stats['attrition_rate'].round(4)
    
    salary_stats = df.groupby('salary')['left'].agg(['count', 'mean']).reset_index()
    salary_stats.columns = ['salary', 'total', 'attrition_rate']
    salary_stats['attrition_rate'] = salary_stats['attrition_rate'].round(4)
    
    return {
        "department_analysis": dept_stats.to_dict(orient='records'),
        "salary_analysis": salary_stats.to_dict(orient='records')
    }

@app.get("/api/data-scientist-metrics")
def get_ds_metrics():
    eval_path = 'reports/model_evaluation.json'
    if os.path.exists(eval_path):
        with open(eval_path, 'r') as f:
            return json.load(f)
    return {"error": "Model evaluation report not found"}

class EmployeeInput(BaseModel):
    satisfaction_level: float
    last_evaluation: float
    number_project: int
    average_montly_hours: int
    time_spend_company: int
    Work_accident: int
    promotion_last_5years: int
    Department: str
    salary: str

@app.post("/api/predict")
def predict_attrition(employee: EmployeeInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
        
    input_df = pd.DataFrame([employee.model_dump()])
    prob_leave = float(model.predict_proba(input_df)[0][1])
    prob_stay = float(1.0 - prob_leave)
    prediction = int(model.predict(input_df)[0])
    
    factors = []
    if employee.satisfaction_level < 0.5:
        factors.append({"factor": "Low Satisfaction Level", "impact": "High Risk", "value": employee.satisfaction_level})
    else:
        factors.append({"factor": "Healthy Satisfaction Level", "impact": "Protective", "value": employee.satisfaction_level})
        
    if employee.average_montly_hours > 220:
        factors.append({"factor": "High Monthly Hours (Burnout Risk)", "impact": "High Risk", "value": employee.average_montly_hours})
    else:
        factors.append({"factor": "Balanced Monthly Hours", "impact": "Protective", "value": employee.average_montly_hours})
        
    if employee.salary == 'low':
        factors.append({"factor": "Low Salary Tier", "impact": "High Risk", "value": employee.salary})
    elif employee.salary == 'high':
        factors.append({"factor": "High Salary Tier", "impact": "Protective", "value": employee.salary})
        
    if 3 <= employee.time_spend_company <= 5:
        factors.append({"factor": "Critical Tenure Milestone (3-5 Years)", "impact": "Moderate Risk", "value": employee.time_spend_company})
        
    if employee.promotion_last_5years == 0:
        factors.append({"factor": "No Promotion in Last 5 Years", "impact": "Moderate Risk", "value": 0})
    else:
        factors.append({"factor": "Recent Promotion Received", "impact": "Protective", "value": 1})

    return {
        "prediction": "Leave" if prediction == 1 else "Stay",
        "probability_leave": round(prob_leave, 4),
        "probability_stay": round(prob_stay, 4),
        "risk_percentage": round(prob_leave * 100, 2),
        "contributing_factors": factors
    }
