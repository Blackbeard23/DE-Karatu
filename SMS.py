from typing import Union, Optional, List, Dict

class Person:
    """
    Represents a person with a name and an ID number.
    """

    def __init__(self, name: str, id_number: str) -> None:
        """
        Initializes a Person instance with a name and an ID number.
        """
        self.name: str = name
        self.id_number: str = id_number

    def __str__(self) -> str:
        """
        A string representation of a person's details
        """
        return f"ID: {self.id_number} Name: {self.name}"
    

class Student(Person):
    """
    Represents a student (inherits from the Person class) in a Student Management System
    """

    def __init__(self, name: str, id_number: str, major: str) -> None:
        """
        Initializes a Student instance with a name, ID number, Major, and a dictionary of enrolled courses.
        """
        super().__init__(name, id_number)
        self.major: str = major
        # Initializes an empty dictionary where the keys are Course objects
        # and the values are optional grade
        self.courses: Dict[Course, Optional[str]] = {}
        

    def add_course(self, enrol: 'Enrollment') -> None:
        """
        Adds the course a student is enrolled in to the student's course list.

        This method is called from the Enrollment class when an enrollment is initialized.
        If the student's ID matches the enrollment's student ID, the course is added to 
        the student's list of courses with the corresponding grade.

        Args:
            enrol (Enrollment): An instance of the Enrollment class, which includes 
            the student, course, and grade information.
        """
        if self.id_number == enrol.student.id_number:
            self.courses[enrol.course] = enrol.grade


    def __str__(self) -> str:
        """
        A string representation of the student's details
        """
        return f"{'ID:':>7} {self.id_number}\n{'Name:':>7} {self.name}\n{'Major:':>7} {self.major}"
    
    def __repr__(self) -> str:
        """
        A formal string representation of the student's details within a list
        """
        return f"({self.name} - {self.major})"
    

class Instructor(Person):
    """
    Represents an Instructor (inherits from the Person class) in a Student Management System
    """

    def __init__(self, name: str, id_number: str, department: str) -> None:
        """
        Initializes an Instructor instance with a name, ID number, and Department.
        """
        super().__init__(name, id_number)
        self.department: str = department

    def __str__(self) -> str:
        """
        A string representation of an Instructor's details
        """
        return f"{'ID:':>12} {self.id_number}\n{'Name:':>12} {self.name}\n{'Department:':>12} {self.department}"
    

class Course:
    """
    Represents a Course in a Student Management System
    """

    def __init__(self, course_name: str, course_id: str, enrolled_students: Optional[List[Student]] = None) -> None:
        """
        Initializes a Course instance with a Course name, ID number, and Enrolled Student.
        """
        self.course_name: str = course_name
        self.course_id: str = course_id
        if enrolled_students is not None:
            self.enrolled_students: List[Student] = enrolled_students
        else:
            self.enrolled_students: List[Student] = []

    def enrollment(self, enrol: "Enrollment") -> None:
        """
        Adds a student to the course's list of enrolled students if the course 
        in the Enrollment matches this course.
        
        Args:
            enrol (Enrollment): An instance of the Enrollment class containing 
            the student and course information.
        """
        if self.course_name == enrol.course.course_name:
            self.enrolled_students.append(enrol.student)

    def add_student(self, student: Student) -> None:
        """
        Adds a student to the course if they are not already enrolled.

        This method checks whether the student is already enrolled in the course. 
        If the student is found in the list of enrolled students, a ValueError is raised. 
        Otherwise, the student is enrolled in the course.

        Args:
            student (Student): The student to be added to the course.
        """
        if student in self.enrolled_students:
            raise ValueError(f'Student ID {student.id_number} is already enrolled in course {self.course_name}')
        Enrollment(student, self)

    def find_enrolled_student(self, student_id: str) -> Optional[Student]:
        """
        Finds a student enrolled in the course by their student ID.

        This method searches through the list of enrolled students and returns the matching 
        student object. If no student with the given ID is found, it returns None.

        Args:
            student_id (str): The ID of the student to search for.
        """
        for std in self.enrolled_students:
            if std.id_number == student_id:
                return std
        return None

    def remove_student(self, student_id: str) -> None:
        """
        Removes a student from the course by their student ID.

        This method finds the student enrolled in the course using the `find_enrolled_student` 
        method, and if the student is found, removes them from the list of enrolled students.
        
        Args:
            student_id (str): The ID of the student to be removed.
        """
        std_enrolled = self.find_enrolled_student(student_id)
        if std_enrolled:
            self.enrolled_students.remove(std_enrolled)

    def __str__(self) -> str:
        """
        A string representation of a Course details
        """
        # return f"{'ID:':>19} {self.course_id}\n{'Course Name:':>19} {self.course_name}\n{'Enrolled Students:':>19} {self.enrolled_students}"
        return (
        f"{'ID:':>18} {self.course_id}\n"
        f"{'Course Name:':>18} {self.course_name}\n"
        f"{'Enrolled Students:':>18} {self.enrolled_students}"
        )
    
    def __repr__(self) -> str:
        """
        A formal string representation of the course ID and name
        """
        return f"({self.course_id} - {self.course_name})"
    

