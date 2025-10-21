# src/student_manager.py

import csv
from statistics import mean, median, pstdev

class Student:
    def __init__(self,id,name):
        self.Id = id
        self.name = name
        self.grades = []
        

    def add_grade(self, grade):
        try:
            grade = float(grade)
            self.grades.append(grade)
        except ValueError:
            print("❌ Grade must be a number")

    def summary(self):
        if not self.grades:
            return {"id": self.id, "name": self.name, "avg": 0.0}
        return {
            "id": self.id,
            "name": self.name,
            "avg": round(mean(self.grades), 2),
            "median": round(median(self.grades), 2),
            "std": round(pstdev(self.grades), 2) if len(self.grades) > 1 else 0.0
        }


class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, name):
        student_id = str(len(self.students) + 1)
        student = Student(student_id, name)
        self.students.append(student)
        print(f"✅ Added student {name} (ID: {student_id})")

    def find_student(self, student_id):
        for s in self.students:
            if s.id == student_id:
                return s
        return None

    def show_all(self):
        for s in self.students:
            print(s.summary())

    def save_to_csv(self, filename="students.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "grades"])
            for s in self.students:
                writer.writerow([s.id, s.name, ";".join(map(str, s.grades))])
        print(f"💾 Data saved to {filename}")


def main():
    manager = StudentManager()

    while True:
        print("\n🎓 YouthHub - Student Manager")
        print("1) Add Student")
        print("2) Add Grade")
        print("3) Show All")
        print("4) Save & Exit")

        choice = input("Your choice: ")

        if choice == "1":
            name = input("Enter student name: ")
            manager.add_student(name)
        elif choice == "2":
            sid = input("Student ID: ")
            grade = input("Grade: ")
            s = manager.find_student(sid)
            if s:
                s.add_grade(grade)
            else:
                print("⚠️ Student not found")
        elif choice == "3":
            manager.show_all()
        elif choice == "4":
            manager.save_to_csv()
            print("👋 Goodbye")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()
