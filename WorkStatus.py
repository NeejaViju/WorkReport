import datetime
import json
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, simpledialog
import pandas as pd


class WorkTracker:
    def __init__(self):
        self.work_entries = []

    def start_tracking(self):
        self.start_time = datetime.datetime.now()

    def stop_tracking(self):
        self.stop_time = datetime.datetime.now()
        elapsed_time = self.stop_time - self.start_time
        self.work_entries.append({"start": self.start_time, "stop": self.stop_time, "elapsed_time": elapsed_time, "tasks": []})

    def record_task(self, task_description):
        self.work_entries[-1]["tasks"].append({"time": datetime.datetime.now(), "description": task_description})

    def save_to_file(self, filename):
        with open(filename, "w") as file:
            json.dump(self.work_entries, file, default=str)

    def load_from_file(self, filename):
        with open(filename, "r") as file:
            self.work_entries = json.load(file)

    def generate_report_data(self):
        report_data = []
        for entry in self.work_entries:
            for task in entry["tasks"]:
                report_data.append({
                    "Work session start": entry["start"],
                    "Work session stop": entry["stop"],
                    "Elapsed time": entry["elapsed_time"],
                    "Task time": task["time"],
                    "Task description": task["description"]
                })
        return report_data

class WorkTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Work Tracker")

        self.tracker = WorkTracker()

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=60)
        self.text_area.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.start_button = self.create_button("Start Tracking", self.start_tracking, 1, 0)
        self.stop_button = self.create_button("Stop Tracking", self.stop_tracking, 1, 1)
        self.record_button = self.create_button("Record Task", self.record_task, 1, 2)
        self.generate_button = self.create_button("Generate Report", self.generate_report, 1, 3)
        self.save_button = self.create_button("Save Data", self.save_data, 2, 0)
        self.load_button = self.create_button("Load Data", self.load_data, 2, 1)
        self.clear_button = self.create_button("Clear", self.clear_text, 2, 2)
        self.exit_button = self.create_button("Exit", self.root.quit, 2, 3)

    def create_button(self, text, command, row, column):
        button = tk.Button(self.root, text=text, command=command)
        button.grid(row=row, column=column, padx=5, pady=5)
        return button

    def start_tracking(self):
        self.tracker.start_tracking()
        self.show_message("Tracking started.")

    def stop_tracking(self):
        self.tracker.stop_tracking()
        self.show_message("Tracking stopped.")

    def record_task(self):
        task_description = self.get_input("Enter task description:")
        if task_description:
            self.tracker.record_task(task_description)
            self.show_message("Task recorded.")
            self.generate_report()  # Automatically update the report

    def generate_report(self):
        report_data = self.tracker.generate_report_data()
        report_df = pd.DataFrame(report_data)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, str(report_df))

    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.tracker.save_to_file(file_path)
            self.show_message("Data saved to file.")

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.tracker.load_from_file(file_path)
            self.show_message("Data loaded from file.")
            self.generate_report()  # Automatically update the report

    def clear_text(self):
        self.text_area.delete(1.0, tk.END)

    def show_message(self, message):
        messagebox.showinfo("Message", message)

    def get_input(self, prompt):
        return simpledialog.askstring("Input", prompt)
    
    def export_excel(self):
        report_data = self.tracker.generate_report_data()
        report_df = pd.DataFrame(report_data)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            report_df.to_excel(file_path, index=False)
            self.show_message("Report data exported to Excel.")
            self.export_excel_button = self.create_button("Export to Excel", self.export_excel, 2, 3)

root = tk.Tk()
app = WorkTrackerApp(root)
root.mainloop()
