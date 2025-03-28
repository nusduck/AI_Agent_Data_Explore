
# Analysis Report

## Data Overview
- The dataset originally contained 37 rows and 11 columns.
- Two columns ('Reference area' and 'Measure') were converted to categorical types.
- Yearly price columns (X2015 to X2023) were converted to numeric values.
- Missing values and duplicate records were removed, resulting in a clean dataset.

## Exploratory Data Analysis (EDA)
- **Descriptive Statistics:**  
  Summary statistics grouped by 'Reference area' and 'Measure' show variations in central tendency and spread.
- **Price Distributions:**  
  Histograms and density plots revealed the distribution shape of price variables across the different measures.
- **Yearly Variations:**  
  Box plots for each year illustrated the presence of outliers and differences in interquartile ranges.
- **Trend Analysis:**  
  Line plots across years for each measure (with breakdown by 'Reference area') indicated observable trends and potential seasonal patterns.

## Statistical Analysis & Predictive Modeling
- **Correlation Analysis:**  
  The heatmap of correlations among the yearly price columns showed a strong positive correlation between most years.
- **Regression Modeling:**  
  A linear regression model was built using prices from X2015 to X2021 to predict the price in X2023.  
  - R-squared: 0.468  
  - RMSE: 41.277  
  The regression plot (X2021 vs X2023) suggests that the price in 2021 is a relatively strong predictor for the price in 2023.

## Visualizations
- All figures were generated using a minimalist, dark-mode, high-contrast style to ensure clarity and accessibility.
- Key visualizations include:
    - Price distribution (histogram and density)
    - Yearly price box plots
    - Trend line plots by measure and reference area
    - Correlation heatmap among yearly prices
    - Regression and scatter plots for evaluating relationships between key years

## Conclusions and Recommendations
- The analysis highlights clear trends in the pricing data, with consistent patterns across most years.
- The regression model indicates that historical prices can predict future values reasonably well, although the small dataset size limits robustness.
- Future work should consider:
    - Acquiring more data to improve model stability.
    - Exploring other predictive modeling techniques.
    - A deeper investigation into the causes of outliers and anomalies observed in the data.

