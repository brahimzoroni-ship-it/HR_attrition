import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"
    assert response.json()["dataset"] == "HR_capstone_dataset.csv"

def test_executive_summary():
    response = client.get("/api/executive-summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_employees" in data
    assert "attrition_rate" in data
    assert "key_findings" in data

def test_hr_analytics():
    response = client.get("/api/hr-analytics")
    assert response.status_code == 200
    data = response.json()
    assert "department_analysis" in data
    assert "salary_analysis" in data

def test_data_scientist_metrics():
    response = client.get("/api/data-scientist-metrics")
    assert response.status_code == 200
    data = response.json()
    assert "best_model" in data
    assert "results" in data

def test_predict_attrition():
    payload = {
        "satisfaction_level": 0.35,
        "last_evaluation": 0.85,
        "number_project": 6,
        "average_montly_hours": 260,
        "time_spend_company": 4,
        "Work_accident": 0,
        "promotion_last_5years": 0,
        "Department": "technical",
        "salary": "low"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability_leave" in data
    assert "probability_stay" in data
    assert "contributing_factors" in data
