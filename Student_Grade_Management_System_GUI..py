import tkinter as tk
from tkinter import messagebox
import logging

# File handler and stream handler setup
logger = logging.getLogger("Student_Grade_Logger")
logger.setLevel(logging.DEBUG)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("student_grade.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class StudentNotFoundError(Exception):
    """Custom exception class for student not found related errors."""
    pass


class StudentManager:
    def __init__(self):
        self.student_grades = {}

    def add_student(self, name, grade):
        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 to 100.")
        if name in self.student_grades:
            logger.warning(f"Student {name} already exists. Overwriting grade.")
        else:
            logger.info(f"Added student {name} with grade {grade}.")
        self.student_grades[name] = grade

    def update_student(self, name, grade):
        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 to 100.")
        if name not in self.student_grades:
            raise StudentNotFoundError(f"Cannot update. Student {name} not found.")
        else:
            self.student_grades[name] = grade
            logger.info(f"Updated {name} to new grade.")

    def delete_student(self, name):
        if name not in self.student_grades:
            raise StudentNotFoundError(f"Cannot delete. Student {name} not found.")
        else:
            del self.student_grades[name]
            logger.info(f"{name} has been successfully deleted.")

    def display_all_students(self):
        return self.student_grades


# GUI Application
class StudentApp:
    def __init__(self, root):
        self.manager = StudentManager()
        self.root = root
        self.root.title("Student Grade Management System")

        # Widgets
        self.name_label = tk.Label(root, text="Student Name:")
        self.name_entry = tk.Entry(root)

        self.grade_label = tk.Label(root, text="Grade:")
        self.grade_entry = tk.Entry(root)

        self.add_btn = tk.Button(root, text="Add", width=50, command=self.add_student)
        self.update_btn = tk.Button(root, text="Update", width=50, command=self.update_student)
        self.delete_btn = tk.Button(root, text="Delete", width=50, command=self.delete_student)
        self.view_btn = tk.Button(root, text="View All", width=50, command=self.view_students)
        self.exit_btn = tk.Button(root, text="Exit", width=50, command=self.exit_app)

        self.output_text = tk.Text(root, height=20, width=50)

        # Layout
        self.name_label.grid(row=0, column=0, padx=20, pady=20, sticky="e")
        self.name_entry.grid(row=0, column=1, padx=20, pady=20)
        self.grade_label.grid(row=1, column=0, padx=20, pady=20, sticky="e")
        self.grade_entry.grid(row=1, column=1, padx=20, pady=20)

        self.add_btn.grid(row=2, column=0, padx=20, pady=20)
        self.update_btn.grid(row=2, column=1, padx=20, pady=20)
        self.delete_btn.grid(row=2, column=2, padx=20, pady=20)
        self.view_btn.grid(row=3, column=0, padx=20, pady=20)
        self.exit_btn.grid(row=3, column=1, padx=20, pady=20)

        self.output_text.grid(row=4, column=0, columnspan=3, padx=20, pady=20)

    # Button functions
    def add_student(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Student name cannot be empty.")
            return
        try:
            grade = int(self.grade_entry.get())
            self.manager.add_student(name, grade)
            self.output_text.insert(tk.END, f"Added {name} with grade {grade}\n")
        except ValueError as e:
            logger.error(str(e))
            messagebox.showerror("Error", str(e))
        self.clear_entries()
    def update_student(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Student name cannot be empty.")
            return
        try:
            grade = int(self.grade_entry.get())
            self.manager.update_student(name, grade)
            self.output_text.insert(tk.END, f"Updated {name} with new grade {grade}\n")
        except StudentNotFoundError as e:
            logger.error(e)
            messagebox.showerror("Error", str(e))
        except ValueError as ve:
            logger.error(str(ve))
            messagebox.showerror("Error", str(ve))
        self.clear_entries()

    def delete_student(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Student name cannot be empty.")
            return
        try:
            self.manager.delete_student(name)
            self.output_text.insert(tk.END, f"Deleted {name}\n")
        except StudentNotFoundError as e:
            logger.error(e)
            messagebox.showerror("Error", str(e))
        self.clear_entries()

    def view_students(self):
        self.output_text.delete(1.0, tk.END)
        students = self.manager.display_all_students()
        if students:
            for name, grade in students.items():
                self.output_text.insert(tk.END, f"{name}: {grade}\n")
        else:
            self.output_text.insert(tk.END, "No students found.\n")
            logger.info("No student records to display.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)

    def exit_app(self):
        logger.info("Application closed by user.")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    app.run()
