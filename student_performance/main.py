# https://www.programmingexpert.io/projects/student-performance

# must output:
# average student mark
# hardest subject
# easiest subject
# best performing grade
# worst performing grade
# best student id
# worst student id

### BASE CODE with modified path

import json
import os

NUM_STUDENTS = 1000
SUBJECTS = ["math", "science", "history", "english", "geography"]
DIRECTORY = "students"

def load_report_card(directory, student_number):
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, f"{student_number}.json")
    path = os.path.join(base_path, file_path)

    try:
        with open(path, "r") as file:
            report_card = json.load(file)
    except FileNotFoundError:
        return {}

    return report_card

### END OF BASE CODE
class Student:
    total_grades_per_subject = {}
    hardest_subject = ""
    easiest_subject = ""
    total_avg_per_grade = {}
    students_per_grade = {}
    avg_per_grade = {}
    student_average = 0
    best_performing_grade = 0
    worst_performing_grade = 0
    best_student_avg = 0
    worst_student_avg = 101
    best_student_id = 0
    worst_student_id = 0

    def __init__(self, report_card):
        total_grades = 0
        for key, value in report_card.items():
            if key == "id":
                self.id = value
            elif key == "grade":
                self.grade = value
            else:
                total_grades += value
                if key == "math":
                    self.math = value
                elif key == "science":
                    self.science = value
                elif key == "history":
                    self.history = value
                elif key == "english":
                    self.english = value
                elif key == "geography":
                    self.geography = value
                
                Student.total_grades_per_subject[key] = Student.total_grades_per_subject.get(key, 0) + value

        self.mark_average = total_grades / 5
        # updating best/worst students
        if Student.best_student_avg < self.mark_average:
            Student.best_student_avg = self.mark_average
            Student.best_student_id = self.id

        if Student.worst_student_avg > self.mark_average:
            Student.worst_student_avg = self.mark_average
            Student.worst_student_id = self.id

        # needed for best/worst performing grades
        Student.total_avg_per_grade[self.grade] = Student.total_avg_per_grade.get(
            self.grade, 0) + self.mark_average
        Student.students_per_grade[self.grade] = Student.students_per_grade.get(
            self.grade, 0) + 1
 

    @classmethod
    def update_avg_per_grade(cls):
        for grade, total_avg in cls.total_avg_per_grade.items():
            nb_students = cls.students_per_grade[grade]
            cls.avg_per_grade[grade] = total_avg / nb_students

    @classmethod
    def update_student_average(cls):
        cls.update_avg_per_grade()

        total_avg = 0
        grades = 0
        for _, avg in cls.avg_per_grade.items():
            grades += 1
            total_avg += avg

        cls.student_average = round(total_avg / grades, 2)

    @classmethod
    def update_best_worst_performing_grades(cls):
        cls.update_avg_per_grade()

        best_avg = 0
        worst_avg = 101
        best_grade = 0
        worst_grade = 0
        for grade, avg in cls.avg_per_grade.items():
            if avg > best_avg:
                best_avg = avg
                best_grade = grade
            
            if avg <= worst_avg:
                worst_avg = avg
                worst_grade = grade

        cls.best_performing_grade = best_grade
        cls.worst_performing_grade = worst_grade


    @classmethod
    def update_hardest_easiest_subjects(cls):
        max_grades = 0
        min_grades = None
        easiest_subject = ""
        hardest_subject = ""

        for subject, total_grades in cls.total_grades_per_subject.items():
            if total_grades > max_grades:
                max_grades = total_grades
                easiest_subject = subject
            
            if min_grades is None:
                min_grades = total_grades
                hardest_subject = subject

            if total_grades < min_grades:
                min_grades = total_grades
                hardest_subject = subject
        
        cls.hardest_subject = hardest_subject
        cls.easiest_subject = easiest_subject


    @classmethod
    def update_all_stats(cls):
        cls.update_best_worst_performing_grades()
        cls.update_student_average()
        cls.update_hardest_easiest_subjects()


    @classmethod
    def print_all_stats(cls):
        cls.update_all_stats()

        print("Average Student Grade: " + str(cls.student_average))
        print("Hardest Subject: " + cls.hardest_subject)
        print("Easiest Subject: " + cls.easiest_subject)
        print("Best Performing Grade: " + str(cls.best_performing_grade))
        print("Worst Performing Grade: " + str(cls.worst_performing_grade))
        print("Best Student ID: " + str(cls.best_student_id))
        print("Worst Student ID: " + str(cls.worst_student_id))

    
for i in range(NUM_STUDENTS):
    report_card = load_report_card(DIRECTORY, i)
    new_student = Student(report_card)

Student.print_all_stats()

# Execution example / target
"""
Average Student Grade: 50.44
Hardest Subject: geography
Easiest Subject: english
Best Performing Grade: 6
Worst Performing Grade: 5
Best Student ID: 549
Worst Student ID: 637
"""


# output = f"""\
#         Average Student Grade: {str(cls.student_average)}
#         Hardest Subject: {cls.hardest_subject}
#         Easiest Subject: {cls.easiest_subject}
#         Best Performing Grade: {str(cls.best_performing_grade)}
#         Worst Performing Grade: {str(cls.worst_performing_grade)}
#         Best Student ID: {str(cls.best_student_id)}
#         Worst Student ID: {str(cls.worst_student_id)}\
#         """