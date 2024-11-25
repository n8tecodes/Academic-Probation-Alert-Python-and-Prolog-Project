# from pyswip import Prolog
# import mysql.connector

# # Database connection function
# def connect_to_database():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="Abc123@!",
#             database="academicprobationsystem"
#         )
#         return conn
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         return None

# # Initialize Prolog
# prolog = Prolog()
# prolog.consult("gpa_calculator.pl")  # Load the Prolog file

# # Function to retrieve GPA data for the student and check for academic probation
# def check_student_academic_probation(conn, student_id, year, semester=None):
#     cursor = conn.cursor(dictionary=True)

#     # Fetch grade points and credits based on student, year, and semester
#     if semester:
#         query = """
#             SELECT m.credits, d.grade_points
#             FROM ModuleDetails d
#             JOIN ModuleMaster m ON d.module_code = m.module_code
#             WHERE d.student_id = %s AND d.year = %s AND d.semester = %s;
#         """
#         cursor.execute(query, (student_id, year, semester))
#     else:
#         query = """
#             SELECT m.credits, d.grade_points
#             FROM ModuleDetails d
#             JOIN ModuleMaster m ON d.module_code = m.module_code
#             WHERE d.student_id = %s AND d.year = %s;
#         """
#         cursor.execute(query, (student_id, year))

#     # Prepare lists for grade points and credits
#     grade_points = []
#     credits = []
#     for row in cursor:
#         grade_points.append(row['credits'] * row['grade_points'])
#         credits.append(row['credits'])

#     cursor.close()

#     # Send data to Prolog for GPA calculation and probation check
#     result = list(prolog.query(f"calculate_gpa({grade_points}, {credits}, GPA)"))
#     gpa = result[0]['GPA'] if result else None

#     # Check academic probation using Prolog rule
#     probation_result = list(prolog.query(f"academic_probation({student_id}, GPA)"))
#     on_probation = bool(probation_result)

#     return gpa, on_probation

# # Main function
# def main():
#     conn = connect_to_database()
#     if not conn:
#         return

#     print("Welcome to the Academic Probation System")
#     role = input("Are you an 'admin' or a 'student'? ").strip().lower()

#     if role == "student":
#         student_id = input("Enter your Student ID: ").strip()
#         year = input("Enter the academic year: ").strip()
#         semester = input("Enter the semester (1 or 2), or press Enter for cumulative GPA: ").strip()
#         semester = int(semester) if semester else None
#         gpa, on_probation = check_student_academic_probation(conn, student_id, year, semester)
#         status = "on academic probation" if on_probation else "in good standing"
#         print(f"Your GPA is {gpa:.2f}. You are {status}.")

#     elif role == "admin":
#         student_id = input("Enter Student ID to check GPA: ").strip()
#         year = input("Enter the academic year: ").strip()
#         semester = input("Enter the semester (1 or 2), or press Enter for cumulative GPA: ").strip()
#         semester = int(semester) if semester else None
#         gpa, on_probation = check_student_academic_probation(conn, student_id, year, semester)
#         status = "on academic probation" if on_probation else "in good standing"
#         print(f"Student {student_id}'s GPA is {gpa:.2f}. They are {status}.")

#     conn.close()

# if __name__ == "__main__":
#     main()






from pyswip import Prolog
import mysql.connector

# Database connection function
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Abc123@!",
            database="academicprobationsystem"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Initialize Prolog
prolog = Prolog()
prolog.consult("gpa_calculator.pl")  # Load the Prolog file

# Function to update the default GPA threshold in Prolog
def update_gpa_threshold(new_threshold):
    # Remove any existing default_gpa_threshold facts
    prolog.query("retractall(default_gpa_threshold(_))")
    # Assert the new GPA threshold
    prolog.assertz(f"default_gpa_threshold({new_threshold})")
    print(f"Default GPA threshold updated to {new_threshold} in Prolog.")

