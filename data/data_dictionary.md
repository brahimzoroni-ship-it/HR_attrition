# HR Attrition Dataset - Data Dictionary

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `satisfaction_level` | Float (0.0 - 1.0) | Employee job satisfaction score reported via periodic surveys. |
| `last_evaluation` | Float (0.0 - 1.0) | Performance evaluation score from the most recent review cycle. |
| `number_project` | Integer | Total number of projects assigned to the employee. |
| `average_montly_hours` | Integer | Average monthly working hours logged by the employee. |
| `time_spend_company` | Integer | Tenure at the company (in years). |
| `Work_accident` | Integer (0/1) | Indicator of whether the employee experienced a workplace accident (1 = Yes, 0 = No). |
| `left` | Integer (0/1) | Target variable indicating employee attrition (1 = Left the company, 0 = Stayed). |
| `promotion_last_5years` | Integer (0/1) | Indicator of whether the employee received a promotion in the last 5 years (1 = Yes, 0 = No). |
| `Department` | String / Categorical | Organizational department (e.g., sales, technical, support, IT, management). |
| `salary` | String / Categorical | Relative salary bracket tier ('low', 'medium', 'high'). |
