students = ["Alice", "Bob", "Carol", "David", "Eve"]
scores = [85, 92, 78, 88, 95]

print("1. Numbered List of Students:")
for i, student in enumerate(students, 1):
    print(f"{i}. {student}")

print("\n2. Students with Their Scores:")
for student, score in zip(students, scores):
    print(f"{student}: {score}")

print("\n3. Positions of High Scorers (above 90):")
high_scorer_positions = [i for i, score in enumerate(scores) if score > 90]
for pos in high_scorer_positions:
    print(f"Position {pos}: {students[pos]} scored {scores[pos]}")

print("\n4. Position to Student Name Dictionary:")
position_to_name = {i: student for i, student in enumerate(students)}
print(position_to_name)
