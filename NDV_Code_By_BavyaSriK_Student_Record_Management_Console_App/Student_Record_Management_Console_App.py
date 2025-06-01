import json
import os

class Student:
    """
    Represents a single student record with ID, name, branch, year, and marks.
    """
    def __init__(self,Student_id,Name,Branch,Year,Marks):
        self.student_id = Student_id
        self.name = Name
        self.branch = Branch
        self.year = Year
        self.marks = Marks

    def to_dict(self):
        """
        Converts the Student object to a dictionary for JSON serialization.
        """
        return {
            "Student_id": self.student_id,
            "Name": self.name,
            "Branch": self.branch,
            "Year": self.year,
            "Marks": self.marks
        }

    @classmethod
    def from_dict(cls,data):
        """
        Creates a Student object from a dictionary.
        This is useful when loading data from JSON.
        """
        return cls(
            data["Student_id"],
            data["Name"],
            data["Branch"],
            data["Year"],
            data["Marks"]
        )

    def __str__(self):
        """
        Returns a string representation of the Student object.
        """
        return (f"ID:{self.student_id},Name:{self.name},Branch:{self.branch},"
                f"Year:{self.year},Marks:{self.marks}")


class StudentManager:
    """
    Manages the collection of student records, including loading, saving,
    adding, viewing, updating, and deleting.
    """
    def __init__(self,file_name="students.json"):
        self.file_name=file_name
        self.students=[]
        self._load_data()

    def _load_data(self):
        """
        Loads student data from the JSON file into the 'students' list.
        If the file doesn't exist, it initializes an empty list.
        """
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name,'r') as f:
                    data=json.load(f)
                    self.students=[Student.from_dict(d) for d in data]
                print(f"Data loaded successfully from {self.file_name}.")
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {self.file_name}. Starting with empty records.")
                self.students=[]
            except Exception as e:
                print(f"An unexpected error occurred while loading data: {e}")
                self.students=[]
        else:
            print(f"No existing data file '{self.file_name}' found. Starting with empty records.")

    def _save_data(self):
        """
        Saves the current 'students' list to the JSON file.
        Each Student object is converted to a dictionary before saving.
        """
        try:
            with open(self.file_name,'w') as f:
                json.dump([s.to_dict() for s in self.students], f, indent=4)
            print(f"Data saved successfully to {self.file_name}.")
        except Exception as e:
            print(f"Error saving data to {self.file_name}: {e}")

    def _find_student(self,student_id):
        """
        Helper method to find a student by their ID.
        Returns the Student object if found, None otherwise.
        """
        for student in self.students:
            if student.student_id==student_id:
                return student
        return None

    def add_student(self):
        """
        Prompts the user for new student details and adds the record.
        Ensures student ID is unique.
        """
        print("\n--- Add New Student ---")
        while True:
            student_id = input("Enter Student ID:").strip()
            if not student_id:
                print("Student ID cannot be empty.Please try again.")
                continue
            if self._find_student(student_id):
                print(f"Student with ID '{student_id}' already exists.Please use a unique ID.")
            else:
                break

        name = input("Enter Name:").strip()
        branch = input("Enter Branch:").strip()
        
        while True:
            try:
                year = int(input("Enter Year (e.g., 1, 2, 3, 4):"))
                if year <= 0:
                    print("Year must be a positive number.")
                else:
                    break
            except ValueError:
                print("Invalid input for year. Please enter a number.")

        while True:
            try:
                marks = float(input("Enter Marks (e.g., 85.5):"))
                if not (0 <= marks <= 100):
                    print("Marks must be between 0 and 100.")
                else:
                    break
            except ValueError:
                print("Invalid input for marks. Please enter a number.")

        new_student=Student(student_id, name, branch, year, marks)
        self.students.append(new_student)
        self._save_data()
        print(f"Student '{name}' added successfully!")

    def view_students(self):
        """
        Displays all student records in a formatted tabular layout.
        """
        print("\n--- All Student Records ---")
        if not self.students:
            print("No student records found.")
            return

        # Define column headers and widths
        headers = ["ID", "Name", "Branch", "Year", "Marks"]
        # Calculate maximum width for each column dynamically
        col_widths = {
            "ID": max(len(s.student_id) for s in self.students + [Student("ID", "", "", 0, 0)]),
            "Name": max(len(s.name) for s in self.students + [Student("", "Name", "", 0, 0)]),
            "Branch": max(len(s.branch) for s in self.students + [Student("", "", "Branch", 0, 0)]),
            "Year": max(len(str(s.year)) for s in self.students + [Student("", "", "", 0, 0)]),
            "Marks": max(len(str(s.marks)) for s in self.students + [Student("", "", "", 0, 0)])
        }
        
        # Adjust header widths if they are longer than content
        col_widths["ID"] = max(col_widths["ID"], len("ID"))
        col_widths["Name"] = max(col_widths["Name"], len("Name"))
        col_widths["Branch"] = max(col_widths["Branch"], len("Branch"))
        col_widths["Year"] = max(col_widths["Year"], len("Year"))
        col_widths["Marks"] = max(col_widths["Marks"], len("Marks"))

        # Print header
        header_line = (
            f"{headers[0]:<{col_widths['ID']}} | "
            f"{headers[1]:<{col_widths['Name']}} | "
            f"{headers[2]:<{col_widths['Branch']}} | "
            f"{headers[3]:<{col_widths['Year']}} | "
            f"{headers[4]:<{col_widths['Marks']}}"
        )
        print(header_line)
        print("-" * len(header_line))

        # Print each student record
        for student in self.students:
            print(
                f"{student.student_id:<{col_widths['ID']}} | "
                f"{student.name:<{col_widths['Name']}} | "
                f"{student.branch:<{col_widths['Branch']}} | "
                f"{str(student.year):<{col_widths['Year']}} | "
                f"{str(student.marks):<{col_widths['Marks']}}"
            )
        print("-" * len(header_line))


    def update_student(self):
        """
        Prompts for a student ID, finds the student, and allows updating
        their name, branch, year, and marks.
        """
        print("\n--- Update Student Record ---")
        student_id = input("Enter Student ID to update: ").strip()
        student = self._find_student(student_id)

        if student:
            print(f"Found student: {student}")
            print("Enter new details (leave blank to keep current value):")

            new_name = input(f"Enter new Name ({student.name}): ").strip()
            if new_name:
                student.name = new_name

            new_branch = input(f"Enter new Branch ({student.branch}): ").strip()
            if new_branch:
                student.branch = new_branch

            while True:
                new_year_str = input(f"Enter new Year ({student.year}): ").strip()
                if not new_year_str:
                    break # Keep current value
                try:
                    new_year = int(new_year_str)
                    if new_year <= 0:
                        print("Year must be a positive number.")
                    else:
                        student.year = new_year
                        break
                except ValueError:
                    print("Invalid input for year. Please enter a number.")

            while True:
                new_marks_str = input(f"Enter new Marks ({student.marks}): ").strip()
                if not new_marks_str:
                    break # Keep current value
                try:
                    new_marks = float(new_marks_str)
                    if not (0 <= new_marks <= 100):
                        print("Marks must be between 0 and 100.")
                    else:
                        student.marks = new_marks
                        break
                except ValueError:
                    print("Invalid input for marks. Please enter a number.")

            self._save_data()
            print(f"Student with ID '{student_id}' updated successfully!")
        else:
            print(f"Student with ID '{student_id}' not found.")

    def delete_student(self):
        """
        Prompts for a student ID and deletes the corresponding record.
        """
        print("\n--- Delete Student Record ---")
        student_id = input("Enter Student ID to delete: ").strip()
        
        initial_len = len(self.students)
        self.students = [s for s in self.students if s.student_id != student_id]

        if len(self.students) < initial_len:
            self._save_data()
            print(f"Student with ID '{student_id}' deleted successfully!")
        else:
            print(f"Student with ID '{student_id}' not found.")

def display_menu():
    """
    Displays the main menu options to the user.
    """
    print("\n--- Student Record Management System ---")
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Update Student Record")
    print("4. Delete Student Record")
    print("5. Exit")
    print("----------------------------------------")

def main():
    """
    Main function to run the student record management application.
    """
    manager = StudentManager()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            manager.add_student()
        elif choice == '2':
            manager.view_students()
        elif choice == '3':
            manager.update_student()
        elif choice == '4':
            manager.delete_student()
        elif choice == '5':
            print("Exiting Student Record Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
