import tkinter as tk
from tkinter import messagebox
import random

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Game")
        self.master.geometry("600x400")
        self.master.configure(bg="#f0f0f0")

        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Rome"],
                "correct_answer": "Paris"
            },
            {
                "question": "Who wrote 'Romeo and Juliet'?",
                "options": ["William Shakespeare", "Charles Dickens", "Jane Austen", "Leo Tolstoy"],
                "correct_answer": "William Shakespeare"
            },
            {
                "question": "What is the powerhouse of the cell?",
                "options": ["Nucleus", "Ribosome", "Mitochondria", "Endoplasmic Reticulum"],
                "correct_answer": "Mitochondria"
            },
            {
                "question": "What is the chemical symbol for water?",
                "options": ["H2O", "CO2", "O2", "NaCl"],
                "correct_answer": "H2O"
            },
            {
                "question": "What year did the Titanic sink?",
                "options": ["1910", "1912", "1915", "1918"],
                "correct_answer": "1912"
            },
            {
                "question": "Who is known as the father of the Indian nation?",
                "options": ["Mahatma Gandhi", "Jawaharlal Nehru", "Subhash Chandra Bose", "Bhagat Singh"],
                "correct_answer": "Mahatma Gandhi"
            },
            {
                "question": "Which battle marked the end of the Maratha Empire?",
                "options": ["Battle of Plassey", "Battle of Buxar", "Third Battle of Panipat", "Battle of Talikota"],
                "correct_answer": "Third Battle of Panipat"
            },
            {
                "question": "Who was the first female Prime Minister of India?",
                "options": ["Indira Gandhi", "Sarojini Naidu", "Pratibha Patil", "Sonia Gandhi"],
                "correct_answer": "Indira Gandhi"
            },
            {
                "question": "Who was the last ruler of the Maurya dynasty?",
                "options": ["Chandragupta Maurya", "Bindusara", "Ashoka", "Brihadratha"],
                "correct_answer": "Brihadratha"
            },
            {
                "question": "Where was the Indian National Congress formed in 1885?",
                "options": ["Bombay", "Calcutta", "Madras", "Allahabad"],
                "correct_answer": "Bombay"
            }
        ]

        self.current_question = 0
        self.score = 0

        self.question_label = tk.Label(master, text="", font=("Helvetica", 16), bg="#f0f0f0", wraplength=500, justify="center")
        self.question_label.pack(pady=20)

        self.option_buttons = []

        for i in range(4):
            btn = tk.Button(master, text="", command=lambda i=i: self.select_option(i), font=("Helvetica", 12), bg="#f0f0f0", bd=1)
            self.option_buttons.append(btn)
            btn.pack(pady=5)

        self.submit_button = tk.Button(master, text="Submit", command=self.check_answer, font=("Helvetica", 14))
        self.submit_button.pack(pady=20)

        self.load_quiz()
        self.ask_question()

    def load_quiz(self):
        random.shuffle(self.questions)

    def ask_question(self):
        if self.current_question < len(self.questions):
            q_data = self.questions[self.current_question]
            self.question_label.config(text=q_data["question"])

            options = random.sample(q_data["options"], len(q_data["options"]))
            for i in range(4):
                self.option_buttons[i].config(text=options[i], bg="#f0f0f0")

        else:
            self.show_result()

    def select_option(self, index):
        for i in range(4):
            if i == index:
                self.option_buttons[i].config(bg="#FFFF00")  
            else:
                self.option_buttons[i].config(bg="#f0f0f0")  

    def check_answer(self):
        user_answer = ""
        for i in range(4):
            if self.option_buttons[i].cget("bg") == "#FFFF00":
                user_answer = self.option_buttons[i].cget("text")
                break

        correct_answer = self.questions[self.current_question]["correct_answer"]

        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct", "Your answer is correct!")
        else:
            messagebox.showerror("Incorrect", f"Sorry, the correct answer is {correct_answer}")

        self.current_question += 1
        self.ask_question()

    def show_result(self):
        result_text = f"Quiz Completed!\nYour Score: {self.score}/{len(self.questions)}"
        if self.score == len(self.questions):
            result_text += "\nCongratulations! You got all the answers correct!"
        elif self.score >= len(self.questions) // 2:
            result_text += "\nNot bad! You got more than half of the answers correct."
        else:
            result_text += "\nYou need to brush up on your knowledge. Better luck next time!"

        messagebox.showinfo("Quiz Result", result_text)

        play_again = messagebox.askyesno("Play Again", "Do you want to play again?")
        if play_again:
            self.current_question = 0
            self.score = 0
            self.load_quiz()
            self.ask_question()
        else:
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
