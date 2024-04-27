import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Real World Calculator")

        self.current_value = ""
        self.memory_value = None

        self.create_display()
        self.create_buttons()

    def create_display(self):
        self.display = tk.Entry(self.master, width=25, font=("Arial", 20), justify="right")
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

    def create_buttons(self):
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("+", 1, 3), ("C", 1, 4),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3), ("←", 2, 4),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("*", 3, 3), ("%", 3, 4),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("/", 4, 3), ("√", 4, 4),
            ("MC", 5, 0), ("MR", 5, 1), ("MS", 5, 2), ("M+", 5, 3), ("M-", 5, 4),
            ("x^y", 6, 0), ("1/x", 6, 1), ("x^2", 6, 2), ("|x|", 6, 3)
        ]

        for (text, row, col) in buttons:
            button = tk.Button(self.master, text=text, font=("Arial", 16), command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def on_button_click(self, value):
        if value == "=":
            try:
                result = str(eval(self.current_value))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, result)
            except:
                messagebox.showerror("Error", "Invalid input")
        elif value == "C":
            self.clear()
        elif value == "←":
            self.backspace()
        elif value == "MC":
            self.memory_clear()
        elif value == "MR":
            self.memory_recall()
        elif value == "MS":
            self.memory_store()
        elif value == "M+":
            self.memory_add()
        elif value == "M-":
            self.memory_subtract()
        elif value == "x^y":
            self.power()
        elif value == "1/x":
            self.inverse()
        elif value == "x^2":
            self.square()
        elif value == "|x|":
            self.absolute_value()
        elif value == "√":
            self.square_root()
        else:
            self.current_value += value
            self.display.insert(tk.END, value)

    def clear(self):
        self.current_value = ""
        self.display.delete(0, tk.END)

    def backspace(self):
        self.current_value = self.current_value[:-1]
        self.display.delete(len(self.current_value), tk.END)

    def memory_store(self):
        try:
            self.memory_value = eval(self.current_value)
        except:
            messagebox.showerror("Error", "Invalid input")

    def memory_recall(self):
        if self.memory_value is not None:
            self.display.insert(tk.END, str(self.memory_value))

    def memory_clear(self):
        self.memory_value = None

    def memory_add(self):
        try:
            if self.memory_value is not None:
                self.memory_value += eval(self.current_value)
        except:
            messagebox.showerror("Error", "Invalid input")

    def memory_subtract(self):
        try:
            if self.memory_value is not None:
                self.memory_value -= eval(self.current_value)
        except:
            messagebox.showerror("Error", "Invalid input")

    def power(self):
        try:
            self.current_value += "**"
            self.display.insert(tk.END, "^")
        except:
            messagebox.showerror("Error", "Invalid input")

    def inverse(self):
        try:
            value = eval(self.current_value)
            if value != 0:
                result = 1 / value
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            else:
                messagebox.showerror("Error", "Cannot divide by zero")
        except:
            messagebox.showerror("Error", "Invalid input")

    def square(self):
        try:
            value = eval(self.current_value)
            result = value ** 2
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except:
            messagebox.showerror("Error", "Invalid input")

    def absolute_value(self):
        try:
            value = eval(self.current_value)
            result = abs(value)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except:
            messagebox.showerror("Error", "Invalid input")

    def square_root(self):
        try:
            value = eval(self.current_value)
            if value >= 0:
                result = value ** 0.5
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            else:
                messagebox.showerror("Error", "Cannot take square root of a negative number")
        except:
            messagebox.showerror("Error", "Invalid input")

root = tk.Tk()
app = Calculator(root)
root.mainloop()
