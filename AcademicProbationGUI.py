import tkinter as tk
from tkinter import messagebox

from Database import Database
from PrologInterface import PrologInterface

class AcademicProbationGUI:
    def __init__(self, root, db, prolog_interface):
        self.root = root
        self.db = db
        self.prolog_interface = prolog_interface
        self.root.title("Academic Probation System")
        self.root.geometry("600x500")
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
                self.prolog_interface.update_gpa_threshold(new_threshold)
                messagebox.showinfo("Success", f"Default GPA threshold updated to {new_threshold}.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a numeric GPA threshold.")

    def check_student_status(self):
        student_id = self.student_id_entry.get().strip()
        year = self.year_entry.get().strip()
        grades = self.db.get_student_grades(student_id, year)

        semester1_grade_points = []
        semester1_credits = []
        semester2_grade_points = []
        semester2_credits = []

        for row in grades:
            if row['semester'] == 1:
                semester1_grade_points.append(row['grade_points'] * row['credits'])
                semester1_credits.append(row['credits'])
            elif row['semester'] == 2:
                semester2_grade_points.append(row['grade_points'] * row['credits'])
                semester2_credits.append(row['credits'])

        semester1_gpa = self.prolog_interface.calculate_gpa(semester1_grade_points, semester1_credits) if semester1_grade_points and semester1_credits else None
        semester2_gpa = self.prolog_interface.calculate_gpa(semester2_grade_points, semester2_credits) if semester2_grade_points and semester2_credits else None

        all_grade_points = semester1_grade_points + semester2_grade_points
        all_credits = semester1_credits + semester2_credits
        cumulative_gpa = self.prolog_interface.calculate_cumulative_gpa(all_grade_points, all_credits) if all_grade_points and all_credits else None

        on_probation = self.prolog_interface.check_academic_probation(cumulative_gpa) if cumulative_gpa is not None else False
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

        self.db.add_student(student_id, student_name, student_email, school, programme)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Main function
def main():
    root = tk.Tk()
    db = Database(host="localhost", user="root", password="Abc123@!", database="academicprobationsystem")
    prolog_interface = PrologInterface(prolog_file="gpa_calculator.pl")
    app = AcademicProbationGUI(root, db, prolog_interface)
    root.mainloop()

if __name__ == "__main__":
    main()