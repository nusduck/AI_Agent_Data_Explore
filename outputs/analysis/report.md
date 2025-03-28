
# Analysis Report

## Data Overview
- The dataset consists of 37 rows and 11 columns.
- Two categorical columns ('Reference area' and 'Measure') were converted to categorical types.
- Year columns originally labeled as X2015 to X2023 were renamed to '2015' to '2023' and converted to numeric types.
- The data was reshaped from wide to long format with columns: Reference area, Measure, Year, and Value.

## Data Quality
- Missing values were checked; please review the printed summary for column-specific details.
- Outlier analysis (using 1st and 99th percentiles) identified a number of potential outlier entries which may require further investigation.

## Exploratory Analysis
- Summary statistics were computed for each measure and for each year, offering insights into central tendency and dispersion.
- A year-over-year percentage change was calculated grouped by Reference area and Measure, which facilitates trend analysis.

## Visualizations
- **Time Series Plots:** For each measure, line plots were generated showing trends over the years for different countries. These plots highlight the evolution and potential seasonal patterns.
- **Bar Charts:** A bar chart for the latest available year (2023) compares the values across countries and measures.
- **Heatmaps:** Heatmaps were produced for each measure, providing a visual perspective on how values evolve over time across different countries.
- **Box Plots:** Box plots illustrate the distribution and variability of values over the years for each measure, helping to visually flag outliers.

## Key Insights
- The trends observed in the time series plots suggest varying behavior across countries and measures. Some measures show consistent increases or decreases while others exhibit more variability.
- The bar chart for 2023 indicates noticeable differences in the current values among the countries.
- Heatmaps and box plots complement these observations by highlighting underlying distribution patterns and anomalies.

## Next Steps
- Further statistical tests (e.g., t-tests or ANOVA) could be performed to validate the significance of the observed differences.
- More robust methods for handling potential outliers might be needed based on domain-specific thresholds.
- An interactive dashboard could be designed to allow dynamic exploration of the trends and comparisons highlighted in this study.

*This report summarizes the initial exploratory and visual analysis of the OECD prices dataset.*
