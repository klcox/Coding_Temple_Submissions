# Data Cleaning Pipeline

This Python project reads a CSV file containing employee survey data; cleans and analyzes the data; produces visualizations from the analyses, stored as an image file; and exports the cleaned data to a new CSV file.

Data cleaning includes:
- removal of duplicate rows and rows with duplicated/missing employee IDs
- removal of extraneous white space
- standardization (e.g. capitalization, office locations, salary format, date format, etc.)
- conversion of "impossible" values (e.g. survey scores outside of the valid range, negative salary entries, etc.) to NaN

(Rows with missing values [NaN/NaT] in any column except for Employee ID are preserved as the remaining data in the row may still prove useful for various analyses.)

## Set-up

1. Clone this repo
2. Ensure the employee survey data is located at data/messy_employee_survey.csv
3. Create a virtual environment (e.g. for Windows/Git Bash: python -m venv venv)
4. Activate the virtual environment (e.g. for Windows/Git Bash: source venv/Scripts/activate)
5. Install pandas and matplotlib (e.g. for Windows/Git Bash: pip install pandas matplotlib)
6. Run the pipeline: python main.py
