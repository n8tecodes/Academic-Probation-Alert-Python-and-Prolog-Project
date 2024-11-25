import mysql.connector
from tkinter import messagebox

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = self.connect_to_database()

    def connect_to_database(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    # CRUD operations for StudentMaster
    def add_student(self, student_id, student_name, student_email, school, programme):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO StudentMaster (student_id, student_name, student_email, school, programme)
                VALUES (%s, %s, %s, %s, %s);
            """, (student_id, student_name, student_email, school, programme))
            self.conn.commit()
            messagebox.showinfo("Success", "Student added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add student: {err}")
        finally:
            cursor.close()

    def read_students(self):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM StudentMaster;")
        students = cursor.fetchall()
        cursor.close()
        return students

    def update_student(self, student_id, student_name, student_email, school, programme):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE StudentMaster
                SET student_name = %s, student_email = %s, school = %s, programme = %s
                WHERE student_id = %s;
            """, (student_name, student_email, school, programme, student_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Student updated successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update student: {err}")
        finally:
            cursor.close()

    def delete_student(self, student_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM StudentMaster WHERE student_id = %s;", (student_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete student: {err}")
        finally:
            cursor.close()

    # CRUD operations for ModuleMaster
    def add_module(self, module_code, module_name, credits):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO ModuleMaster (module_code, module_name, credits)
                VALUES (%s, %s, %s);
            """, (module_code, module_name, credits))
            self.conn.commit()
            messagebox.showinfo("Success", "Module added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add module: {err}")
        finally:
            cursor.close()

    def read_modules(self):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ModuleMaster;")
        modules = cursor.fetchall()
        cursor.close()
        return modules

    def update_module(self, module_code, module_name, credits):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE ModuleMaster
                SET module_name = %s, credits = %s
                WHERE module_code = %s;
            """, (module_name, credits, module_code))
            self.conn.commit()
            messagebox.showinfo("Success", "Module updated successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update module: {err}")
        finally:
            cursor.close()

    def delete_module(self, module_code):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM ModuleMaster WHERE module_code = %s;", (module_code,))
            self.conn.commit()
            messagebox.showinfo("Success", "Module deleted successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete module: {err}")
        finally:
            cursor.close()

    # CRUD operations for ModuleDetails
    def add_module_detail(self, student_id, module_code, year, semester, grade_points):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO ModuleDetails (student_id, module_code, year, semester, grade_points)
                VALUES (%s, %s, %s, %s, %s);
            """, (student_id, module_code, year, semester, grade_points))
            self.conn.commit()
            messagebox.showinfo("Success", "Module detail added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add module detail: {err}")
        finally:
            cursor.close()

    def read_module_details(self):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ModuleDetails;")
        module_details = cursor.fetchall()
        cursor.close()
        return module_details

    def update_module_detail(self, id, student_id, module_code, year, semester, grade_points):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE ModuleDetails
                SET student_id = %s, module_code = %s, year = %s, semester = %s, grade_points = %s
                WHERE id = %s;
            """, (student_id, module_code, year, semester, grade_points, id))
            self.conn.commit()
            messagebox.showinfo("Success", "Module detail updated successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update module detail: {err}")
        finally:
            cursor.close()

    def delete_module_detail(self, id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM ModuleDetails WHERE id = %s;", (id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Module detail deleted successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete module detail: {err}")
        finally:
            cursor.close()

    def get_student_grades(self, student_id, year):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.grade_points, m.credits, d.semester
            FROM ModuleDetails d
            JOIN ModuleMaster m ON d.module_code = m.module_code
            WHERE d.student_id = %s AND d.year = %s;
        """, (student_id, year))
        grades = cursor.fetchall()
        cursor.close()
        return grades