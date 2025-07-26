students = [
    (101, "Alice", 85, 20),
    (102, "Bob", 92, 19),
    (103, "Carol", 78, 21),
    (104, "David", 88, 20)
]

highest_grade_student = max(students, key=lambda student: student[2])
print(f"Student with highest grade: {highest_grade_student}")

name_grade_list = [(student[1], student[2]) for student in students]
print(f"Name-Grade list: {name_grade_list}")

try:
    students[0] = (students[0][0], students[0][1], 95, students[0][3])
except TypeError as e:
    print(f"Cannot modify tuple: {e}")
    print("Tuples are immutable, which makes them ideal for storing fixed student records")
