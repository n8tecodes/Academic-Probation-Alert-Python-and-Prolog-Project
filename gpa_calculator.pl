/*% Default GPA threshold fact
default_gpa_threshold(2.0).

% Student facts: student_id, student_name, email, school, program
student(1001, 'John Doe', 'johndoe@example.com', 'School of Computing', 'Computer Science').
student(1002, 'Jane Smith', 'janesmith@example.com', 'School of Business', 'Accounting').

% Module facts: module_code, module_name, credits
module('CS101', 'Introduction to Computer Science', 4).
module('CS102', 'Data Structures', 3).
module('ACC101', 'Principles of Accounting', 3).

% Grade facts: module_code, year, semester, student_id, grade_points
grade('CS101', 2024, 1, 1001, 3.0).
grade('CS102', 2024, 1, 1001, 2.5).
grade('ACC101', 2024, 1, 1002, 2.0).*/

/*% Rule to sum lists
sum_list([], 0).
sum_list([H|T], Sum) :-
    sum_list(T, Rest),
    Sum is H + Rest.

% Rule to calculate GPA for a list of modules
calculate_gpa(GradePointsList, CreditsList, GPA) :-
    sum_list(GradePointsList, TotalGradePoints),
    sum_list(CreditsList, TotalCredits),
    TotalCredits > 0, % Avoid division by zero
    GPA is TotalGradePoints / TotalCredits.

% Rule to check if a student is on academic probation
academic_probation(StudentID, GPA) :-
    default_gpa_threshold(Threshold),
    findall(GradePoints, grade(_, _, _, StudentID, GradePoints), GradePointsList),
    findall(Credits, (grade(ModuleCode, _, _, StudentID, _), module(ModuleCode, _, Credits)), CreditsList),
    calculate_gpa(GradePointsList, CreditsList, GPA),
    GPA =< Threshold.*/





% Dynamic declaration for the GPA threshold
:- dynamic default_gpa_threshold/1.
default_gpa_threshold(2.0).  % Default GPA threshold

% Rule to sum lists
sum_list([], 0).
sum_list([H|T], Sum) :-
    sum_list(T, Rest),
    Sum is H + Rest.

% Rule to calculate GPA from lists of grade points and credits
calculate_gpa(GradePointsList, CreditsList, GPA) :-
    sum_list(GradePointsList, TotalGradePoints),
    sum_list(CreditsList, TotalCredits),
    TotalCredits > 0,  % Avoid division by zero
    GPA is TotalGradePoints / TotalCredits.

% Calculate GPA for a specific semester, taking redo attempts into account
calculate_gpa_by_semester(GradePointsList, CreditsList, GPA) :-
    calculate_gpa(GradePointsList, CreditsList, GPA).

% Calculate cumulative GPA across all semesters
calculate_cumulative_gpa(AllGradePointsList, AllCreditsList, CumulativeGPA) :-
    calculate_gpa(AllGradePointsList, AllCreditsList, CumulativeGPA).

% Rule to check if a student is on academic probation based on cumulative GPA
academic_probation(CumulativeGPA) :-
    default_gpa_threshold(Threshold),
    CumulativeGPA =< Threshold.


