import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.length_var = tk.IntVar(value=12)
        self.include_lowercase = tk.BooleanVar(value=True)
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_special_chars = tk.BooleanVar(value=False)
        self.password_strength_var = tk.StringVar()
        self.generated_password = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        header_label = tk.Label(self.root, text="Password Generator", font=("Helvetica", 20, "bold"))
        header_label.pack(pady=10)

        length_frame = tk.Frame(self.root)
        length_frame.pack()
        length_label = tk.Label(length_frame, text="Password Length:", font=("Helvetica", 12))
        length_label.grid(row=0, column=0, padx=10, pady=5)
        self.length_entry = tk.Entry(length_frame, textvariable=self.length_var, font=("Helvetica", 12), width=10)
        self.length_entry.grid(row=0, column=1, padx=10, pady=5)

        char_type_frame = tk.Frame(self.root)
        char_type_frame.pack(pady=5)
        lowercase_check = tk.Checkbutton(char_type_frame, text="Lowercase", variable=self.include_lowercase, font=("Helvetica", 12))
        lowercase_check.grid(row=0, column=0, padx=10)
        uppercase_check = tk.Checkbutton(char_type_frame, text="Uppercase", variable=self.include_uppercase, font=("Helvetica", 12))
        uppercase_check.grid(row=0, column=1, padx=10)
        digits_check = tk.Checkbutton(char_type_frame, text="Digits", variable=self.include_digits, font=("Helvetica", 12))
        digits_check.grid(row=0, column=2, padx=10)
        special_chars_check = tk.Checkbutton(char_type_frame, text="Special Characters", variable=self.include_special_chars, font=("Helvetica", 12))
        special_chars_check.grid(row=0, column=3, padx=10)

        generate_button = tk.Button(self.root, text="Generate Password", command=self.generate_password, font=("Helvetica", 12))
        generate_button.pack(pady=10)

        strength_frame = tk.Frame(self.root)
        strength_frame.pack(pady=5)
        strength_label = tk.Label(strength_frame, text="Password Strength:", font=("Helvetica", 12))
        strength_label.grid(row=0, column=0, padx=10, pady=5)
        self.strength_indicator = tk.Label(strength_frame, textvariable=self.password_strength_var, font=("Helvetica", 12, "bold"), fg="green")
        self.strength_indicator.grid(row=0, column=1, padx=10, pady=5)

        password_label = tk.Label(self.root, textvariable=self.generated_password, font=("Helvetica", 16, "bold"))
        password_label.pack(pady=10)

        copy_button = tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard, font=("Helvetica", 12))
        copy_button.pack(pady=5)

        save_button = tk.Button(self.root, text="Save Password", command=self.save_password, font=("Helvetica", 12))
        save_button.pack(pady=5)

    def generate_password(self):
        password_length = self.length_var.get()

        if password_length <= 0:
            messagebox.showerror("Error", "Please enter a valid password length.")
            return

        character_pool = ''
        if self.include_lowercase.get():
            character_pool += string.ascii_lowercase
        if self.include_uppercase.get():
            character_pool += string.ascii_uppercase
        if self.include_digits.get():
            character_pool += string.digits
        if self.include_special_chars.get():
            character_pool += string.punctuation

        if len(character_pool) == 0:
            messagebox.showerror("Error", "Please select at least one character type.")
            return

        password = ''.join(random.choices(character_pool, k=password_length))
        self.generated_password.set(password)
        self.check_password_strength(password)

    def check_password_strength(self, password):
        strength = 0
        if any(char in string.ascii_lowercase for char in password):
            strength += 1
        if any(char in string.ascii_uppercase for char in password):
            strength += 1
        if any(char in string.digits for char in password):
            strength += 1
        if any(char in string.punctuation for char in password):
            strength += 1

        if len(password) >= 12 and strength >= 3:
            self.password_strength_var.set("Strong")
            self.strength_indicator.config(fg="green")
        elif len(password) >= 8 and strength >= 2:
            self.password_strength_var.set("Moderate")
            self.strength_indicator.config(fg="orange")
        else:
            self.password_strength_var.set("Weak")
            self.strength_indicator.config(fg="red")

    def copy_to_clipboard(self):
        password = self.generated_password.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Info", "Password copied to clipboard.")
        else:
            messagebox.showerror("Error", "No password generated.")

    def save_password(self):
        password = self.generated_password.get()
        if password:
            try:
                filename = "passwords.txt"
                with open(filename, "a") as f:
                    f.write(password + "\n")
                messagebox.showinfo("Info", f"Password saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving password: {str(e)}")
        else:
            messagebox.showerror("Error", "No password generated.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
