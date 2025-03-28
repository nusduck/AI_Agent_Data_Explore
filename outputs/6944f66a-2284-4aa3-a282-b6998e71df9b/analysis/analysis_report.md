# Data Analysis Report

## 1. Data Ingestion and Preprocessing
- Data was loaded from "data/temp_upload.xlsx" and filtered to include only rows where **Dimension = 'Age'**.
- The 'Category' (representing age groups) and 'Percentage' columns were validated and cleaned.
- Final dataset contains 43 rows of age-related data.

## 2. Exploratory Data Analysis (EDA)
- **Unique Age Categories:** ['30-49', '50-64', 'Ages 18-29', '65+']
- **Unique Platforms:** ['Be Real', 'Facebook', 'Instagram', 'Linked In', 'Pinterest', 'Reddit', 'Snapchat', 'Tik Tok', 'Twitter (X)', 'Whats App', 'You Tube']

### Frequency Distributions:
- **Age Categories Frequency:**  
Category
30-49         11
50-64         11
Ages 18-29    11
65+           10

- **Platforms Frequency:**  
Platform
Facebook       4
Instagram      4
Linked In      4
Pinterest      4
Reddit         4
Snapchat       4
Tik Tok        4
Twitter (X)    4
Whats App      4
You Tube       4
Be Real        3

### Percentage Summary:
~~~
count    43.000000
mean     37.139535
std      25.515244
min       1.000000
25%      15.500000
50%      32.000000
75%      58.500000
max      93.000000
~~~

### Pivot Table (Platforms vs. Age Categories):
~~~
Category     30-49  50-64   65+  Ages 18-29
Platform                                   
Be Real        3.0    1.0   0.0        12.0
Facebook      75.0   69.0  58.0        67.0
Instagram     59.0   35.0  15.0        78.0
Linked In     40.0   31.0  12.0        32.0
Pinterest     40.0   33.0  21.0        45.0
Reddit        31.0   11.0   3.0        44.0
Snapchat      30.0   13.0   4.0        65.0
Tik Tok       39.0   24.0  10.0        62.0
Twitter (X)   27.0   17.0   6.0        42.0
Whats App     38.0   29.0  16.0        32.0
You Tube      92.0   83.0  60.0        93.0
~~~

## 3. Statistical Analysis
- **Chi-square Test for Independence:**  
  Chi-Square Statistic: 126.6420, p-value: 0.0000, Degrees of Freedom: 30  
  (A p-value < 0.05 would indicate a statistically significant relationship between platform and age group.)

- **ANOVA Test:**  
  ANOVA Statistic: 5.9050, p-value: 0.0001  
  (A p-value < 0.05 suggests significant differences in mean percentage values across platforms.)

## 4. Data Visualization
The following visualizations were generated and saved in the directory:  
`outputs/6944f66a-2284-4aa3-a282-b6998e71df9b/visualization`

1. **Grouped Bar Chart:** Compares age group percentages side-by-side for each platform.
2. **Stacked Bar Chart:** Shows the composition of age group percentages within each platform.
3. **Heatmap:** Provides a color-coded overview of percentage values across platforms and age groups.

## 5. Interpretation and Recommendations
- The **Grouped Bar Chart** and **Stacked Bar Chart** facilitate visual comparison of age group distributions across platforms.
- The **Heatmap** aids in quickly identifying platforms with particularly high or low percentage values for certain age groups.
- Statistical tests (Chi-square and ANOVA) support the evaluation of observed trends.
- **Limitations:** The analysis assumes that the provided percentage values approximate weighted frequencies since raw counts were not available.
- **Further Analysis:** Expanding this analysis to other dimensions (e.g., Gender, Political Affiliation) could provide a more comprehensive view.

