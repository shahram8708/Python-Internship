import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime, timedelta
from collections import defaultdict

DATA_FILE = 'expenses.json'

def load_expenses():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(DATA_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Expense Tracker")
        self.geometry("700x500")  
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.expenses = load_expenses()

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.Frame(main_frame, padding="10 10 10 10")
        input_frame.pack(fill=tk.X)

        list_frame = ttk.Frame(main_frame, padding="10 0 10 10")
        list_frame.pack(fill=tk.BOTH, expand=True)

        report_frame = ttk.Frame(main_frame, padding="10 10 10 10")
        report_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="Amount:").pack(side=tk.LEFT)
        self.amount_var = tk.DoubleVar()
        ttk.Entry(input_frame, textvariable=self.amount_var, width=15).pack(side=tk.LEFT, padx=5)

        ttk.Label(input_frame, text="Category:").pack(side=tk.LEFT)
        self.category_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.category_var, width=20).pack(side=tk.LEFT, padx=5)

        ttk.Label(input_frame, text="Description:").pack(side=tk.LEFT)
        self.description_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.description_var, width=30).pack(side=tk.LEFT, padx=5)

        ttk.Button(input_frame, text="Add Expense", command=self.add_expense).pack(side=tk.LEFT, padx=10)

        self.listbox = tk.Listbox(list_frame, height=15, width=80, bd=1, relief=tk.SUNKEN, font=('TkDefaultFont', 10))
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Button(report_frame, text="Generate Monthly Report", command=self.generate_monthly_report).pack(side=tk.LEFT, padx=10)
        ttk.Button(report_frame, text="Total Expenses Today", command=lambda: self.calculate_total_expenses('daily')).pack(side=tk.LEFT, padx=10)
        ttk.Button(report_frame, text="Total Expenses This Month", command=lambda: self.calculate_total_expenses('monthly')).pack(side=tk.LEFT, padx=10)
        ttk.Button(report_frame, text="Delete Selected Expense", command=self.delete_expense).pack(side=tk.LEFT, padx=10)

        self.refresh_listbox()

    def add_expense(self):
        amount = self.amount_var.get()
        category = self.category_var.get()
        description = self.description_var.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": date
        }

        self.expenses.append(expense)
        save_expenses(self.expenses)
        self.refresh_listbox()
        self.amount_var.set(0)
        self.category_var.set('')
        self.description_var.set('')
        messagebox.showinfo("Success", "Expense added successfully!")

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for expense in self.expenses:
            self.listbox.insert(tk.END, f"{expense['date']} - {expense['amount']} - {expense['category']} - {expense['description']}")

    def generate_monthly_report(self):
        now = datetime.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_expenses = [e for e in self.expenses if datetime.strptime(e['date'], "%Y-%m-%d %H:%M:%S") >= start_of_month]

        categories = defaultdict(float)
        for expense in monthly_expenses:
            categories[expense['category']] += expense['amount']

        report = "\n".join([f"{category}: {amount}" for category, amount in categories.items()])
        messagebox.showinfo("Monthly Report", report)

    def calculate_total_expenses(self, timeframe):
        now = datetime.now()
        if timeframe == 'daily':
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif timeframe == 'monthly':
            start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        total = sum(e['amount'] for e in self.expenses if datetime.strptime(e['date'], "%Y-%m-%d %H:%M:%S") >= start_time)
        messagebox.showinfo(f"Total Expenses {timeframe.title()}", f"Total {timeframe} expenses: {total}")

    def delete_expense(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select an expense to delete.")
            return

        confirmed = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected expense?")
        if confirmed:
            selected_indices = map(int, selected_indices) 
            selected_indices = sorted(selected_indices, reverse=True) 
            for index in selected_indices:
                del self.expenses[index]

            save_expenses(self.expenses)
            self.refresh_listbox()
            messagebox.showinfo("Success", "Selected expenses have been deleted.")

if __name__ == '__main__':
    app = ExpenseTrackerApp()
    app.mainloop()
