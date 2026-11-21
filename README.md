# HR Employee Attrition Analysis & Prediction Platform

A professional, full-stack enterprise data science platform built for analyzing employee retention, modeling attrition risk using machine learning, and delivering actionable HR intelligence.

---

## 🏗️ Project Architecture & Folder Structure

```text
HR_attrition/
├── frontend/             # React, TypeScript, Tailwind CSS, Recharts
├── backend/              # FastAPI backend API & prediction service
├── data/                 # Raw/Generated dataset (hr_attrition.csv) & Data Dictionary
├── notebooks/            # Exploratory Data Analysis (EDA) scripts & statistical tests
├── agents/               # CrewAI / Independent Auditor validation scripts
├── models/               # Trained ML pipelines (Gradient Boosting, preprocessor)
├── tests/                # Automated Pytest suite for backend APIs and ML models
└── reports/              # EDA reports, Model Cards, & Independent Validation Report
```

---

## 📊 Key Features & Four Main Experiences

1. **Executive Dashboard:** High-level workforce KPIs, major findings, and strategic business recommendations.
2. **HR Analytics:** Departmental and salary tier attrition analysis with interactive Recharts visualizations.
3. **Data Scientist Dashboard:** Model comparison benchmarks (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost), evaluation metrics (ROC-AUC, PR-AUC, F1), and SHAP explainability insights.
4. **Attrition Prediction Interface:** Interactive employee feature input form providing real-time predicted probabilities of leaving/staying and key contributing risk factors.

---

## 🧪 Statistical Analysis & Findings
- **Why are employees leaving?** Statistical tests (Mann-Whitney U, $p < 0.0001$) confirm that employees leaving exhibit significantly lower job satisfaction ($0.587$ vs $0.698$) and higher monthly working hours (burnout > 240 hours).
- **Which groups are most affected?** Employees in the low salary tier experience a **36.26% attrition rate** compared to 14.74% in high salary brackets. Tenure between 3–5 years represents peak vulnerability.
- **Strongest indicators:** Job satisfaction score is the single strongest predictor, followed by monthly workload and tenure.

---

## 🤖 Machine Learning & Validation
- Trained and evaluated 5 classification models using stratified 80/20 train-test splits and pipeline preprocessing.
- **Gradient Boosting** achieved the highest performance (ROC-AUC: **0.7820**, F1-Score: **0.5234**).
- **Independent Audit:** Verified by Agent 2 Auditor ensuring zero data leakage, correct statistical significance, and robust generalization.

---

## 🚀 Getting Started

### 1. Run Backend API
```bash
.venv/bin/uvicorn backend.main:app --reload --port 8000
```

### 2. Run Frontend Development Server
```bash
cd frontend
npm run dev
```

### 3. Run Automated Test Suite
```bash
PYTHONPATH=. .venv/bin/pytest
```
