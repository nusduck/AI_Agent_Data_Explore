# Data Analysis Assistant - Streamlit Frontend

This Streamlit application provides a user-friendly interface for the data analysis workflow.

## Features

1. **Data Upload**: Upload CSV, Excel, or JSON files
2. **Data Information**: View data description, sample, and detailed information
3. **Analysis Configuration**: Set your analysis target (default: "help me explore the data, show the insights")
4. **Analysis Plan**: View the generated analysis plan and provide feedback
5. **Results Viewer**: Browse analysis reports and visualizations from previous runs

## Running the App

1. Make sure you have installed all required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

3. The app will open in your browser at `http://localhost:8501`

## Workflow

1. Upload your data file using the sidebar
2. Review the data information that's automatically generated
3. Set your analysis target or use the default
4. Click "Start Analysis" to begin the process
5. Review the analysis plan and provide feedback if needed
6. Check the "Analysis Results" section to view reports and visualizations

## Notes

- Analysis results are stored in the `outputs/{uuid}/` directory
- You can select different analysis runs using the dropdown menu in the Results section
- Visualizations are displayed in a grid layout for easy comparison 