from pyswip import Prolog

class PrologInterface:
    def __init__(self, prolog_file):
        self.prolog = Prolog()
        self.prolog.consult(prolog_file)

    def update_gpa_threshold(self, new_threshold):
        self.prolog.query("retractall(default_gpa_threshold(_))")
        self.prolog.assertz(f"default_gpa_threshold({new_threshold})")
        print(f"Default GPA threshold updated to {new_threshold} in Prolog.")

    def calculate_gpa(self, grade_points, credits):
        result = list(self.prolog.query(f"calculate_gpa_by_semester({grade_points}, {credits}, GPA)"))
        return result[0]['GPA'] if result else None

    def calculate_cumulative_gpa(self, grade_points, credits):
        result = list(self.prolog.query(f"calculate_cumulative_gpa({grade_points}, {credits}, CumulativeGPA)"))
        return result[0]['CumulativeGPA'] if result else None

    def check_academic_probation(self, cumulative_gpa):
        result = list(self.prolog.query(f"academic_probation({cumulative_gpa})"))
        return bool(result)