class Enrollment:
    """
    Represents an enrollment of a student in a course within a Student Management System.
    """

    def __init__(self, student: Student, course: Course, grade: Optional[str] = None) -> None:
        """
        Initializes an Enrollment instance with a student, course, and optional grade.

        Upon initialization:
        - The course's `enrollment` method is called to add the student to the course's list 
          of enrolled students.
        - The student's `add_course` method is called to add the course to the student's 
          list of enrolled courses.
        """
        self.student: Student = student
        self.course: Course = course
        self.grade: Optional[str] = grade
        self.course.enrollment(self)
        self.student.add_course(self)

    def assign_grade(self, grade: str):
        """
        Assigns a grade to a student enrolled in a course

        This method validates the grade against a predefined grading system 
        (['A', 'B', 'C', 'D', 'E', 'F']). If the grade is valid, it assigns it 
        to the student. Otherwise, it raises a ValueError. 
        """
        grade_system: List[str] = ['A', 'B', 'C', 'D', 'E', 'F']
        if grade in grade_system:
            self.grade = grade
            self.student.courses[self.course] = grade
        else:
            raise ValueError('Invalid grading system')

    def __str__(self) -> str:
        """
        A string representation of enrollment details
        """
        return f"{'Course:':>8} {self.course.course_name}\n{'Student:':>8} {self.student.name}"
    
    def __repr__(self) -> str:
        """
        A formal string representation of enrollment details
        """
        return f"({self.course.course_name}, {self.student.name}, {self.grade})"
    

