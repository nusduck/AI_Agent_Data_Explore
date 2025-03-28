
# Analysis Report

## 1. Data Cleaning and Preprocessing
- **Dataset Dimensions:** Loaded data with shape: (357, 7).
- **Missing Values & Duplicates:** No missing values and no duplicate rows.
- **Data Types:** 'Brand' is a categorical column; the other columns are numeric.
- **Feature Engineering:** One-hot encoded the 'Brand' column.

## 2. Exploratory Data Analysis (EDA)
- **Descriptive Statistics:** Summary statistics show a tight spread for Price and other features.
- **Brand Distribution:** Dell (80), Asus (77), Lenovo (71), Acer (66), HP (63).
- **Visualizations:**  
  - Univariate plots for Price (histogram, boxplot, density plot).  
  - Scatter plots for Price versus predictors.  
  - Box plots by Brand and a correlation heatmap among numeric features.

## 3. Predictive Modeling
- **Model:** Multiple linear regression with Price as the target.
- **Performance:**  
  - R²: 0.878  
  - MSE: 45347.393  
  - MAE: 161.915
- **Feature Importances:**  
  - The most influential predictor is Processor_Speed, with additional contributions from RAM_Size, Weight, and Screen_Size.  
  - Brand dummies adjust the baseline price.

## 4. Conclusions & Recommendations
- The model explains around 87.8% of the variance in Price.
- Key predictors include Processor_Speed and RAM_Size, with brand-specific effects.
- Future work could consider additional features (e.g., battery life, GPU details), advanced modeling methods, and examination of feature interactions.

## 5. Visualizations
All visualizations have been saved in:
outputs/20cb90a6-f138-4c39-aa38-2f7d239462f9/visualization
