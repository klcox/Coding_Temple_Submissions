import csv

# ============================================================
# FUNCTION 1: Load data from CSV
# ============================================================

def load_students(filepath: str) -> list[dict]:
    """
    Read student data from a CSV file.

    Each row becomes a dictionary. The CSV has columns:
    student_name, math, science, english, history

    Some cells may be empty strings (missing grades) — that's expected.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A list of dicts, one per student.
        Example: [{"student_name": "Alice", "math": "92", ...}, ...]

    Raises:
        FileNotFoundError: if the CSV file doesn't exist.
    """
    try: 
        
        with open(filepath, "r") as file:
            reader = csv.DictReader(file)

            student_data = []          

            for row in reader:
                student_data.append(row)
                
            return student_data

    except FileNotFoundError:
        print(f"Error: CSV file {filepath} not found.")          
        return []    

# ============================================================
# FUNCTION 2: Calculate average, handling missing values
# ============================================================

def calculate_average(grades: list) -> float | None:
    """
    Calculate the average of a list of grade values.

    Grade values may be strings (from the CSV), empty strings, or numbers.
    Ignore any value that can't be converted to a float.

    Args:
        grades: A list of values (e.g., ["92", "88", "", "79"]).

    Returns:
        The average as a float, rounded to 1 decimal place.
        Returns None if there are no valid grades.
    """     

    #Variables needed for calculating the average
    count = 0  #Number of grades
    total = 0  #Sum of grades

    for grade in grades:  #Loops through the list of student grades and updates the variables needed for calculation
        try:                       
            conv_grade = float(grade)
            count += 1
            total += conv_grade
        
        except ValueError: 
            continue  #Skips any values that cannot be converted to a float

    if count == 0: 
        return None  #Handles case where there are no valid grades; helps address zero division error when attempting to calculate average         
    
    average = total/count   
    return round(average, 1)        
        
# ============================================================
# FUNCTION 3: Assign letter grade
# ============================================================

def get_letter_grade(average: float | None) -> str:
    """
    Convert a numeric average to a letter grade.

    Scale:
        90+  → "A"
        80-89 → "B"
        70-79 → "C"
        60-69 → "D"
        < 60  → "F"
        None  → "N/A" (no grades available)

    Args:
        average: The numeric average, or None.

    Returns:
        The letter grade as a string.
    """
    if average is None:
        return "N/A"
    elif average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"
       
# ============================================================
# FUNCTION 4: Generate summary report
# ============================================================

def generate_report(students: list[dict]) -> dict:
    """
    Generate a class summary report.

    Args:
        students: The list of student dicts from load_students().

    Returns:
        A dict with these keys:
            "total_students":   int — how many students
            "class_average":    float — average of all valid averages
            "highest_average":  float — the best average
            "lowest_average":   float — the lowest average
            "grade_distribution": dict — {"A": 3, "B": 5, ...}
            "students":         list of dicts, each with:
                                  name, average, grade
    """
    
    #Initialized variables needed for later use
    total_students = len(students)
    class_averages = []    
    grade_dist = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "F": 0,
        "N/A": 0
    }
    student_summary = []
    
    for student in students:
        student_grades = [  #Loops through each dictionary and creates a list of grades per student
            student["math"],
            student["science"],
            student["english"],
            student["history"]
        ]
      
        student_ave = calculate_average(student_grades)  #Uses the above list and calls a previous function to calculate the average per student
        if student_ave is not None:
            class_averages.append(student_ave)  #Adds only numeric values to the class averages list to prevent later calculation errors

        student_letter_grade = get_letter_grade(student_ave)  #Uses the student average calculated above and calls a previous function to determine the letter grade per student
        grade_dist[student_letter_grade] += 1  #Updates the grade distribuion dictionary according to letter grade
        
        student_summary.append({  #Creates a new dictionary per student within the student_summary list
            "name": student['student_name'],
            "average": student_ave,
            "grade": student_letter_grade
        })
    
    if class_averages:  #If the list is not empty, proceeds with the below calculations
        class_average = round((sum(class_averages)/len(class_averages)), 1)
        highest_average = max(class_averages)
        lowest_average = min(class_averages)
    else:  #Otherwise, if the list is empty, returns None for each value
        class_average = None
        highest_average = None
        lowest_average = None

    return {  #Returns a dictionary with the following keys/values
        "total_students": total_students,
        "class_average": class_average,
        "highest_average": highest_average,
        "lowest_average": lowest_average,
        "grade_distribution": grade_dist,
        "students": student_summary
    }
    
