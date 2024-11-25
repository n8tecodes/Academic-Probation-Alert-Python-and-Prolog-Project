import subprocess

class PrologInterface:
    def __init__(self, prolog_file):
        self.prolog_file = prolog_file

    def _run_prolog_query(self, query):
        result = subprocess.run(['swipl', '-s', self.prolog_file, '-g', query, '-t', 'halt'], capture_output=True, text=True)
        return result.stdout

    def calculate_gpa(self, grade_points, credits):
        query = f"calculate_gpa({grade_points}, {credits}, GPA)."
        result = self._run_prolog_query(query)
        try:
            return float(result.strip())
        except ValueError:
            return None

    def calculate_cumulative_gpa(self, all_grade_points, all_credits):
        query = f"calculate_cumulative_gpa({all_grade_points}, {all_credits}, CumulativeGPA)."
        result = self._run_prolog_query(query)
        try:
            return float(result.strip())
        except ValueError:
            return None

    def check_academic_probation(self, cumulative_gpa):
        query = f"check_academic_probation({cumulative_gpa}, ProbationStatus)."
        result = self._run_prolog_query(query)
        return "true" in result

    def update_gpa_threshold(self, new_threshold):
        query = f"update_gpa_threshold({new_threshold})."
        self._run_prolog_query(query)
