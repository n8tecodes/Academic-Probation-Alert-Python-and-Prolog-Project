from pyswip import Prolog
import mysql.connector
import tkinter as tk
from tkinter import messagebox

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

# Function to add a new student to the database
def add_student(conn, student_id, student_name, student_email, school, programme):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO StudentMaster (student_id, student_name, student_email, school, programme)
            VALUES (%s, %s, %s, %s, %s);
        """, (student_id, student_name, student_email, school, programme))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to add student: {err}")
    finally:
        cursor.close()

# GUI Class
class AcademicProbationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Academic Probation System")
        self.root.geometry("600x500")  # Set window size

        self.conn = connect_to_database()
        if not self.conn:
            messagebox.showerror("Error", "Failed to connect to the database.")
            return

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.role_label = tk.Label(self.main_frame, text="Are you an 'admin' or a 'student'?", font=("Arial", 14))
        self.role_label.pack(pady=10)

        self.role_entry = tk.Entry(self.main_frame, font=("Arial", 12))
        self.role_entry.pack(pady=5)

        self.submit_role_button = tk.Button(self.main_frame, text="Submit", command=self.submit_role, font=("Arial", 12))
        self.submit_role_button.pack(pady=10)

    def submit_role(self):
        role = self.role_entry.get().strip().lower()
        if role == "student":
            self.student_interface()
        elif role == "admin":
            self.admin_interface()
        else:
            messagebox.showerror("Error", "Invalid role. Please enter 'admin' or 'student'.")

    def student_interface(self):
        self.clear_widgets()

        self.student_frame = tk.Frame(self.root, padx=10, pady=10)
        self.student_frame.pack(fill=tk.BOTH, expand=True)

        self.student_id_label = tk.Label(self.student_frame, text="Enter your Student ID:", font=("Arial", 14))
        self.student_id_label.pack(pady=10)

        self.student_id_entry = tk.Entry(self.student_frame, font=("Arial", 12))
        self.student_id_entry.pack(pady=5)

        self.year_label = tk.Label(self.student_frame, text="Enter the academic year:", font=("Arial", 14))
        self.year_label.pack(pady=10)

        self.year_entry = tk.Entry(self.student_frame, font=("Arial", 12))
        self.year_entry.pack(pady=5)

        self.submit_student_button = tk.Button(self.student_frame, text="Submit", command=self.check_student_status, font=("Arial", 12))
        self.submit_student_button.pack(pady=10)

    def admin_interface(self):
        self.clear_widgets()

        self.admin_frame = tk.Frame(self.root, padx=10, pady=10)
        self.admin_frame.pack(fill=tk.BOTH, expand=True)

        self.update_threshold_label = tk.Label(self.admin_frame, text="Would you like to update the default GPA threshold? (yes/no):", font=("Arial", 14))
        self.update_threshold_label.pack(pady=10)

        self.update_threshold_entry = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.update_threshold_entry.pack(pady=5)

        self.submit_update_button = tk.Button(self.admin_frame, text="Submit", command=self.update_threshold, font=("Arial", 12))
        self.submit_update_button.pack(pady=10)

        self.student_id_label = tk.Label(self.admin_frame, text="Enter Student ID to check GPA:", font=("Arial", 14))
        self.student_id_label.pack(pady=10)

        self.student_id_entry = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.student_id_entry.pack(pady=5)

        self.year_label = tk.Label(self.admin_frame, text="Enter the academic year:", font=("Arial", 14))
        self.year_label.pack(pady=10)

        self.year_entry = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.year_entry.pack(pady=5)

        self.submit_admin_button = tk.Button(self.admin_frame, text="Submit", command=self.check_student_status, font=("Arial", 12))
        self.submit_admin_button.pack(pady=10)

        self.add_student_label = tk.Label(self.admin_frame, text="Add a new student:", font=("Arial", 14))
        self.add_student_label.pack(pady=10)

        self.new_student_id_label = tk.Label(self.admin_frame, text="Student ID:", font=("Arial", 12))
        self.new_student_id_label.pack(pady=5)
        self.new_student_id_entry = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.new_student_id_entry.pack(pady=5)

        self.new_student_name_label = tk.Label(self.admin_frame, text="Student Name:", font=("Arial", 12))
        self.new_student_name_label.pack(pady=5)
        self.new_student_name_entry = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.new_student_name_entry.pack(pady=5)

        self.new_student_email_label = tk.Label(self.admin_frame, text="Student Email:", font=("Arial", 12))
        self.new_student_email_label.pack(pady=5)
        self.new_student_email_entry = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.new_student_email_entry.pack(pady=5)

        self.new_student_school_label = tk.Label(self.admin_frame, text="School:", font=("Arial", 12))
        self.new_student_school_label.pack(pady=5)
        self.new_student_school_entry = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.new_student_school_entry.pack(pady=5)

        self.new_student_programme_label = tk.Label(self.admin_frame, text="Programme:", font=("Arial", 12))
        self.new_student_programme_label.pack(pady=5)
        self.new_student_programme_entry = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.new_student_programme_entry.pack(pady=5)

        self.add_student_button = tk.Button(self.admin_frame, text="Add Student", command=self.add_student, font=("Arial", 12))
        self.add_student_button.pack(pady=10)

    def update_threshold(self):
        action = self.update_threshold_entry.get().strip().lower()
        if action == "yes":
            try:
                new_threshold = float(input("Enter the new GPA threshold (e.g., 2.5): ").strip())
                update_gpa_threshold(new_threshold)
                messagebox.showinfo("Success", f"Default GPA threshold updated to {new_threshold}.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a numeric GPA threshold.")

    def check_student_status(self):
        student_id = self.student_id_entry.get().strip()
        year = self.year_entry.get().strip()
        semester1_gpa, semester2_gpa, cumulative_gpa, on_probation = check_student_academic_probation(self.conn, student_id, year)
        status = "on academic probation" if on_probation else "in good standing"
        messagebox.showinfo("GPA Status", f"Student {student_id}'s Semester 1 GPA is {semester1_gpa}, Semester 2 GPA is {semester2_gpa}, Cumulative GPA is {cumulative_gpa}. They are {status}.")

    def add_student(self):
        student_id = self.new_student_id_entry.get().strip()
        student_name = self.new_student_name_entry.get().strip()
        student_email = self.new_student_email_entry.get().strip()
        school = self.new_student_school_entry.get().strip()
        programme = self.new_student_programme_entry.get().strip()

        if not (student_id and student_name and student_email and school and programme):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            student_id = int(student_id)
        except ValueError:
            messagebox.showerror("Error", "Student ID must be an integer.")
            return

        add_student(self.conn, student_id, student_name, student_email, school, programme)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Main function
def main():
    root = tk.Tk()
    app = AcademicProbationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()