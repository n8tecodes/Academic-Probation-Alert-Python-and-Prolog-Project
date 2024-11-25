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