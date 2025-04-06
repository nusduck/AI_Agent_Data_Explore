
# Exploratory Data Analysis Report

## Step 1: Data Loading and Cleaning
- **Data Import:** The CSV file was loaded successfully, revealing a dataset with 299 rows and 13 columns.
- **Structure & Types:** The inspection using df.info() confirmed the data structure. Although many predictors are stored as numeric types, some (e.g., bloodPressure, sex) are binary and may benefit from recoding.
- **Missing Values & Outliers:** No substantial missing values were found; duplicates were minimal. Summary statistics indicated potential outlier clusters, particularly in creatinine-related variables.

## Step 2: Exploratory Data Analysis (EDA)
- **Summary Statistics:** Continuous variables (age, creatinineP, platelets, creatinineS, sodium, time) showed broad ranges and varying dispersion.
- **Frequency Analysis:** The binary variables (anaemia, diabetes, bloodPressure, sex, smoking, DEATH) exhibit distinctive proportions. This information establishes the baseline for class balance.

## Step 3: Basic Visualizations
- **Histograms:** The distribution of continuous variables revealed skewness and potential outliers.
- **Bar Charts:** Count plots for binary predictors, especially the DEATH outcome, provided clear visualization of class distributions.

## Step 4: Correlation Analysis and Statistical Testing
- **Correlation Matrix:** The heatmap displayed relationships among continuous variables and the DEATH outcome, with certain variables (e.g., creatinineP) showing stronger associations.
- **Box Plots:** Visual comparisons between DEATH groups highlighted significant differences in the medians and dispersion for several continuous variables.
- **Statistical Testing:** T-tests for continuous features and chi-squared tests for binary predictors produced several statistically significant differences (p-value < 0.05), reinforcing the visual insights.

## Step 5: Advanced Visualizations
- **Pair Plot:** The pair plot allowed for an in-depth view of the pairwise relationships among continuous variables, with DEATH-based color coding suggesting potential clusters.
- **Violin Plots:** Enhanced violin plots confirmed the differences in distribution shapes and variability between DEATH groups, adding nuance to the earlier box plot observations.

## Conclusion
The EDA identified key variables, such as elevated creatinine levels and differences in other physiological measures, that are strongly associated with the DEATH outcome. These insights pave the way for further predictive modeling and risk assessment. The combination of visual and statistical evidence establishes a robust understanding of the data.