class StudentManagementSystem:
    """
    Manages students, instructors, courses, and enrollments within the system.
    """

    def __init__(self) -> None:
        """
        Initializes the StudentManagementSystem with empty lists for 
        students, instructors, courses, and enrollments.
        """
        self.students: List[Student] = []
        self.instructors: List[Instructor] = []
        self.courses: List[Course] = []
        self.enrollments: List[Enrollment] = []

    def add_student(self, student: Student) -> None:
        """
        Adds a student to the student management system.

        This method checks if the student is not already in the list of students. 
        If the student is not present, it appends the student to the list.

        Args:
            student (Student): The student to be added to the system.
        """
        if student not in self.students:
            self.students.append(student)

    def find_student(self, student_id: str) -> Student:
        """
        Finds and returns a student by their ID number.

        This method iterates through the list of students to find a match for 
        the given student ID. If a student with the specified ID is found, 
        the student object is returned. Otherwise, it returns None.

        Args:
            student_id (str): The ID number of the student to find.
        """
        for std in self.students:
            if std.id_number == student_id:
                return std
        raise ValueError(f'No student record found for ID: {student_id}')

    def remove_student(self, student_id: str) -> None:
        """
        Removes a student from the student management system by their ID number.

        This method first attempts to find a student with the given ID using 
        the `find_student` method. If the student is found, they are removed 
        from the list of students.

        Args:
            student_id (str): The ID number of the student to be removed.
        """
        std = self.find_student(student_id)
        self.students.remove(std)

    def update_student(self, student_id: str, name: Optional[str] = None, major: Optional[str] = None) -> None:
        """
        Updates the details of a student in the student management system.

        This method finds the student by their ID using the `find_student` method. 
        If the student is found, it updates the student's name and/or major if 
        new values are provided.

        Args:
            student_id (str): The ID number of the student to be updated.
            name (Optional[str]): The new name for the student, if provided.
            major (Optional[str]): The new major for the student, if provided.
        """
        student_found = self.find_student(student_id)
        if name is not None:
            student_found.name = name
        if major is not None:
            student_found.major = major
    
    def add_instructor(self, instructor: Instructor) -> None:
        """
        Adds an instructor to the student management system.

        This method checks if the instructor is not already in the list of instructors. 
        If the instructor is not present, it appends the instructor to the list.

        Args:
            instructor (Instructor): The instructor to be added to the system.
        """
        if instructor not in self.instructors:
            self.instructors.append(instructor)

    def find_instructor(self, instructor_id: str) -> Instructor:
        """
        Finds and returns an instructor by their ID number.

        This method iterates through the list of instructors to find a match for 
        the given instructor ID. If an instructor with the specified ID is found, 
        the instructor object is returned. Otherwise, it returns None.

        Args:
            instructor_id (str): The ID number of the instructor to find.
        """
        for inst in self.instructors:
            if inst.id_number == instructor_id:
                return inst        
        raise ValueError(f'No instructor record found for ID: {instructor_id}')

    def remove_instructor(self, instructor_id: str) -> None:
        """
        Removes an instructor from the student management system by their ID number.

        This method first attempts to find an instructor with the given ID using 
        the `find_instructor` method. If the instructor is found, they are removed 
        from the list of instructors.

        Args:
            instructor_id (str): The ID number of the instructor to be removed.
        """
        inst_obj = self.find_instructor(instructor_id)
        self.instructors.remove(inst_obj)

    def update_instructor(self, instructor_id: str, name: Optional[str]=None, department: Optional[str]=None) -> None:
        """
        Updates the details of an instructor in the system.

        This method finds the instructor by their ID using the `find_instructor` method. 
        If the instructor is found, their name and/or department are updated if new values 
        are provided.

        Args:
            instructor_id (str): The ID number of the instructor to be updated.
            name (Optional[str]): The new name for the instructor, if provided.
            department (Optional[str]): The new department for the instructor, if provided.
        """
        instructor_found = self.find_instructor(instructor_id)
        if name is not None:
            instructor_found.name = name
        if department is not None:
            instructor_found.department = department
    
    def add_course(self, course: Course) -> None:
        """
        Adds a course to the system.

        This method checks if the given course is already in the list of courses.
        If the course is not in the list, it is added to the system.

        Args:
            course (Course): The course to be added to the system.
        """
        if course not in self.courses:
            self.courses.append(course)

    def find_course(self, course_id: str) -> Course:
        """
        Finds a course in the system by its course ID.

        This method searches through the list of courses to find a course that matches 
        the given course ID. If a matching course is found, it is returned; otherwise, 
        None is returned.

        Args:
            course_id (str): The ID of the course to find.
        """
        for crs in self.courses:
            if crs.course_id == course_id:
                return crs        
        raise ValueError(f'No course record found for ID: {course_id}')

        
    def remove_course(self, course_id: str) -> None:
        """
        Removes a course from the system by its course ID.

        This method first finds the course with the specified ID using the `find_course` method. 
        If the course is found, it is removed from the list of courses.

        Args:
            course_id (str): The ID of the course to be removed.
        """
        course_found = self.find_course(course_id)
        self.courses.remove(course_found)

    def update_course(self, course_id: str, course_name: Optional[str]=None) -> None:
        """
        Removes a course from the system by its course ID.

        This method first finds the course with the specified ID using the `find_course` method. 
        If the course is found, it is removed from the list of courses.

        Args:
            course_id (str): The ID of the course to be removed.
        """
        course_found = self.find_course(course_id)
        if course_name is not None:
            course_found.course_name = course_name

    def enroll_student(self, student_id: str, course_id: str) -> None:
        """
        Enrolls a student in a course.

        This method first finds the student by their ID using the `find_student` method. 
        Then, finds the corresponding course using the `find_course` method 
        and creates an `Enrollment` instance.
        The created enrollment instance is then added to the list of enrollments.

        Args:
            student_id (str): The ID of the student to be enrolled.
            course_id (str): The course ID in which the student should be enrolled.
        """
        student_found = self.find_student(student_id)
        course_found = self.find_course(crs)
        enrol_obj = Enrollment(student_found, course_found)
        self.enrollments.append(enrol_obj)

    def find_enrollment(self, course_id: str, student_id: str) -> Enrollment:
        """
        Finds an enrollment record for a specific student in a specific course.

        Searches through the list of enrollments to find an `Enrollment` object that matches
        the provided student ID and course ID.

        Args:
            course_id (str): The ID of the course to search for.
            student_id (str): The ID of the student to search for.
        """
        for enrol in self.enrollments:
            if (enrol.student.id_number == student_id) and (enrol.course.course_id == course_id):
                return enrol
        raise ValueError(f'StudentID {student_id} is not enrolled in courseID {course_id}')

    def assign_grade(self, course_id: str, student_id: str, grade: str) -> None:
        """
        Assigns a grade to a student for a specific course.

        This method looks for an enrollment matching the provided student ID and course ID. 
        If found, it assigns the provided grade to the student. If no matching enrollment 
        is found, it raises a ValueError.

        Args:
            course_id (str): The ID of the course for which the grade is assigned.
            student_id (str): The ID of the student to whom the grade is assigned.
            grade (str): The grade to be assigned.
        """
        enrollment_found = self.find_enrollment(course_id, student_id)
        enrollment_found.assign_grade(grade)

    def students_in_course(self, course_id: str) -> List[Student]:
        """
        Retrieves a list of students enrolled in a specific course.

        This method finds the course by its ID using the `find_course` method. 
        If the course is found, it returns the list of students enrolled in that course. 
        If the course is not found, it returns an empty list.

        Args:
            course_id (str): The ID of the course for which to retrieve the enrolled students.
        """
        course_found = self.find_course(course_id)
        return course_found.enrolled_students
    
    def student_courses(self, student_id: str) -> List[Course]:
        """
        Retrieves a list of courses a student is enrolled in.

        This method finds the student by their ID using the `find_student` method. 
        If the student is found, it returns the list of courses the student is enrolled in. 
        If the student is not found, it returns an empty list.

        Args:
            student_id (str): The ID of the student for whom to retrieve the enrolled courses.
        """
        student_found = self.find_student(student_id)
        return list(student_found.courses.keys())
        


    