# ============================================================
# FUNCTION 5: Write report to a file
# ============================================================

def write_report(report: dict, filepath: str) -> None:
    """
    Write the summary report to a text file.

    Format example:
        ===========================
        STUDENT GRADE REPORT
        ===========================
        Total students: 15
        Class average:  81.3
        Highest average: 95.0
        Lowest average:  55.0

        Grade Distribution:
          A: 5
          B: 4
          ...

        Individual Results:
          Alice Johnson    Avg: 91.5  Grade: A
          ...

    Args:
        report:   The dict returned by generate_report().
        filepath: Path to write the report file.
    """
   
    with open(filepath, "w") as file:
        file.write(f"{'=' * 30} \nSTUDENT GRADE REPORT\n{'=' * 30}\n")

        file.write(f"Total Students: {report['total_students']}")

        if report["class_average"] is not None:  #Formats class average for later printing/writing
            class_avg = f"{report['class_average']:.1f}"
        else:
            class_avg = "N/A"
        file.write(f"\nClass Average: {class_avg}")

        if report["highest_average"] is not None:  #Formats highest average for later printing/writing
            highest_avg = f"{report['highest_average']:.1f}"
        else:
            highest_avg = "N/A"
        file.write(f"\nHighest Average: {highest_avg}")

        if report["lowest_average"] is not None:  #Formats lowest average for later printing/writing
            lowest_avg = f"{report['lowest_average']:.1f}"
        else:
            lowest_avg = "N/A"
        file.write(f"\nLowest Average: {lowest_avg}\n\n")

        file.write("Grade Distribution:\n")
        for grade, count in report['grade_distribution'].items():  #Loops through grade_distribution dictionary and produces the letter grades along with the associated counts
            file.write(f"{grade}: {count}\n")

        file.write("\nIndividual Results:\n")       
        for student in report['students']:  #Loops through the list of student dictionaries in order to produce a summary by student
            if student["average"] is not None:  #Formats student average for later printing/writing
                student_avg = f"{student['average']:.1f}"
            else:
                student_avg = "N/A"
            file.write(f"{student['name']:<18} Avg: {student_avg:<10} Grade: {student['grade']}\n")


# ============================================================
# MAIN — do not modify
# ============================================================

def main():
    print("Loading student data...")
    students = load_students("data/students.csv")
    print(f"Loaded {len(students)} students.")

    print("Generating report...")
    report = generate_report(students)

    print("\n--- Summary ---")
    print(f"Total students:   {report['total_students']}")
    print(f"Class average:    {report['class_average']}")
    print(f"Highest average:  {report['highest_average']}")
    print(f"Lowest average:   {report['lowest_average']}")

    print("\nGrade Distribution:")
    for grade, count in sorted(report["grade_distribution"].items()):
        print(f"  {grade}: {count}")

    print("\nTop 5 students:")
    sorted_students = sorted(
        [s for s in report["students"] if s["average"] is not None],
        key=lambda s: s["average"],
        reverse=True
    )
    for s in sorted_students[:5]:
        print(f"  {s['name']:<20} {s['average']:.1f}  ({s['grade']})")

    write_report(report, "grade_report.txt")
    print("\nReport written to grade_report.txt")


if __name__ == "__main__":
    main()