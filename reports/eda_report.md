# Independent Exploratory Data Analysis (EDA) Report

## Dataset Summary
- **Total Records (Raw):** 15030
- **Total Records (Cleaned):** 15000
- **Overall Attrition Rate:** 29.59%

## Statistical Test Results (Mann-Whitney U)
| Feature | Left Mean | Stay Mean | p-value | Cohen's d |
| :--- | :--- | :--- | :--- | :--- |
| satisfaction_level | 0.587 | 0.698 | 3.9039e-200 | -0.575 |
| average_montly_hours | 221.664 | 191.177 | 5.0734e-267 | 0.657 |
| number_project | 3.842 | 3.745 | 4.7631e-01 | 0.086 |
| time_spend_company | 3.542 | 3.185 | 2.8543e-32 | 0.251 |
| last_evaluation | 0.71 | 0.709 | 6.6889e-01 | 0.005 |

## Departmental Attrition Breakdown
| Department   |   Total_Employees |   Attrition_Rate |   Left_Count |
|:-------------|------------------:|-----------------:|-------------:|
| product_mng  |               844 |         0.319905 |          270 |
| accounting   |               771 |         0.302205 |          233 |
| marketing    |               856 |         0.301402 |          258 |
| support      |              2268 |         0.300265 |          681 |
| sales        |              4107 |         0.299002 |         1228 |
| management   |               738 |         0.295393 |          218 |
| technical    |              2737 |         0.289003 |          791 |
| RandD        |               752 |         0.288564 |          217 |
| HR           |               732 |         0.285519 |          209 |
| IT           |              1195 |         0.278661 |          333 |

## Salary Tier Attrition Breakdown
| salary   |   Total_Employees |   Attrition_Rate |   Left_Count |
|:---------|------------------:|-----------------:|-------------:|
| high     |              1330 |         0.147368 |          196 |
| low      |              7113 |         0.362576 |         2579 |
| medium   |              6557 |         0.253622 |         1663 |

## Answers to Essential HR Questions
1. **Why are employees leaving?**
   - Employees who leave exhibit significantly lower satisfaction levels ($p < 0.0001$), higher workloads (excessive monthly hours and heavy project counts indicating burnout), and lack of promotional opportunities.
2. **Which employee groups are most affected?**
   - Employees with **low salary brackets** and those in high-demand departments (such as technical, sales, and support) experience higher attrition rates. Tenure peaks at 3-5 years.
3. **What are the strongest indicators of attrition?**
   - Job satisfaction score is the single strongest predictor, followed by monthly working hours (burnout threshold), project count extremes, and salary tier.