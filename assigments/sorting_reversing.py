employees = [
    ("Alice", 50000, "Engineering"),
    ("Bob", 60000, "Marketing"),
    ("Carol", 55000, "Engineering"),
    ("David", 45000, "Sales")
]

print("Original employees list:")
for emp in employees:
    print(emp)

print("\nTask 1: Sort by Salary")
employees_salary_asc = sorted(employees, key=lambda x: x[1])
print("Ascending order:")
for emp in employees_salary_asc:
    print(emp)

employees_salary_desc = sorted(employees, key=lambda x: x[1], reverse=True)
print("Descending order:")
for emp in employees_salary_desc:
    print(emp)

print("\nTask 2: Sort by Department, Then by Salary")
employees_dept_salary = sorted(employees, key=lambda x: (x[2], x[1]))
print("Sorted by department (alphabetically), then by salary:")
for emp in employees_dept_salary:
    print(emp)

print("\nTask 3: Create a Reversed List")
employees_reversed = employees[::-1]
print("Reversed list (without modifying original):")
for emp in employees_reversed:
    print(emp)

print("\nTask 4: Sort by Name Length")
employees_name_length = sorted(employees, key=lambda x: len(x[0]))
print("Sorted by name length:")
for emp in employees_name_length:
    print(emp)

print("\nTask 5: Use sorted() vs .sort() Appropriately")
print("Using .sort() to modify original list:")
employees_copy = employees.copy()
employees_copy.sort(key=lambda x: x[1])
print("Modified list (using .sort()):")
for emp in employees_copy:
    print(emp)

print("Using sorted() to create new sorted list:")
employees_new_sorted = sorted(employees, key=lambda x: x[1])
print("New sorted list (using sorted()):")
for emp in employees_new_sorted:
    print(emp)

print("Original list remains unchanged:")
for emp in employees:
    print(emp)
