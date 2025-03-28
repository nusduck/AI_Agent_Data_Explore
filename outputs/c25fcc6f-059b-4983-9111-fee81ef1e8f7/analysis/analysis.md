# Analysis Report

## 1. Data Loading and Initial Inspection
- The dataset was loaded from "data/temp_upload.csv" and contains 2938 rows and 22 columns.
- Column names were standardized to lower-case, and initial inspection revealed important features such as "life expectancy", "adult mortality", "gdp", and "population".

## 2. Data Cleaning and Preprocessing
- Non-categorical columns were converted to numeric. Missing values were imputed using the median.
- The "status" column was one-hot encoded to support group comparisons.

## 3. Exploratory Data Analysis (EDA)
- **Descriptive Statistics:** Saved as "descriptive_statistics.csv".
- **Visualizations:**  
  - Scatter plots (Life Expectancy vs GDP and vs Adult Mortality)  
  - Box plot by status group  
  - Histogram and density plot of Life Expectancy  
  - Correlation heatmap among numeric variables

## 4. Statistical Analysis
- **Correlation Analysis:**  
  - GDP: 0.43  
  - Adult Mortality: -0.70  
  - Population: -0.03  
  - Hepatitis B: 0.17
- **T-test:**  
  A t-test between Developing and non-Developing countries resulted in a t-statistic of -47.87 with a p-value of 1.9763e-323, indicating statistically significant differences.

## 5. Feature Selection and Modeling Pipeline
- A multiple linear regression model was developed after removing non-predictive identifier columns.
- **Model Performance:**  
  - R-squared: 0.82  
  - RMSE: 3.91
- Diagnostic plots (Residual Plot and Predicted vs Actual) and a feature importance chart were generated.

## 6. Visualizations
All plots are saved in the following directory:
outputs/c25fcc6f-059b-4983-9111-fee81ef1e8f7/visualization

## 7. Interpretation of Results
- Key predictors of Life Expectancy include Adult Mortality and GDP.
- The statistical tests confirm a significant difference in Life Expectancy between Developing and non-Developing countries.
- The regression model (R-squared = 0.82) offers a robust baseline; however, additional feature engineering and advanced modeling could further enhance predictive accuracy.

## 8. Conclusion
This analysis—from data cleaning and exploratory analysis through statistical testing and regression modeling—provides actionable insights into the determinants of Life Expectancy. The findings highlight the crucial roles of Adult Mortality and GDP, and the work lays the groundwork for more sophisticated investigations in the future.
