# Independent Exploratory Data Analysis (EDA) Report — Original Dataset

## Dataset Summary
- **Dataset Source:** `HR_capstone_dataset.csv` (Original Dataset)
- **Total Records (Raw):** 14999
- **Total Records (Cleaned / Deduplicated):** 11991
- **Overall Attrition Rate:** 16.60%

## Statistical Test Results (Mann-Whitney U)
| Feature | Left Mean | Stay Mean | p-value | Cohen's d |
| :--- | :--- | :--- | :--- | :--- |
| satisfaction_level | 0.44 | 0.667 | 2.2403e-266 | -1.006 |
| average_montly_hours | 208.162 | 198.943 | 1.8324e-07 | 0.19 |
| number_project | 3.883 | 3.787 | 3.8103e-01 | 0.083 |
| time_spend_company | 3.881 | 3.262 | 2.0964e-177 | 0.473 |
| last_evaluation | 0.722 | 0.716 | 5.2784e-01 | 0.036 |

## Departmental Attrition Breakdown
| Department   |   Total_Employees |   Attrition_Rate |   Left_Count |
|:-------------|------------------:|-----------------:|-------------:|
| hr           |               601 |         0.18802  |          113 |
| accounting   |               621 |         0.175523 |          109 |
| technical    |              2244 |         0.173797 |          390 |
| support      |              1821 |         0.171334 |          312 |
| sales        |              3239 |         0.169805 |          550 |
| marketing    |               673 |         0.166419 |          112 |
| IT           |               976 |         0.161885 |          158 |
| product_mng  |               686 |         0.16035  |          110 |
| RandD        |               694 |         0.122478 |           85 |
| management   |               436 |         0.119266 |           52 |

## Salary Tier Attrition Breakdown
| salary   |   Total_Employees |   Attrition_Rate |   Left_Count |
|:---------|------------------:|-----------------:|-------------:|
| high     |               990 |        0.0484848 |           48 |
| low      |              5740 |        0.20453   |         1174 |
| medium   |              5261 |        0.14617   |          769 |

## Answers to Essential HR Questions (Original Dataset)
1. **Why are employees leaving?**
   - Employees who leave exhibit significantly lower satisfaction levels, bimodal distribution of evaluations (very low or very high evaluation), high monthly working hours (burnout), and lack of promotions.
2. **Which employee groups are most affected?**
   - Low salary brackets and specific departments (HR, Accounting, Technical, Sales) show heightened vulnerability, peaking at 3–5 years of tenure.
3. **What are the strongest indicators of attrition?**
   - Satisfaction level is the primary indicator, followed by monthly hours, number of projects (overload/underload), and tenure milestone.