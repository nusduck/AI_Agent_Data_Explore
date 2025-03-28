
# Data Analysis and Technical Indicators Report

## Data Overview
- The original dataset contained 267 rows and 13 columns. After data type conversions and cleaning (dropping missing values), the dataset now has 267 rows.
- The 'Date' column was converted to datetime and set as the index.
- 'Stock Code' was verified as a categorical variable.
- Numeric columns (e.g., Open, Close, High, Low, Volume, Price_Change, Amplitude_pct) were processed accordingly.

## Exploratory Data Analysis (EDA)
- Summary statistics for numeric variables were computed and saved.
- A time series chart of the Close price shows the trend over time.
- Histograms (if available) for Price Change and Amplitude distributions were generated.
- A correlation matrix among numeric variables was visualized.

## Technical Indicators Calculated
- **Moving Averages**: SMA20 and EMA12 (used in overlay plots with the Close price).
- **MACD**: Computed as the difference between EMA12 and EMA26, along with its signal line.
- **RSI**: Computed over a 14-day period to indicate overbought or oversold conditions.
- **Bollinger Bands**: Calculated with a 20-day SMA (middle band) and ±2 standard deviations for upper and lower bands.

## Visualization of Technical Indicators
- **Price with Moving Averages**: Overlay plot displays the Close price with SMA20 and EMA12 to highlight potential trend crossovers.
- **MACD and RSI Plots**: Dual subplots visualize momentum shifts and price action relative to overbought/oversold thresholds.
- **Bollinger Bands**: The Close price is plotted along with Bollinger Bands, showing price volatility and potential breakout regions.

## Interpretation of Findings
- The interplay between the Close price and moving averages provides insights into trend directions and potential reversals.
- The MACD and its signal line help in identifying momentum changes, with RSI further indicating possible overbought/oversold conditions.
- Bollinger Bands serve as a useful tool in assessing price variability and breakout patterns.
- These visualizations and analyses form a strong basis for further trend analysis, regression testing, or comparative studies across multiple stocks.

## Additional Considerations
- Future analysis could incorporate volume-based metrics such as On-Balance Volume (OBV) for additional market context.
- For datasets with multiple stocks, similar technical indicator analyses can be compared across different 'Stock Code' categories.

All visualizations are saved in the directory: `outputs/visualization/`.
