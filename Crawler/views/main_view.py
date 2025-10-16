import tkinter as tk
from collections import Counter
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from datetime import datetime
from crawler.student_api import StudentApi
import os
import pandas as pd

class MainView:
    def __init__(self, root):
        self.root = root
        self.students = []
        self.display_entry = None
        self.root.title("Crawl")
        self.current_plot_widget = None
        self.create_widgets()
        self.root.state('zoomed')

    def create_widgets(self):
        self.create_header()
        self.create_button()
        self.create_body()
        self.create_chart_frame()

    def create_header(self):
        top_frame = tk.Frame(self.root, bg='#2c3e50', pady=10)
        top_frame.pack(fill=tk.X)
        tk.Label(top_frame, text="Crawler",font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack()

    def create_button(self):
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Crawl", command=self.crawl_data, bg='#27ae60', fg='white', padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Plot Data", command=self.plot_data, bg='#27ae60', fg='white', padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Export CSV", command=self.export_csv, bg='#27ae60', fg='white', padx=15, pady=5).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Export Excel", command=self.export_xls, bg='#27ae60', fg='white', padx=15, pady=5).pack(
        side=tk.LEFT, padx=5)
    def export_csv(self):
        if not self.students:
            messagebox.showerror("Error", "Please crawl data first.")
            return

        try:
            filename = 'export.csv'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('Student ID,Last Name,First Name,DOB,Address,Math Grade,Literature Grade,English Grade\n')
                for student in self.students:
                    f.write(f"{student.student_id},{student.lastname},{student.firstname},{student.dob},{student.address},{student.math_grade},{student.literature_grade},{student.english_grade}\n")
            os.startfile(filename)
        except Exception as e:
            messagebox.showerror("Error", "Failed")

    def export_xls(self):
        if not self.students:
            messagebox.showerror("Error", "Please crawl data first.")
            return
        try:
            data = []
            for student in self.students:
                data.append({
                    'Student ID': student.student_id,
                    'Last Name': student.lastname,
                    'First Name': student.firstname,
                    'DOB': student.dob,
                    'Address': student.address,
                    'Math Grade': student.math_grade,
                    'Literature Grade': student.literature_grade,
                    'English Grade': student.english_grade
                })
            df = pd.DataFrame(data)
            filename = 'export.xlsx'
            df.to_excel(filename, index=False)
            os.startfile(filename)
        except Exception as e:
            messagebox.showerror("Error", "Failed")


    def create_body(self):
        body_frame = tk.Frame(self.root, height=200)
        body_frame.pack(fill=tk.X,padx=10, pady=10)
        body_frame.pack_propagate(False)
        scrollbar = tk.Scrollbar(body_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.display_entry = tk.Text(body_frame,
                                     yscrollcommand=scrollbar.set,
                                     wrap=tk.WORD)
        self.display_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.display_entry.yview)


    def create_chart_frame(self):
        chart_frame = tk.Frame(self.root, pady=10)
        chart_frame.pack(fill=tk.BOTH, expand=True)

        self.chart_canvas = tk.Canvas(chart_frame, bg='white', height=200)
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


    def crawl_data(self):
        api = StudentApi()
        self.students = api.fetch_all_students()
        self.display_entry.delete('1.0', tk.END)

        for student in self.students:
            self.display_entry.insert('1.0', student)

    def plot_data(self):
        if not self.students:
            messagebox.showerror("Error", "Please crawl data first.")
            return

        if self.current_plot_widget:
            self.current_plot_widget.destroy()

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Student Data Analysis', fontsize=14, fontweight='bold')

        #Graph 1: Student Count by Birth Month
        month_count = defaultdict(int)
        for student in self.students:
            if student.dob:
                try:
                    date_obj = datetime.strptime(str(student.dob), '%d-%m-%Y')
                    month = date_obj.month
                    month_count[month] += 1
                except:
                    continue

        months = list(range(1, 13))
        counts = [month_count.get(m, 0) for m in months]

        axes[0, 0].plot(months, counts, marker='o', color='steelblue', linewidth=2, markersize=6)
        axes[0, 0].set_title('Student Count by Birth Month', fontsize=10, fontweight='bold')
        axes[0, 0].set_xlabel('Month', fontsize=9)
        axes[0, 0].set_ylabel('Number of Students', fontsize=9)
        axes[0, 0].set_xticks(months)
        axes[0, 0].grid(True, alpha=0.3, linestyle='--')
        axes[0, 0].tick_params(labelsize=8)

        # Graph 2: Student Classification by Average Grade
        categories = {
            'Not Graduate': 0,
            'Good': 0,
            'Very Good': 0,
            'Excellent': 0
        }

        for student in self.students:
            if student.math_grade is None or student.literature_grade is None or student.english_grade is None:
                categories['Not Graduate'] += 1
            else:
                avg = (student.math_grade + student.literature_grade + student.english_grade) / 3
                if avg > 9:
                    categories['Excellent'] += 1
                elif avg > 8:
                    categories['Very Good'] += 1
                elif avg > 6:
                    categories['Good'] += 1
                else:
                    categories['Not Graduate'] += 1

        if categories:
            labels = list(categories.keys())
            sizes = list(categories.values())

            colors = []
            for label in labels:
                if label == 'Not Graduate':
                    colors.append('#e74c3c')
                elif label == 'Good':
                    colors.append('#f39c12')
                elif label == 'Very Good':
                    colors.append('#3498db')
                elif label == 'Excellent':
                    colors.append('#2ecc71')

            wedges, texts, autotexts = axes[0, 1].pie(
                sizes,
                labels=labels,
                colors=colors,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 9}
            )

            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(8)

            axes[0, 1].set_title('Student Classification by Average Grade', fontsize=10, fontweight='bold')
        else:
            axes[0, 1].text(0.5, 0.5, 'No data available',
                            horizontalalignment='center',
                            verticalalignment='center',
                            fontsize=12)
            axes[0, 1].set_title('Student Classification by Average Grade', fontsize=10, fontweight='bold')

        #Graph 3: Average by address
        counts = defaultdict(int)
        address_grades = defaultdict(list)
        for student in self.students:
            if student.address:
                counts[student.address]+=1
                if student.math_grade is not None and student.literature_grade is not None and student.english_grade is not None:
                    avg_grade = (student.math_grade + student.literature_grade + student.english_grade) / 3
                    address_grades[student.address].append(avg_grade)

        addresses = []
        averages = []
        student_counts = []
        for address in address_grades:
            grades = address_grades[address]
            student_counts.append(counts[address])
            if grades:
                addresses.append(address)
                averages.append(sum(grades) / len(grades))

        if addresses:
            bars = axes[1, 0].bar(range(len(addresses)), averages, color='steelblue', alpha=0.7)
            axes[1, 0].set_title('Average Grade by Address', fontsize=10, fontweight='bold')
            axes[1, 0].set_xlabel('Address', fontsize=9)
            axes[1, 0].set_ylabel('Average Grade', fontsize=9)
            axes[1, 0].set_xticks(range(len(addresses)))
            axes[1, 0].set_xticklabels(addresses, rotation=45, ha='right', fontsize=8)
            axes[1, 0].grid(axis='y', alpha=0.3, linestyle='--')
            axes[1, 0].tick_params(labelsize=8)

            for i in range(len(bars)):
                bar = bars[i]
                avg = averages[i]
                height = bar.get_height()
                x_position = bar.get_x() + bar.get_width() / 2.

                axes[1, 0].text(x_position, height, f'{avg:.1f}',
                                ha='center', va='bottom', fontsize=8)

            overall_avg = sum(averages) / len(averages)
            axes[1, 0].axhline(y=overall_avg, color='red', linestyle='--', linewidth=1, alpha=0.5,
                               label=f'Overall Avg: {overall_avg:.1f}')
            axes[1, 0].legend(fontsize=8)


        bars1 = axes[1, 1].bar(range(len(addresses)), student_counts, color='steelblue', alpha=0.7)
        axes[1, 1].set_title('Number of student by Address', fontsize=10, fontweight='bold')
        axes[1, 1].set_xlabel('Address', fontsize=9)
        axes[1, 1].set_ylabel('Number of Student', fontsize=9)
        axes[1, 1].set_xticks(range(len(addresses)))
        axes[1, 1].set_xticklabels(addresses, rotation=45, ha='right', fontsize=8)
        axes[1, 1].grid(axis='y', alpha=0.3, linestyle='--')
        axes[1, 1].tick_params(labelsize=8)

        for i in range(len(bars)):
            bar1 = bars1[i]
            height = bar1.get_height()
            x_position = bar1.get_x() + bar1.get_width() / 2.
            axes[1, 1].text(x_position, height, f'{student_counts[i]}',
                            ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        plot_frame = tk.Frame(self.chart_canvas)
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.current_plot_widget = plot_frame
        self.chart_canvas.create_window(0, 0, window=plot_frame, anchor='nw')
        self.chart_canvas.update_idletasks()
        plot_frame.update_idletasks()
        self.chart_canvas.configure(scrollregion=self.chart_canvas.bbox('all'))