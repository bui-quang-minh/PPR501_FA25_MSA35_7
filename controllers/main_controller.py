from utils.csv_handler import CSVHandler
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
from database.db_manager import DatabaseManager
from utils.validators import Validator
from views.main_window import MainWindow

class MainController:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.validator = Validator()
        self.main_window = MainWindow()
        self.tree = None
        self.entries = {}
        self.search_entry = None

    def add_student(self):
        if not self.main_window.validate_inputs():
            return

        try:
            student = self.main_window.get_student_from_inputs()
            self.db_manager.add_student(student)
            self.load_students()
            self.main_window.clear_entries()
            messagebox.showinfo("Success", "Student added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")


    def update_student(self):
        if not self.validate_inputs():
            return

        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to update")
            return

        try:
            student = self.get_student_from_inputs()
            self.db_manager.update_student(student)
            self.load_students()
            self.clear_entries()
            messagebox.showinfo("Success", "Student updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {str(e)}")


    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            try:
                item = self.tree.item(selected[0])
                student_id = item['values'][0]

                self.db_manager.delete_student(student_id)
                self.load_students()
                self.clear_entries()
                messagebox.showinfo("Success", "Student deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student: {str(e)}")


    def import_csv(self):
        filename = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not filename:
            return

        try:
            students = CSVHandler.import_from_csv(filename)
            self.db_manager.import_students(students)
            self.load_students()
            messagebox.showinfo("Success", f"Imported {len(students)} students successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import CSV: {str(e)}")


    def export_csv(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not filename:
            return

        try:
            students = self.db_manager.get_all_students()
            CSVHandler.export_to_csv(filename, students)
            messagebox.showinfo("Success", f"Exported {len(students)} students successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {str(e)}")


    def search_students(self):
        search_term = self.search_entry.get().strip().lower()

        if not search_term:
            self.load_students()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        students = self.db_manager.get_all_students()
        for student in students:
            student_id = str(student.student_id).lower()
            full_name = f"{student.lastname} {student.firstname}".lower()

            if search_term in student_id or search_term in full_name:
                self.tree.insert('', tk.END, values=student.to_tuple())


    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_students()

    def load_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        students = self.db_manager.get_all_students()
        for student in students:
            self.tree.insert('', tk.END, values=student.to_tuple())