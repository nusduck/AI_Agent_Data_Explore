
# Forecasting Analysis Report

## Data Overview
- The dataset contains 297 rows and 13 columns.
- The datetime column identified is **Unnamed: 0** and was set as the index.
- The target forecasting column is **price**.

## Feature Engineering
- Created lagged features: price_lag_1, price_lag_2, price_lag_3.
- Computed a rolling average feature named price_roll_3 with a window of 3.

## Seasonal-Trend Decomposition (Custom)
- A simple seasonal-trend decomposition was performed assuming a weekly period (7 days).
- Trend was estimated using a centered rolling average.
- Seasonal component was derived by grouping detrended values by day-of-week.
- Residuals were computed by subtracting the seasonal component from the detrended series.
- The decomposition plot (Observed, Trend, Seasonal, Residual) is saved at:
  `/Users/eddieho/Documents/NUS/QF5208/ai_agent/outputs/b4750f61-ed20-4e82-b782-27961e485193/visualization/seasonal_decomposition.png`

## Modeling & Forecasting
- The series was split into training (80%) and testing (20%) sets.
- A naive forecasting method was employed: the last observation from the training set was used as a constant forecast.
- Forecast for the test set is: 1525.0.

### Evaluation Metrics:
- **Mean Absolute Error (MAE):** 58.3252
- **Root Mean Squared Error (RMSE):** 67.0011

## Visualization
- The Actual vs Naive Forecasted Prices plot is saved at:
  `/Users/eddieho/Documents/NUS/QF5208/ai_agent/outputs/b4750f61-ed20-4e82-b782-27961e485193/visualization/forecast_vs_actual.png`

## Insights
- The decomposition reveals underlying trend and seasonal patterns in the data.
- Although the naive forecast offers a simple baseline, the error metrics indicate room for improvement with more advanced models.
- Future work might include experimenting with ARIMA or LSTM-based forecasting models when additional libraries are available.

---

*End of Analysis Report*
