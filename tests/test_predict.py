from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_prediction_endpoint():
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
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200

if __name__ == '__main__':
    test_prediction_endpoint()
