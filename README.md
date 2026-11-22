# HR Employee Attrition Intelligence Platform (Original Dataset)

A professional, full-stack enterprise data science platform built exclusively on the original dataset (`HR_capstone_dataset.csv`), analyzing employee retention, modeling attrition risk using machine learning, and delivering actionable HR intelligence.

---

## 🏗️ Project Architecture & Folder Structure

```text
HR_attrition/
├── HR_capstone_dataset.csv # Single source of truth (14,999 records, 10 columns)
├── frontend/               # React, TypeScript, Tailwind CSS, Recharts
├── backend/                # FastAPI backend API & prediction service
├── notebooks/              # Exploratory Data Analysis (EDA) scripts & statistical tests
├── agents/                 # CrewAI / Independent Auditor validation scripts
├── models/                 # Trained ML pipelines (Random Forest, XGBoost, preprocessor)
├── tests/                  # Automated Pytest suite for backend APIs and ML models
└── reports/                # EDA reports, Model Cards, & Independent Validation Report
```

---

## 📊 Key Features & Four Main Experiences

1. **Executive Dashboard:** High-level workforce KPIs, major findings, and strategic business recommendations.
2. **HR Analytics:** Departmental and salary tier attrition analysis with interactive Recharts visualizations.
3. **Data Scientist Dashboard:** Model comparison benchmarks (Logistic Regression, Random Forest, Gradient Boosting, XGBoost), evaluation metrics (Accuracy ~98.6%, F1 ~95.7%, ROC-AUC ~0.977), and explainability insights.
4. **Attrition Prediction Interface:** Interactive employee feature input form providing real-time predicted probabilities of leaving/staying and key contributing risk factors.

---

## 🧪 Statistical Analysis & Findings (Original Dataset)
- **Why are employees leaving?** Statistical tests (Mann-Whitney U, $p < 0.0001$) confirm that employees leaving exhibit significantly lower job satisfaction ($0.44$ vs $0.67$) and higher monthly working hours.
- **Which groups are most affected?** Employees in the low salary tier experience a **20.45% attrition rate** compared to 4.85% in high salary brackets. Tenure between 3–5 years represents peak vulnerability.
- **Strongest indicators:** Job satisfaction score is the single strongest predictor, followed by monthly workload and tenure.

---

## 🤖 Machine Learning & Validation
- Trained and evaluated 4 classification models using stratified 80/20 train-test splits on deduplicated records (11,991 rows).
- **Random Forest** achieved outstanding performance (Accuracy: **98.62%**, Precision: **98.93%**, Recall: **92.71%**, F1-Score: **95.72%**, ROC-AUC: **0.9772**).
- **Independent Audit:** Verified by Agent 2 Auditor ensuring zero synthetic data usage, zero data leakage, and robust generalization matching the user's previous experimental results (~95.5% F1-score).

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
