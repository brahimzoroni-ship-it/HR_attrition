import numpy as np
import pandas as pd

np.random.seed(42)
n_samples = 15000

departments = ['sales', 'technical', 'support', 'IT', 'product_mng', 'marketing', 'RandD', 'accounting', 'HR', 'management']
dept_probs = [0.27, 0.18, 0.15, 0.08, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05]

salaries = ['low', 'medium', 'high']
salary_probs = [0.48, 0.43, 0.09]

# Generate features
dept = np.random.choice(departments, size=n_samples, p=dept_probs)
salary = np.random.choice(salaries, size=n_samples, p=salary_probs)
satisfaction_level = np.clip(np.random.beta(a=3, b=1.5, size=n_samples), 0.05, 1.0)
last_evaluation = np.clip(np.random.normal(loc=0.71, scale=0.17, size=n_samples), 0.35, 1.0)
number_project = np.random.choice([2, 3, 4, 5, 6, 7], size=n_samples, p=[0.1, 0.35, 0.30, 0.18, 0.05, 0.02])
average_montly_hours = np.random.normal(loc=200, scale=50, size=n_samples).astype(int)
average_montly_hours = np.clip(average_montly_hours, 96, 310)
time_spend_company = np.random.choice([2, 3, 4, 5, 6, 7, 8, 10], size=n_samples, p=[0.32, 0.38, 0.15, 0.08, 0.03, 0.02, 0.01, 0.01])
Work_accident = np.random.choice([0, 1], size=n_samples, p=[0.85, 0.15])
promotion_last_5years = np.random.choice([0, 1], size=n_samples, p=[0.97, 0.03])

# Calculate attrition probability using logistic function with realistic coefficients
# Factors increasing attrition: low satisfaction, very low or very high evaluation, extreme monthly hours, high project count (overload) or low project count, low salary, long tenure without promotion.
sat_effect = -3.5 * (satisfaction_level - 0.5)
hours_effect = 0.015 * (average_montly_hours - 180)
proj_effect = 0.8 * np.abs(number_project - 4) - 0.5 # too few or too many projects
tenure_effect = 0.2 * (time_spend_company - 3)
salary_effect = np.where(salary == 'low', 0.8, np.where(salary == 'medium', 0.2, -0.6))
promo_effect = -1.2 * promotion_last_5years
accident_effect = -0.5 * Work_accident

# Add some non-linearity and interaction
overworked_burnout = np.where((average_montly_hours > 240) & (number_project >= 5), 1.5, 0.0)
underchallenged = np.where((average_montly_hours < 130) & (number_project <= 2), 0.8, 0.0)

logits = -1.5 + sat_effect + hours_effect + proj_effect + tenure_effect + salary_effect + promo_effect + accident_effect + overworked_burnout + underchallenged
probs = 1 / (1 + np.exp(-logits))
left = np.random.binomial(1, probs)

df = pd.DataFrame({
    'satisfaction_level': np.round(satisfaction_level, 2),
    'last_evaluation': np.round(last_evaluation, 2),
    'number_project': number_project,
    'average_montly_hours': average_montly_hours,
    'time_spend_company': time_spend_company,
    'Work_accident': Work_accident,
    'left': left,
    'promotion_last_5years': promotion_last_5years,
    'Department': dept,
    'salary': salary
})

# Introduce minor noise / missing values / duplicates to simulate real-world data quality checks
df.loc[np.random.choice(n_samples, 25, replace=False), 'satisfaction_level'] = np.nan
df.loc[np.random.choice(n_samples, 15, replace=False), 'average_montly_hours'] = np.nan

# Add some duplicate rows
df = pd.concat([df, df.iloc[:30]], ignore_index=True)

df.to_csv('data/hr_attrition.csv', index=False)
print(f"Dataset generated successfully with {len(df)} rows. Attrition rate: {df['left'].mean():.2%}")
