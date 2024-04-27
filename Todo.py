import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List")
        self.master.geometry("600x400")

        self.load_tasks()

        self.task_input = tk.Entry(master, width=50, font=("Arial", 12))
        self.task_input.pack(pady=10, padx=20)

        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        self.add_button = tk.Button(button_frame, text="Add Task", command=self.add_task, width=10, font=("Arial", 12))
        self.add_button.grid(row=0, column=0, padx=5)

        self.complete_button = tk.Button(button_frame, text="Mark as Completed", command=self.mark_as_completed, width=15, font=("Arial", 12))
        self.complete_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(button_frame, text="Delete Task", command=self.confirm_delete_task, width=10, font=("Arial", 12))
        self.delete_button.grid(row=0, column=2, padx=5)

        self.save_button = tk.Button(button_frame, text="Save Tasks", command=self.save_tasks, width=10, font=("Arial", 12))
        self.save_button.grid(row=0, column=3, padx=5)

        self.task_listbox = tk.Listbox(master, width=70, height=15, font=("Arial", 12))
        self.task_listbox.pack(pady=10, padx=20)

        self.refresh_listbox()

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_task(self):
        task = self.task_input.get()
        if task:
            due_date = self.get_due_date()
            priority = self.get_priority()
            category = self.get_category()
            self.tasks.append({"task": task, "completed": False, "due_date": due_date, "priority": priority, "category": category})
            self.refresh_listbox()
            self.task_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def mark_as_completed(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            self.tasks[index]["completed"] = True
            self.refresh_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as completed!")

    def confirm_delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            if messagebox.askokcancel("Delete Task", "Are you sure you want to delete this task?"):
                self.delete_task()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete!")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            del self.tasks[index]
            self.refresh_listbox()

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)
        messagebox.showinfo("Information", "Tasks saved successfully!")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

    def refresh_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task["completed"] else " "
            due_date = f"Due: {task['due_date']}" if task['due_date'] else ""
            priority = f"Priority: {task['priority']}" if task['priority'] else ""
            category = f"Category: {task['category']}" if task['category'] else ""
            self.task_listbox.insert(tk.END, f"{status} {task['task']} - {due_date} - {priority} - {category}")

    def get_due_date(self):
        try:
            due_date = datetime.strptime(simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):"), "%Y-%m-%d")
            return due_date.strftime("%Y-%m-%d")
        except ValueError:
            return None

    def get_priority(self):
        return simpledialog.askstring("Priority", "Enter priority (High/Medium/Low):")

    def get_category(self):
        return simpledialog.askstring("Category", "Enter category:")

    def on_closing(self):
        self.save_tasks()  
        self.master.destroy()

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
