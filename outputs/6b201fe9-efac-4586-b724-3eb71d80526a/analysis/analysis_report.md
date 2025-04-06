# Data Analysis Report

## Step 1: Data Cleaning and Preprocessing
- CSV file loaded with 299 rows and 13 columns.
- All required columns were converted to numeric data types.
- Missing values dropped and duplicates removed (duplicates count: 0).

## Step 2: Exploratory Data Analysis (EDA)
- **Continuous Variables:** Summary statistics computed (see `data_summary.txt`).
- **Binary Variables:** Frequency counts computed.
- **Visualizations:** Histograms, bar charts, a correlation heatmap, and a scatter plot (age vs. ejection) generated.

## Step 3: Statistical Analysis
- **Group Comparisons:** Data split by DEATH outcome; box plots for continuous variables created.
- **Hypothesis Testing:**
  - T-tests for continuous variables and Chi-square tests for binary variables were conducted (results in `statistical_tests.txt`).

## Step 4: Advanced Visualizations
- Detailed correlation heatmap for all variables.
- Pair plot of continuous variables conditioned on DEATH.
- Stacked bar charts displaying proportions of binary risk factors by DEATH.
- Kaplan-Meier style survival curves computed manually from the 'time' variable.

## Step 5: Interpretation and Recommendations
- **Key Insights:**
  - Significant differences observed in variables such as creatinineP and creatinineS between DEATH groups.
  - Visual analyses suggest potential clinically relevant relationships (e.g., age vs. ejection fraction).
- **Recommendations:**
  - Consider predictive models (e.g., logistic regression) using the identified key variables.
  - Further survival analyses may be warranted if detailed censoring information is available.

## Conclusion
The analysis provides a comprehensive overview of the dataset—from data cleaning and EDA to statistical tests and advanced visualizations. The insights derived lay the groundwork for further predictive modeling and clinical investigation.