# Function to calculate GPA and check probation status
def check_student_academic_probation(conn, student_id, year):
    cursor = conn.cursor(dictionary=True)

    # Retrieve grade points and credits for each semester from the database
    cursor.execute("""
        SELECT d.grade_points, m.credits, d.semester
        FROM ModuleDetails d
        JOIN ModuleMaster m ON d.module_code = m.module_code
        WHERE d.student_id = %s AND d.year = %s;
    """, (student_id, year))

    semester1_grade_points = []
    semester1_credits = []
    semester2_grade_points = []
    semester2_credits = []

    # Populate grade points and credits lists for each semester
    for row in cursor:
        if row['semester'] == 1:
            semester1_grade_points.append(row['grade_points'] * row['credits'])
            semester1_credits.append(row['credits'])
        elif row['semester'] == 2:
            semester2_grade_points.append(row['grade_points'] * row['credits'])
            semester2_credits.append(row['credits'])

    cursor.close()

    # Calculate semester GPAs using Prolog
    semester1_gpa = None
    if semester1_grade_points and semester1_credits:
        result = list(prolog.query(f"calculate_gpa_by_semester({semester1_grade_points}, {semester1_credits}, GPA)"))
        semester1_gpa = result[0]['GPA'] if result else None

    semester2_gpa = None
    if semester2_grade_points and semester2_credits:
        result = list(prolog.query(f"calculate_gpa_by_semester({semester2_grade_points}, {semester2_credits}, GPA)"))
        semester2_gpa = result[0]['GPA'] if result else None

    # Calculate cumulative GPA using Prolog
    all_grade_points = semester1_grade_points + semester2_grade_points
    all_credits = semester1_credits + semester2_credits
    cumulative_gpa = None
    if all_grade_points and all_credits:
        result = list(prolog.query(f"calculate_cumulative_gpa({all_grade_points}, {all_credits}, CumulativeGPA)"))
        cumulative_gpa = result[0]['CumulativeGPA'] if result else None

    # Check academic probation status using cumulative GPA
    if cumulative_gpa is not None:
        probation_query = list(prolog.query(f"academic_probation({cumulative_gpa})"))
        on_probation = bool(probation_query)
    else:
        on_probation = False

    return semester1_gpa, semester2_gpa, cumulative_gpa, on_probation

# Main function
def main():
    conn = connect_to_database()
    if not conn:
        return

    print("Welcome to the Academic Probation System")
    role = input("Are you an 'admin' or a 'student'? ").strip().lower()

    if role == "student":
        student_id = input("Enter your Student ID: ").strip()
        year = input("Enter the academic year: ").strip()
        semester1_gpa, semester2_gpa, cumulative_gpa, on_probation = check_student_academic_probation(conn, student_id, year)
        status = "on academic probation" if on_probation else "in good standing"
        print(f"Your Semester 1 GPA is {semester1_gpa}, Semester 2 GPA is {semester2_gpa}, Cumulative GPA is {cumulative_gpa}. You are {status}.")

    elif role == "admin":
        # Option for admin to update the default GPA threshold
        action = input("Would you like to update the default GPA threshold? (yes/no): ").strip().lower()
        if action == "yes":
            try:
                new_threshold = float(input("Enter the new GPA threshold (e.g., 2.5): ").strip())
                update_gpa_threshold(new_threshold)
            except ValueError:
                print("Invalid input. Please enter a numeric GPA threshold.")

        # Option for admin to check a student's GPA and probation status
        student_id = input("Enter Student ID to check GPA: ").strip()
        year = input("Enter the academic year: ").strip()
        semester1_gpa, semester2_gpa, cumulative_gpa, on_probation = check_student_academic_probation(conn, student_id, year)
        status = "on academic probation" if on_probation else "in good standing"
        print(f"Student {student_id}'s Semester 1 GPA is {semester1_gpa}, Semester 2 GPA is {semester2_gpa}, Cumulative GPA is {cumulative_gpa}. They are {status}.")

    conn.close()

if __name__ == "__main__":
    main()

