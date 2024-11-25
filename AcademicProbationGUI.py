import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from Database import Database
from PrologInterface import PrologInterface

class AcademicProbationGUI:
    def __init__(self, root, db, prolog_interface):
        self.root = root
        self.db = db
        self.prolog_interface = prolog_interface
        self.root.title("Academic Probation System")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.create_student_tab()
        self.create_admin_tab()

    def create_student_tab(self):
        self.student_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.student_frame, text="Student")

        ttk.Label(self.student_frame, text="Enter your Student ID:", font=("Arial", 14)).pack(pady=10)
        self.student_id_entry = ttk.Entry(self.student_frame, font=("Arial", 12))
        self.student_id_entry.pack(pady=5)

        ttk.Label(self.student_frame, text="Enter the academic year:", font=("Arial", 14)).pack(pady=10)
        self.year_entry = ttk.Entry(self.student_frame, font=("Arial", 12))
        self.year_entry.pack(pady=5)

        ttk.Button(self.student_frame, text="Submit", command=self.check_student_status, style="TButton").pack(pady=10)

    def create_admin_tab(self):
        self.admin_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.admin_frame, text="Admin")

        self.admin_notebook = ttk.Notebook(self.admin_frame)
        self.admin_notebook.pack(expand=True, fill='both')

        self.create_student_management_tab()
        self.create_module_management_tab()
        self.create_module_details_management_tab()

    def create_student_management_tab(self):
        self.student_management_frame = ttk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.student_management_frame, text="Manage Students")

        ttk.Label(self.student_management_frame, text="Student ID:", font=("Arial", 12)).pack(pady=5)
        self.new_student_id_entry = ttk.Entry(self.student_management_frame, font=("Arial", 12))
        self.new_student_id_entry.pack(pady=5)

        ttk.Label(self.student_management_frame, text="Student Name:", font=("Arial", 12)).pack(pady=5)
        self.new_student_name_entry = ttk.Entry(self.student_management_frame, font=("Arial", 12))
        self.new_student_name_entry.pack(pady=5)

        ttk.Label(self.student_management_frame, text="Student Email:", font=("Arial", 12)).pack(pady=5)
        self.new_student_email_entry = ttk.Entry(self.student_management_frame, font=("Arial", 12))
        self.new_student_email_entry.pack(pady=5)

        ttk.Label(self.student_management_frame, text="School:", font=("Arial", 12)).pack(pady=5)
        self.new_student_school_entry = ttk.Entry(self.student_management_frame, font=("Arial", 12))
        self.new_student_school_entry.pack(pady=5)

        ttk.Label(self.student_management_frame, text="Programme:", font=("Arial", 12)).pack(pady=5)
        self.new_student_programme_entry = ttk.Entry(self.student_management_frame, font=("Arial", 12))
        self.new_student_programme_entry.pack(pady=5)

        ttk.Button(self.student_management_frame, text="Add Student", command=self.add_student, style="TButton").pack(pady=10)
        ttk.Button(self.student_management_frame, text="View Students", command=self.view_students, style="TButton").pack(pady=10)
        ttk.Button(self.student_management_frame, text="Update Student", command=self.update_student, style="TButton").pack(pady=10)
        ttk.Button(self.student_management_frame, text="Delete Student", command=self.delete_student, style="TButton").pack(pady=10)

    def create_module_management_tab(self):
        self.module_management_frame = ttk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.module_management_frame, text="Manage Modules")

        ttk.Label(self.module_management_frame, text="Module Code:", font=("Arial", 12)).pack(pady=5)
        self.module_code_entry = ttk.Entry(self.module_management_frame, font=("Arial", 12))
        self.module_code_entry.pack(pady=5)

        ttk.Label(self.module_management_frame, text="Module Name:", font=("Arial", 12)).pack(pady=5)
        self.module_name_entry = ttk.Entry(self.module_management_frame, font=("Arial", 12))
        self.module_name_entry.pack(pady=5)

        ttk.Label(self.module_management_frame, text="Credits:", font=("Arial", 12)).pack(pady=5)
        self.credits_entry = ttk.Entry(self.module_management_frame, font=("Arial", 12))
        self.credits_entry.pack(pady=5)

        ttk.Button(self.module_management_frame, text="Add Module", command=self.add_module, style="TButton").pack(pady=10)
        ttk.Button(self.module_management_frame, text="View Modules", command=self.view_modules, style="TButton").pack(pady=10)
        ttk.Button(self.module_management_frame, text="Update Module", command=self.update_module, style="TButton").pack(pady=10)
        ttk.Button(self.module_management_frame, text="Delete Module", command=self.delete_module, style="TButton").pack(pady=10)

    def create_module_details_management_tab(self):
        self.module_details_management_frame = ttk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.module_details_management_frame, text="Manage Module Details")

        ttk.Label(self.module_details_management_frame, text="Detail ID:", font=("Arial", 12)).pack(pady=5)
        self.detail_id_entry = ttk.Entry(self.module_details_management_frame, font=("Arial", 12))
        self.detail_id_entry.pack(pady=5)

        ttk.Label(self.module_details_management_frame, text="Student ID:", font=("Arial", 12)).pack(pady=5)
        self.student_id_entry = ttk.Entry(self.module_details_management_frame, font=("Arial", 12))
        self.student_id_entry.pack(pady=5)

        ttk.Label(self.module_details_management_frame, text="Module Code:", font=("Arial", 12)).pack(pady=5)
        self.module_code_entry = ttk.Entry(self.module_details_management_frame, font=("Arial", 12))
        self.module_code_entry.pack(pady=5)

        ttk.Label(self.module_details_management_frame, text="Year:", font=("Arial", 12)).pack(pady=5)
        self.year_entry = ttk.Entry(self.module_details_management_frame, font=("Arial", 12))
        self.year_entry.pack(pady=5)

        ttk.Label(self.module_details_management_frame, text="Semester:", font=("Arial", 12)).pack(pady=5)
        self.semester_entry = ttk.Entry(self.module_details_management_frame, font=("Arial", 12))
        self.semester_entry.pack(pady=5)

        ttk.Label(self.module_details_management_frame, text="Grade Points:", font=("Arial", 12)).pack(pady=5)
        self.grade_points_entry = ttk.Entry(self.module_details_management_frame, font=("Arial", 12))
        self.grade_points_entry.pack(pady=5)

        ttk.Button(self.module_details_management_frame, text="Add Module Detail", command=self.add_module_detail, style="TButton").pack(pady=10)
        ttk.Button(self.module_details_management_frame, text="View Module Details", command=self.view_module_details, style="TButton").pack(pady=10)
        ttk.Button(self.module_details_management_frame, text="Update Module Detail", command=self.update_module_detail, style="TButton").pack(pady=10)
        ttk.Button(self.module_details_management_frame, text="Delete Module Detail", command=self.delete_module_detail, style="TButton").pack(pady=10)

    def update_threshold(self):
        action = self.update_threshold_entry.get().strip().lower()
        if action == "yes":
            new_threshold = simpledialog.askfloat("Input", "Enter the new GPA threshold (e.g., 2.5):")
            if new_threshold is not None:
                self.prolog_interface.update_gpa_threshold(new_threshold)
                messagebox.showinfo("Success", f"Default GPA threshold updated to {new_threshold}.")

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

    def view_students(self):
        students = self.db.read_students()
        student_list = "\n".join([f"{student['student_id']}: {student['student_name']} ({student['student_email']}, {student['school']}, {student['programme']})" for student in students])
        messagebox.showinfo("Students", student_list)

    def update_student(self):
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

        self.db.update_student(student_id, student_name, student_email, school, programme)

    def delete_student(self):
        student_id = self.new_student_id_entry.get().strip()

        if not student_id:
            messagebox.showerror("Error", "Student ID is required.")
            return

        try:
            student_id = int(student_id)
        except ValueError:
            messagebox.showerror("Error", "Student ID must be an integer.")
            return

        self.db.delete_student(student_id)

    def add_module(self):
        module_code = self.module_code_entry.get().strip()
        module_name = self.module_name_entry.get().strip()
        credits = self.credits_entry.get().strip()

        if not (module_code and module_name and credits):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            credits = int(credits)
        except ValueError:
            messagebox.showerror("Error", "Credits must be an integer.")
            return

        self.db.add_module(module_code, module_name, credits)

    def view_modules(self):
        modules = self.db.read_modules()
        module_list = "\n".join([f"{module['module_code']}: {module['module_name']} ({module['credits']} credits)" for module in modules])
        messagebox.showinfo("Modules", module_list)

    def update_module(self):
        module_code = self.module_code_entry.get().strip()
        module_name = self.module_name_entry.get().strip()
        credits = self.credits_entry.get().strip()

        if not (module_code and module_name and credits):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            credits = int(credits)
        except ValueError:
            messagebox.showerror("Error", "Credits must be an integer.")
            return

        self.db.update_module(module_code, module_name, credits)

    def delete_module(self):
        module_code = self.module_code_entry.get().strip()

        if not module_code:
            messagebox.showerror("Error", "Module Code is required.")
            return

        self.db.delete_module(module_code)

    def add_module_detail(self):
        student_id = self.student_id_entry.get().strip()
        module_code = self.module_code_entry.get().strip()
        year = self.year_entry.get().strip()
        semester = self.semester_entry.get().strip()
        grade_points = self.grade_points_entry.get().strip()

        if not (student_id and module_code and year and semester and grade_points):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            student_id = int(student_id)
            year = int(year)
            semester = int(semester)
            grade_points = float(grade_points)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Ensure Student ID, Year, and Semester are integers, and Grade Points is a float.")
            return

        self.db.add_module_detail(student_id, module_code, year, semester, grade_points)

    def view_module_details(self):
        module_details = self.db.read_module_details()
        details_list = "\n".join([f"ID: {detail['id']}, Student ID: {detail['student_id']}, Module Code: {detail['module_code']}, Year: {detail['year']}, Semester: {detail['semester']}, Grade Points: {detail['grade_points']}" for detail in module_details])
        messagebox.showinfo("Module Details", details_list)

    def update_module_detail(self):
        detail_id = self.detail_id_entry.get().strip()
        student_id = self.student_id_entry.get().strip()
        module_code = self.module_code_entry.get().strip()
        year = self.year_entry.get().strip()
        semester = self.semester_entry.get().strip()
        grade_points = self.grade_points_entry.get().strip()

        if not (detail_id and student_id and module_code and year and semester and grade_points):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            detail_id = int(detail_id)
            student_id = int(student_id)
            year = int(year)
            semester = int(semester)
            grade_points = float(grade_points)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Ensure Detail ID, Student ID, Year, and Semester are integers, and Grade Points is a float.")
            return

        self.db.update_module_detail(detail_id, student_id, module_code, year, semester, grade_points)

    def delete_module_detail(self):
        detail_id = self.detail_id_entry.get().strip()

        if not detail_id:
            messagebox.showerror("Error", "Detail ID is required.")
            return

        try:
            detail_id = int(detail_id)
        except ValueError:
            messagebox.showerror("Error", "Detail ID must be an integer.")
            return

        self.db.delete_module_detail(detail_id)

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