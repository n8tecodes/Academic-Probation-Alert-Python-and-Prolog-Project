
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


