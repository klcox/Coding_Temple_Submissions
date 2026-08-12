import pandas as pd
import re

import matplotlib
matplotlib.use("Agg")  # Prevents errors when no display is available
import matplotlib.pyplot as plt

import os


class DataPipeline:
    """A reusable data processing pipeline."""

    def __init__(self, filepath):
        """
        Loads the raw data from a CSV file. 
        Converts the CSV data into a DataFrame to be used with Python/pandas. 
        If the filepath cannot be found, creates an empty DataFrame so as to prevent later errors.
        """

        try:

            self.df = pd.read_csv(filepath)   

            print(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns.")                    
                        
        except FileNotFoundError:

            print(f"Error: CSV file {filepath} not found.")          
            self.df = pd.DataFrame()


    def clean(self):
        """
        Run all cleaning steps. Returns self for chaining.
        If the DataFrame is empty, the method does not attempt to clean data; it prints a message and returns self as the empty DataFrame.
        """

        if self.df.empty:  # Check for zero rows and/or zero columns
            print("DataFrame is empty. No data to clean.")
            return self


        # Original value (used for comparison in later cleaning summary)
        original_rows = len(self.df)       
                
        # Raw Data overview
        print(f"\n{'=' * 5} Raw Data Overview {'=' * 5}\n")
        print(self.df.head())
        print(f"\nShape: {self.df.shape}")
        print(f"\nMissing values:\n{self.df.isna().sum() }")        
        print(f"\nTotal Missing values:\n{self.df.isna().sum() .sum()}")          


        # Remove (whole) duplicate rows  
        self.df = self.df.drop_duplicates()
        dupe_rows_removed = original_rows - len(self.df)  # Value needed for later cleaning summary

        # Remove rows with duplicated Employee IDs; in the event of a dupe, keep first instance
        dupe_ids_rows_before = len(self.df)  # Value needed for calculation regarding later cleaning summary
        self.df = self.df.drop_duplicates(subset=["employee_id"], keep="first")
        dupe_ids_removed = dupe_ids_rows_before - len(self.df)  # Value needed for later cleaning summary

        # Remove rows with missing Employee IDs
        missing_ids_rows_before = len(self.df)  # Value needed for calculation regarding later cleaning summary
        self.df = self.df.dropna(subset=["employee_id"])
        missing_ids_removed = missing_ids_rows_before - len(self.df)  # Value needed for later cleaning summary

        
        # Strip white space and standardize case for Name, Department, Office Location; Strip white space for Comments     
        self.df["name"] = self.df["name"].str.strip().str.title()
        self.df["department"] = self.df["department"].str.strip().str.title()
        self.df["office_location"] = self.df["office_location"].str.strip().str.title()
        self.df["comments"] = self.df["comments"].str.strip()


        # Normalize Department entries
        department_map = {
            "Eng": "Engineering",
            "Fin": "Finance",
            "HR": "Human Resources",
            "Hr": "Human Resources",
            "H.R.": "Human Resources",
            "Mktg": "Marketing"
        }

        self.df["department"] = self.df["department"].replace(department_map)        


        # Normalize Office Location entries        
        office_map = {
            "Austin, Tx": "Austin",
            "Atx": "Austin",
            "Chi": "Chicago",
            "Nyc": "New York",
            "Work From Home": "Remote",
            "Sea": "Seattle"
        }
        
        self.df["office_location"] = self.df["office_location"].replace(office_map)       

                
        # Convert Salary, Years of Experience, and Satisfaction Score to the appropriate data type (numeric); invalid values become NaN       
        self.df["salary"] = self.df["salary"].astype(str).str.replace("$", "").str.replace(",", "")  # Ensure values are strings before attempting to remove unnecessary characters so as to prevent cleaning/conversion errors
        self.df["salary"] = pd.to_numeric(self.df["salary"], errors="coerce")

        self.df["years_experience"] = pd.to_numeric(self.df["years_experience"], errors="coerce")
        self.df["satisfaction_score"] = pd.to_numeric(self.df["satisfaction_score"], errors="coerce")

        # Store values (used for comparison in later cleaning summary)             
        invalid_salaries = (self.df["salary"] < 0).sum()
        invalid_experience = ((self.df["years_experience"] < 0) | (self.df["years_experience"] > 50)).sum()
        invalid_scores = ((self.df["satisfaction_score"] < 1) | (self.df["satisfaction_score"] > 10)).sum() 


        # Convert "Impossible" Values to NaN
        self.df.loc[self.df["salary"] < 0, "salary"] = pd.NA  # Salary cannot be a negative number

        self.df.loc[(self.df["years_experience"] < 0) | (self.df["years_experience"] > 50), "years_experience"] = pd.NA  # Years of experience must be between 0 and 50

        self.df.loc[(self.df["satisfaction_score"] < 1) | (self.df["satisfaction_score"] > 10), "satisfaction_score"] = pd.NA  # Survey score must be between 1 and 10           

                 
        # Convert Survey Date to appropriate data type (datetime); invalid values become NaT      
        def normalize_date(date):

            """
            Internal function; cleans and normalizes Survey Dates before attempting conversion to datetime.

            Though some raw dates are ambiguous as to day/month, formats are interpreted as follows based on overarching patterns from the raw data: "DD-MM-YYYY", "MM/DD/YYYY", "YYYY-MM-DD".

            "DD-MM-YYYY" and "MM/DD/YYYY" are standardized to: "YYYY-MM-DD" for consistency and ease of later conversion using pandas; dates already as "YYYY-MM-DD" are left as-is.       

            """

            if pd.isna(date):  # Leaves missing dates as-is
                return date

            match = re.match(r'(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})', date)  # DD-MM-YYY

            if not match:
                match = re.match(r'(?P<month>\d{2})/(?P<day>\d{2})/(?P<year>\d{4})', date)  # MM/DD/YYY           
                    
            if match:
                date = f"{match.group('year')}-{match.group('month')}-{match.group('day')}"  # Reformat as YYYY-MM-DD

            return date
        
        missing_dates_before = self.df["survey_date"].isna().sum()  # Value needed for later cleaning summary
        self.df["survey_date"] = self.df["survey_date"].apply(normalize_date)  # Run normalization function over the raw data for Survey Date
        self.df["survey_date"] = pd.to_datetime(self.df["survey_date"], errors="coerce")  # Complete the conversion to datetime; includes error handling  
        invalid_dates = self.df["survey_date"].isna().sum() - missing_dates_before  # Value needed for later cleaning summary
       

        """
        Strategy for missing values:

        In that employee IDs are intended to be unique identifiers, rows with duplicated or missing IDs are removed.

        Otherwise, all rows with missing values in other columns are retained, with the missing values converted to NaN or NaT (respective to the data type). This is because the remaining data in the row may still be useful. For example, a missing salary may not impact the survey results as long as there is a satisfaction score and/or comment.

        I chose not to fill missing values with other data so as to not introduce inaccurate information (e.g. retain NaN instead of replacing it with an average salary); so as to streamline later calculations/analyses (e.g. retain NaN instead of replacing it with "Unknown" for salary); and for readability (e.g. leave blank comments as-is rather than replacing missing comments with "N/A").
        
        """

        # Print Cleaning Summary       
        print(f"\n{'=' * 5} Cleaning Summary {'=' * 5}\n")
        print(f"Original Rows: {original_rows}\n")
        print(f"Rows Removed (Whole): {dupe_rows_removed}\n")
        print(f"Rows Removed (Duplicate Employee IDs): {dupe_ids_removed}\n")
        print(f"Rows Removed (Missing Employee IDs): {missing_ids_removed}\n")
        print(f"Final Rows: {len(self.df)}\n\n")

        print(f"Invalid salaries converted to NaN: {invalid_salaries}\n")
        print(f"Invalid experience values converted to NaN: {invalid_experience}\n")
        print(f"Invalid satisfaction scores converted to NaN: {invalid_scores}\n")
        print(f"Invalid survey dates converted to NaT: {invalid_dates}\n")
        print(f"Final Total Missing Values: {self.df.isna().sum().sum()}")

        return self
        

    def analyze(self):
        """
        Computes summary statistics from the cleaned self.df - performs analyses and returns a summary dictionary.
        If the DataFrame is empty, the method does not attempt analysis; it prints a message and returns an empty dictionary.
        """

        if self.df.empty:  # Check for zero rows and/or zero columns
            print("DataFrame is empty. No data to analyze.")
            return {}

        avg_salary_by_dept = self.df.groupby("department")["salary"].mean().round(0)

        avg_sat_score_by_dept = self.df.groupby("department")["satisfaction_score"].mean().round(0)

        employees_per_office = self.df.groupby("office_location")["employee_id"].count()

        avg_sat_score_by_office = self.df.groupby("office_location")["satisfaction_score"].mean().round(0)        

        
        avg_sat_score_by_years_exp = (  # Group years of experience into bins before analysis for readability
            self.df.groupby(pd.cut(
                    self.df["years_experience"],
                    bins = [-1, 2, 5, 10, 15, 20, 30, 40, 50],  # Default is right = True -> left-exclusive, right-inclusive
                    labels = [
                        "0-2 years",
                        "3-5 years",
                        "6-10 years",
                        "11-15 years",
                        "16-20 years",
                        "21-30 years",
                        "31-40 years",
                        "41-50 years"
                    ]                    
            ))["satisfaction_score"].mean().round(0)
        )


        corr_data = self.df[["years_experience", "salary"]].dropna()  # Drop rows with missing values in Years of Experience and/or Salary columns before computing correlation for accurate, steamlined data processing
        salary_experience_corr = round(corr_data["years_experience"].corr(corr_data["salary"]), 2)

        return {
            "Average Salary by Department": avg_salary_by_dept,
            "Average Satisfaction Score by Department": avg_sat_score_by_dept,
            "Employee Count by Office": employees_per_office,
            "Average Satisfaction Score by Office": avg_sat_score_by_office,
            "Average Satisfaction Score by Years of Experience": avg_sat_score_by_years_exp,            
            "Correlation Strength Between Salary and Years of Experience (+1 = positive corr, 0 = little corr, -1 = negative corr )": salary_experience_corr            
        }
       

    def visualize(self, output_path="output/charts.png"):
        """
        Generates and saves visualizations as an image file.
        If the DataFrame is empty, the method does not attempt to produce visualizations; it prints a message and exits the method.
        """

        if self.df.empty:  # Check for zero rows and/or zero columns
            print("DataFrame is empty. No visualizations to generate.")
            return 

        fig, axes = plt.subplots(1, 5, figsize=(15, 5))

        # Chart 1: Average Salary by Department (Bar Chart)    
        avg_salary_by_dept = self.df.groupby("department")["salary"].mean().round(0)    
        axes[0].bar(avg_salary_by_dept.index, avg_salary_by_dept.values, color="darkgreen")  # Bar chart(x-axis, y-axis, bar color)
        axes[0].set_title("Avg Salary by Dept")
        axes[0].set_xlabel("Department")
        axes[0].set_ylabel("Average Salary")
        axes[0].tick_params(axis="x", rotation=45)  # Rotate x-axis labels 45 degrees for readability

        # Chart 2: Average Satisfaction Score by Department (Bar Chart)    
        avg_sat_score_by_dept = self.df.groupby("department")["satisfaction_score"].mean().round(0)  
        axes[1].bar(avg_sat_score_by_dept.index, avg_sat_score_by_dept.values, color="lightblue")  # Bar chart(x-axis, y-axis, bar color)
        axes[1].set_title("Avg Sat Score by Dept")
        axes[1].set_xlabel("Department")
        axes[1].set_ylabel("Average Satisfaction Score")
        axes[1].tick_params(axis="x", rotation=45)  # Rotate x-axis labels 45 degrees for readability

        # Chart 3: Average Satisfaction Score by Office Location (Bar Chart)    
        avg_sat_score_by_office = self.df.groupby("office_location")["satisfaction_score"].mean().round(0)    
        axes[2].bar(avg_sat_score_by_office.index, avg_sat_score_by_office.values, color="lavender")  # Bar chart(x-axis, y-axis, bar color)
        axes[2].set_title("Avg Sat Score by Office")
        axes[2].set_xlabel("Office Location")
        axes[2].set_ylabel("Average Satisfaction Score")
        axes[2].tick_params(axis="x", rotation=45)  # Rotate x-axis labels 45 degrees for readability

        # Chart 4: Satisfaction Score Distribution (Histogram)
        axes[3].hist(self.df["satisfaction_score"], bins=10, color="darkblue", alpha=0.7, edgecolor="black")  # Histogram(pull satisfaction score values, 10 bins for measurement/display, color, transparency, edge lines for readability)
        axes[3].set_title("Distribution of Satisfaction Scores")
        axes[3].set_xlabel("Satisfaction Scores")
        axes[3].set_ylabel("Frequency of Occurrence")

        # Chart 5: Trend of Satisfaction Scores by Years of Experience (Line Chart)
        avg_sat_score_by_years_exp = self.df.groupby("years_experience")["satisfaction_score"].mean().round(0)
        axes[4].plot(avg_sat_score_by_years_exp.index, avg_sat_score_by_years_exp.values, color="darkred")  # Line chart(x-axis, y-axis, line color)
        axes[4].set_title("Sat Scores by Years of Experience")
        axes[4].set_xlabel("Years of Experience")
        axes[4].set_ylabel("Satisfaction Score")
        axes[4].tick_params(axis="x", rotation=45)  # Rotate x-axis labels 45 degrees for readability

        plt.tight_layout()  # Prevents labels from being cut off
        plt.savefig(output_path, dpi=120, bbox_inches="tight")  # Save charts as image file, resolution, trim white space around the content        
        plt.close()


    def export(self, output_path="output/clean_employee_data.csv"):
        """Export the cleaned data to a new CSV file."""

        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Create directory if it does not already exist
            self.df.to_csv(output_path, index=False)  # Generate CSV with cleaned data; excludes DF index from CSV

        except OSError as err:
            print(f"Error when attempting to export data: {err}")


    def run(self):
        """Execute the full pipeline: clean → analyze → visualize → export."""

        output_dir = os.path.join(os.path.dirname(__file__), "output")
        chart_path = os.path.join(output_dir, "charts.png")
        data_path = os.path.join(output_dir, "clean_employee_data.csv")

        self.clean()
        results = self.analyze()
        self.visualize(chart_path)
        self.export(data_path)

        return results