grades = [85, 92, 78, 90, 88, 76, 94, 89, 87, 91]

sliced_grades = grades[2:8]
print(f"Grades from index 2 to 7: {sliced_grades}")

grades_above_85 = [grade for grade in grades if grade > 85]
print(f"Grades above 85: {grades_above_85}")

grades[3] = 95
print(f"After replacing grade at index 3 with 95: {grades}")

grades.extend([93, 96, 88])
print(f"After appending three new grades: {grades}")

sorted_grades = sorted(grades, reverse=True)
top_5_grades = sorted_grades[:5]
print(f"Top 5 grades in descending order: {top_5_grades}")
