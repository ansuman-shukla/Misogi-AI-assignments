from collections import defaultdict

class GradeManager:
    def __init__(self):
        self.grade_manager = defaultdict(lambda: defaultdict(list))
    
    def add_grade(self, student_name, subject, grade):
        self.grade_manager[student_name][subject].append(grade)
    
    def get_student_average(self, student_name):
        if student_name not in self.grade_manager:
            return f"Student {student_name} not found"
        
        total_grades = []
        for subject in self.grade_manager[student_name]:
            total_grades.extend(self.grade_manager[student_name][subject])
        
        if not total_grades:
            return 0
        
        return sum(total_grades) / len(total_grades)
    
    def get_subject_statistics(self, subject):
        all_grades = []
        for student in self.grade_manager:
            if subject in self.grade_manager[student]:
                all_grades.extend(self.grade_manager[student][subject])
        
        if not all_grades:
            return f"No grades found for subject {subject}"
        
        average = sum(all_grades) / len(all_grades)
        highest = max(all_grades)
        lowest = min(all_grades)
        student_count = sum(1 for student in self.grade_manager if subject in self.grade_manager[student])
        
        return {
            "subject": subject,
            "average": average,
            "highest": highest,
            "lowest": lowest,
            "student_count": student_count
        }
    
    def get_top_students(self, n=3):
        student_averages = []
        for student in self.grade_manager:
            avg = self.get_student_average(student)
            if isinstance(avg, (int, float)):
                student_averages.append((student, avg))
        
        student_averages.sort(key=lambda x: x[1], reverse=True)
        return student_averages[:n]
    
    def get_failing_students(self, passing_grade=60):
        failing_students = []
        for student in self.grade_manager:
            avg = self.get_student_average(student)
            if isinstance(avg, (int, float)) and avg < passing_grade:
                failing_students.append((student, avg))
        
        failing_students.sort(key=lambda x: x[1])
        return failing_students

manager = GradeManager()

sample_data = [
    ("Alice", "Math", 85), ("Alice", "Science", 92), ("Alice", "English", 78),
    ("Bob", "Math", 78), ("Bob", "Science", 85), ("Bob", "English", 82),
    ("Charlie", "Math", 92), ("Charlie", "Science", 88), ("Charlie", "History", 90),
    ("Diana", "Math", 67), ("Diana", "Science", 73), ("Diana", "English", 85), ("Diana", "History", 80)
]

for student, subject, grade in sample_data:
    manager.add_grade(student, subject, grade)

print("Alice's average:", manager.get_student_average("Alice"))
print("Math statistics:", manager.get_subject_statistics("Math"))
print("Top 3 students:", manager.get_top_students(3))
print("Failing students:", manager.get_failing_students())
