import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.student import Student
from database.db_manager import DatabaseManager
from controllers.main_controller import MainController
from utils.validators import Validator


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1200x700")

        self.db_manager = DatabaseManager()
        self.validator = Validator()
        self.main_controller = MainController(self)

        self.create_widgets()
        self.main_controller.tree = self.tree
        self.main_controller.load_students()

    def create_widgets(self):
        self.create_header()
        self.create_button_frame()
        self.create_input_frame()
        self.create_table_frame()

    def create_header(self):
        top_frame = tk.Frame(self.root, bg='#2c3e50', pady=10)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Student Management System",
                 font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack()

    def create_button_frame(self):
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack(fill=tk.X)

        buttons = [
            ("Add Student", self.main_controller.add_student, '#27ae60'),
            ("Update Student", self.main_controller.update_student, '#2980b9'),
            ("Delete Student", self.main_controller.delete_student, '#c0392b'),
            ("Import CSV", self.main_controller.import_csv, '#8e44ad'),
            ("Export CSV", self.main_controller.export_csv, '#16a085'),
            ("Refresh", self.main_controller.load_students, '#34495e'),
        ]

        for text, command, color in buttons:
            tk.Button(btn_frame, text=text, command=command,
                      bg=color, fg='white', padx=15, pady=5).pack(side=tk.LEFT, padx=5)

        tk.Label(btn_frame, text="Search:", font=('Arial', 10)).pack(side=tk.LEFT, padx=(20, 5))
        self.main_controller.search_entry = tk.Entry(btn_frame, width=30)
        self.main_controller.search_entry.pack(side=tk.LEFT, padx=5)
        self.main_controller.search_entry.bind('<Return>', lambda e: self.main_controller.search_students())

        tk.Button(btn_frame, text="Clear", command=self.main_controller.clear_search,
                  bg='#7f8c8d', fg='white', padx=10, pady=5).pack(side=tk.LEFT, padx=5)

    def create_input_frame(self):
        input_frame = tk.LabelFrame(self.root, text="Student Information",
                                    padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        labels = ['Student ID', 'Last Name', 'First Name', 'DOB (DD-MM-YYYY)',
                  'Address', 'Math Grade', 'Literature Grade', 'English Grade']
        self.entries = {}

        for i, label in enumerate(labels):
            row = i // 4
            col = (i % 4) * 2

            tk.Label(input_frame, text=label + ":").grid(row=row, column=col,
                                                         sticky='e', padx=5, pady=5)
            entry = tk.Entry(input_frame, width=20)
            entry.grid(row=row, column=col + 1, padx=5, pady=5)
            self.entries[label] = entry

    def create_table_frame(self):
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(table_frame,
                                 yscrollcommand=scroll_y.set,
                                 xscrollcommand=scroll_x.set,
                                 selectmode='browse')

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree['columns'] = ('StudentID', 'LastName', 'FirstName', 'DOB',
                                'Address', 'Math', 'Literature', 'English')

        self.tree.column('#0', width=0, stretch=tk.NO)
        column_widths = [80, 120, 120, 100, 200, 80, 80, 80]

        for col, width in zip(self.tree['columns'], column_widths):
            self.tree.column(col, width=width, anchor=tk.CENTER if width < 150 else tk.W)
            self.tree.heading(col, text=col.replace('_', ' ').title())

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']

            fields = ['Student ID', 'Last Name', 'First Name', 'DOB (DD-MM-YYYY)',
                      'Address', 'Math Grade', 'Literature Grade', 'English Grade']

            for i, field in enumerate(fields):
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, values[i] if values[i] else '')

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def validate_inputs(self):
        student_id = self.entries['Student ID'].get().strip()
        valid, msg = self.validator.validate_student_id(student_id)
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return False

        lastname = self.entries['Last Name'].get().strip()
        valid, msg = self.validator.validate_name(lastname, "Last Name")
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return False

        firstname = self.entries['First Name'].get().strip()
        valid, msg = self.validator.validate_name(firstname, "First Name")
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return False

        dob = self.entries['DOB (DD-MM-YYYY)'].get().strip()
        valid, msg = self.validator.validate_dob(dob)
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return False

        address = self.entries['Address'].get().strip()
        if not address:
            messagebox.showerror("Validation Error", "Address is required")
            return False

        grade_fields = ['Math Grade', 'Literature Grade', 'English Grade']
        for field in grade_fields:
            grade = self.entries[field].get().strip()
            valid, msg = self.validator.validate_grade(grade)
            if not valid:
                messagebox.showerror("Validation Error", f"{field}: {msg}")
                return False

        return True

    def get_student_from_inputs(self):
        return Student(
            self.entries['Student ID'].get().strip(),
            self.entries['Last Name'].get().strip(),
            self.entries['First Name'].get().strip(),
            self.entries['DOB (DD-MM-YYYY)'].get().strip(),
            self.entries['Address'].get().strip(),
            float(self.entries['Math Grade'].get().strip()) if self.entries['Math Grade'].get().strip() else None,
            float(self.entries['Literature Grade'].get().strip()) if self.entries[
                'Literature Grade'].get().strip() else None,
            float(self.entries['English Grade'].get().strip()) if self.entries['English Grade'].get().strip() else None
        )

    def __del__(self):
        if hasattr(self, 'db_manager'):
            self.db_manager.close()