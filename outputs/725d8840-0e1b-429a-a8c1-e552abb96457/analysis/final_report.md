
# Comprehensive Analysis Report

## Data Loading & Initial Review
- Data loaded from "data/temp_upload.csv" with shape 299 rows x 13 columns.
- Data types were inspected using .info() and summary statistics computed with .describe().
- No duplicate rows were found.

## Data Cleaning & Preprocessing
- Continuous variables (age, creatinineP, ejection, platelets) were converted to numeric.
- Missing values in continuous variables were imputed using the median.
- Outliers were detected using the IQR method and winsorized.

## Exploratory Data Analysis (EDA)
### Univariate Analysis
- Histograms with density curves for continuous variables.
- Bar charts for binary/categorical variables (anaemia, diabetes, bloodPressure, sex, smoking, DEATH).

  ![Univariate Continuous](outputs/visualization/univariate_continuous.png)
  ![Univariate Categorical](outputs/visualization/univariate_categorical.png)

### Bivariate Analysis with DEATH
- Boxplots and overlapping histograms displaying differences in continuous variables by DEATH.

  ![Boxplots by DEATH](outputs/visualization/bivariate_boxplot_DEATH.png)
  ![Histograms by DEATH](outputs/visualization/bivariate_histogram_DEATH.png)

### Correlation Analysis
- A correlation matrix for continuous variables visualized via a heatmap.

  ![Correlation Matrix](outputs/visualization/correlation_matrix.png)

## Statistical Analysis
### Hypothesis Testing
- T-tests for continuous variables comparing DEATH outcomes. For example:
  - Age: t-statistic = -4.521, p-value = 0.000
- Chi-square tests for categorical variables. For instance:
  - Anaemia: chi2 = 1.042, p-value = 0.307

### Regression Analysis
- Logistic regression analysis was skipped due to the unavailability of statsmodels.

## Data Visualization for Insight Communication
- A scatter plot of creatinineP vs. ejection fraction with DEATH status indicated provides patient stratification insight.

  ![Scatter Plot](outputs/visualization/scatter_creatinineP_ejection.png)

## Integration of External Analysis Ideas
- Additional visualization methods and clinical insights were examined.
- Findings align with clinical evidence indicating that high creatinineP and low ejection fraction are key risk factors for DEATH.

## Conclusion
This comprehensive analysis reveals that factors such as creatinineP, ejection fraction, and certain binary clinical indicators significantly impact the DEATH outcome. Both statistical tests and visual explorations support these clinical insights.
