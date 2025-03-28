# Exploratory Data Analysis and Modeling Report

## Data Overview
- **Original Data Shape:** 9200 rows x 18 columns
- After cleaning, the data dimensions are: **4602 rows x 23 columns**

## Summary Statistics (Numeric Features)

              count           mean            std    min        25%            50%        75%         max
price        4602.0  551912.591694  563738.436651    0.0  322625.00  460943.461539  654987.50  26590000.0
sqft_living  4602.0    2138.888744     963.256877  370.0    1460.00    1980.000000    2620.00     13540.0
bedrooms     4602.0       3.400261       0.909359    0.0       3.00       3.000000       4.00         9.0
bathrooms    4602.0       2.160637       0.783813    0.0       1.75       2.250000       2.50         8.0
house_age    4602.0      28.951760      26.859643    0.0       9.00      20.000000      40.75       114.0

## Frequency Tables (Categorical Variables)
### city

                     Count
city                      
Seattle               1575
Renton                 293
Bellevue               286
Redmond                235
Issaquah               187
Kirkland               187
Kent                   185
Auburn                 176
Sammamish              175
Federal Way            148
Shoreline              123
Woodinville            115
Maple Valley            96
Mercer Island           86
Burien                  74
Snoqualmie              71
Kenmore                 66
Des Moines              58
North Bend              50
Covington               43
Duvall                  42
Lake Forest Park        36
Bothell                 33
Newcastle               33
SeaTac                  29
Tukwila                 29
Vashon                  29
Enumclaw                28
Carnation               22
Normandy Park           18
Clyde Hill              11
Medina                  11
Fall City               11
Black Diamond            9
Ravensdale               7
Pacific                  6
Algona                   5
Yarrow Point             4
Skykomish                3
Preston                  2
Milton                   2
Inglewood-Finn Hill      1
Snoqualmie Pass          1
Beaux Arts Village       1

### waterfront

            Count
waterfront       
0            4569
1              33

### condition

           Count
condition       
3           2876
4           1253
5            435
2             32
1              6

### view

      Count
view       
0      4142
2       205
3       116
4        70
1        69

## Visualizations

### Univariate Analysis
![Univariate Plots](/Users/eddieho/Documents/NUS/QF5208/ai_agent/outputs/a6b794a6-a038-4a02-8eb2-f8d07f859cc5/visualization/univariate_plots.png)

### Bivariate Analysis
![Bivariate Scatter Plots](/Users/eddieho/Documents/NUS/QF5208/ai_agent/outputs/a6b794a6-a038-4a02-8eb2-f8d07f859cc5/visualization/bivariate_scatter.png)

### Time Series Analysis
![Time Series Plot](/Users/eddieho/Documents/NUS/QF5208/ai_agent/outputs/a6b794a6-a038-4a02-8eb2-f8d07f859cc5/visualization/time_series.png)

### Correlation Matrix
![Correlation Heatmap](/Users/eddieho/Documents/NUS/QF5208/ai_agent/outputs/a6b794a6-a038-4a02-8eb2-f8d07f859cc5/visualization/correlation_heatmap.png)

### Regression Model Coefficients
![Regression Coefficients](/Users/eddieho/Documents/NUS/QF5208/ai_agent/outputs/a6b794a6-a038-4a02-8eb2-f8d07f859cc5/visualization/regression_coefficients.png)

## Statistical Analysis

### Correlation with Price
                price
price        1.000000
sqft_living  0.430408
bathrooms    0.327230
bedrooms     0.200507
house_age   -0.002280

### Linear Regression Model (using Least Squares)

The regression model was built using the following predictors: sqft_living, bedrooms, bathrooms, house_age, trans_year

#### Linear Regression Coefficients
- **Intercept**: 0.0215
- **sqft_living**: 273.5007
- **bedrooms**: -57596.5374
- **bathrooms**: 21789.5861
- **house_age**: 987.1650
- **trans_year**: 43.2516

Key findings:
- The coefficients indicate how a one-unit increase in each predictor is associated with changes in house price.
- The computed coefficients provide insight into the importance of features like sqft_living and house_age.

## Summary of Insights

- **Location effects:** Frequency tables for 'city' (if analyzed separately) could reveal location impacts.
- **Physical characteristics:** Attributes such as sqft_living significantly influence price.
- **Time-based trends:** Time series analysis shows seasonal and long-term trends in house prices.
- **House Age:** Derived from construction and renovation years, this feature helps explain depreciation or modernization effects.

This comprehensive analysis, covering data cleaning, descriptive statistics, visualization, and regression modeling using numpy, provides actionable insights into the factors affecting house prices.