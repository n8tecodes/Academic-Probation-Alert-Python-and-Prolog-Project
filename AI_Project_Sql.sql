CREATE DATABASE AcademicProbationSystem;
USE AcademicProbationSystem;

CREATE TABLE StudentMaster (
    		student_id INT PRIMARY KEY,
    		student_name VARCHAR(100) NOT NULL,
    		student_email VARCHAR(100) NOT NULL UNIQUE,
    		school VARCHAR(50) NOT NULL,
    		programme VARCHAR(50) NOT NULL
	);

INSERT INTO StudentMaster (student_id, student_name, student_email, school, programme) VALUES
		(1, 'John Doe', 'johndoe@university.com', 'School of Computing', 'Computer Science'),
		(2, 'Jane Smith', 'janesmith@university.com', 'School of Engineering', 'Mechanical 	Engineering');
        
select * from StudentMaster;       
select * from ModuleMaster;
select * from moduledetails;


CREATE TABLE ModuleMaster (
    		module_code VARCHAR(10) PRIMARY KEY,
    		module_name VARCHAR(100) NOT NULL,
    		credits INT NOT NULL CHECK (credits > 0)
	);
    
    
CREATE TABLE ModuleDetails (
    		id INT AUTO_INCREMENT PRIMARY KEY,
    		student_id INT,
    		module_code VARCHAR(10),
    		year INT NOT NULL,
    		semester INT NOT NULL CHECK (semester IN (1, 2)),
    		grade_points FLOAT CHECK (grade_points >= 0),
    		FOREIGN KEY (student_id) REFERENCES StudentMaster(student_id),
    		FOREIGN KEY (module_code) REFERENCES ModuleMaster(module_code)
	);    
INSERT INTO ModuleMaster (module_code, module_name, credits) VALUES
	('CS101', 'Introduction to Computer Science', 3),
	('MATH201', 'Calculus II', 4);

INSERT INTO ModuleDetails (student_id, module_code, year, semester, grade_points) VALUES
		(1, 'CS101', 2024, 1, 3.5),
		(1, 'MATH201', 2024, 1, 2.0),
		(2, 'CS101', 2024, 2, 3.0);
SELECT 
    SUM(m.credits * d.grade_points) / SUM(m.credits) AS GPA
FROM 
    ModuleDetails d
JOIN 
    ModuleMaster m ON d.module_code = m.module_code
WHERE 
    d.student_id = 1 AND d.year = 2024 AND d.semester = 1; 
    
    
    
SELECT 
    SUM(m.credits * d.grade_points) / SUM(m.credits) AS cumulative_GPA
FROM 
    ModuleDetails d
JOIN 
    ModuleMaster m ON d.module_code = m.module_code
WHERE 
    d.student_id = 1;
    
CREATE TABLE AdminStaff (
    admin_id VARCHAR(20) PRIMARY KEY,
    admin_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);    