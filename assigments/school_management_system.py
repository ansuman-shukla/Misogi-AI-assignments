school = {
    "Math": {
        "teacher": "Mr. Smith",
        "students": [("Alice", 85), ("Bob", 92), ("Carol", 78)]
    },
    "Science": {
        "teacher": "Ms. Johnson",
        "students": [("David", 88), ("Eve", 94), ("Frank", 82)]
    }
}

for class_name, class_info in school.items():
    print(class_info["teacher"])

for class_name, class_info in school.items():
    total_grades = sum(grade for name, grade in class_info["students"])
    average = total_grades / len(class_info["students"])
    print(f"{class_name}: {average:.2f}")

all_students = []
for class_name, class_info in school.items():
    for name, grade in class_info["students"]:
        all_students.append((name, grade))

top_student = max(all_students, key=lambda x: x[1])
print(f"{top_student[0]}: {top_student[1]}")

for class_name, class_info in school.items():
    for name, grade in class_info["students"]:
        print(f"Student: {name}, Grade: {grade}")
