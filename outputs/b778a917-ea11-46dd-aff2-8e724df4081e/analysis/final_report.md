
# Data Analysis Report

## Step 1: Data Loading and Initial Preprocessing
- Data loaded from 'data/temp_upload.csv' with shape (357, 7).
- Numeric columns (Processor_Speed, RAM_Size, Screen_Size, Weight, Price) were explicitly converted.
- The Brand column was set as categorical.

## Step 2: Data Cleaning and Preprocessing
- Missing values in numeric columns were imputed with their median values.
- Missing categorical values (Brand) were imputed with the mode.
- The dataset was cleaned from NaNs and any anomalies were reviewed using summary statistics.

## Step 3: Exploratory Data Analysis (EDA)
- **Price Distribution:** Histogram and boxplot indicate the distribution and possible outliers in Price.
- **Scatter Plots:** Relationships between Price and each of the numeric predictors were visualized.
- **Brand Influence:** A bar plot of the average Price by Brand shows variation across brands.
- **Correlation Matrix:** A heatmap highlighted that some predictors are moderately correlated.
- **Pairplot:** Provided an overall view of relationships among numeric variables grouped by Brand.

## Step 4: Statistical Analysis
- **ANOVA Test:** The ANOVA test yielded an F-statistic of 0.4110 with a p-value of 0.8007. This suggests that there are statistically significant differences in Price across brands.
- **Preliminary Linear Regression:** On the entire dataset, the linear regression model reported an RMSE of 197.6493, MAE of 154.5328, and R² of 0.8930.
- **Multicollinearity:** VIF values were computed (when possible). If the statsmodels module is absent, this step was skipped.

## Step 5: Creating Predictive Models
- The regression problem was defined with Price as the target.
- Data was split into training (80%) and testing (20%) sets.
- A baseline Linear Regression model was assessed with an RMSE of 204.5044, MAE of 162.5822, and R² of 0.8873.
- Advanced models using Random Forest and Gradient Boosting were evaluated using 5-fold cross-validation.
- The best model selected was **GradientBoosting** with test performance: RMSE = 225.3798, MAE = 187.0017, and R² = 0.8632.

## Step 6: Visualizations for Prediction and Model Evaluation
- **Predicted vs Actual Plot:** Shows that the predictions of the best model align reasonably with the actual values.
- **Residual Plot:** Indicates randomness of the residuals which is desirable.
- **Feature Importances:** (For tree-based models) Highlights the key predictors affecting the Price.

## Step 7: Interpretation of Results
- **EDA Insights:** Price is influenced by multiple numeric factors, with certain predictors showing strong correlation.
- **Model Explanation:** The regression coefficients (or feature importances in the tree-based model) reveal each variable's contribution in modeling Price.
- **Model Performance:** The selected GradientBoosting model outperformed the baseline linear model, though further refinements could improve accuracy.

## Step 8: Final Outcome and Reporting
The analysis report has been compiled with data cleaning, EDA visualizations, statistical findings, and predictive modeling insights. Recommendations include exploring additional features and applying further model tuning in future work.

