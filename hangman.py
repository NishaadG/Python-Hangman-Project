import os
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f4f9")
        
        self.word = self.get_random_word().upper()
        self.tries = 6
        self.guesses = ' '
        
        script_dir = os.path.dirname(__file__)
        self.hangman_images = [
            ImageTk.PhotoImage(Image.open(os.path.join(script_dir, 'hangman1.jpg'))),
            ImageTk.PhotoImage(Image.open(os.path.join(script_dir, 'hangman2.jpg'))),
            ImageTk.PhotoImage(Image.open(os.path.join(script_dir, 'hangman3.jpg'))),
            ImageTk.PhotoImage(Image.open(os.path.join(script_dir, 'hangman4.jpg'))),
            ImageTk.PhotoImage(Image.open(os.path.join(script_dir, 'hangman5.jpg'))),
            ImageTk.PhotoImage(Image.open(os.path.join(script_dir, 'hangman6.jpg'))),
            ImageTk.PhotoImage(Image.open(os.path.join(script_dir, 'hangman7.jpg')))
        ]
        
        self.setup_ui()
        self.update_word_display()
    
    def get_random_word(self):
        try:
            response = requests.get("https://random-word-api.herokuapp.com/word?number=1")
            if response.status_code == 200:
                word = response.json()[0]
                return word
            else:
                return "python"
        except Exception as e:
            return "python"
    
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.main_frame.pack(side="left", padx=20, pady=20)
        
        self.hangman_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.hangman_frame.pack(side="right", padx=20, pady=20)

        self.hangman_label = tk.Label(self.hangman_frame, image=self.hangman_images[0], bg="#f4f4f9")
        self.hangman_label.pack(pady=10)
        
        self.title_label = tk.Label(self.main_frame, text="HANGMAN", font=("Helvetica", 24, "bold"), bg="#f4f4f9", fg="#333")
        self.title_label.pack(pady=10)
        
        self.word_label = tk.Label(self.main_frame, text="", font=("Helvetica", 20, "bold"), bg="#f4f4f9", fg="#555")
        self.word_label.pack(pady=20)
        
        self.tries_label = tk.Label(self.main_frame, text=f"Tries Left: {self.tries}", font=("Helvetica", 16), bg="#f4f4f9", fg="#333")
        self.tries_label.pack(pady=10)
        
        self.buttons_frame = tk.Frame(self.main_frame, bg="#f4f4f9")
        self.buttons_frame.pack(pady=10)
        
        self.letter_buttons = {}
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            button = tk.Button(
                self.buttons_frame, 
                text=letter, 
                width=4, 
                height=2, 
                font=("Helvetica", 14, "bold"), 
                bg="#8e44ad", 
                fg="white", 
                command=lambda l=letter: self.guess_letter(l)
            )
            button.grid(row=i // 7, column=i % 7, padx=5, pady=5)
            self.letter_buttons[letter] = button
        
        self.reset_button = tk.Button(self.main_frame, text="Reset Game", command=self.reset_game, bg="#e74c3c", fg="white", font=("Helvetica", 14, "bold"))
        self.reset_button.pack(pady=10)
    
    def update_word_display(self):
        display_word = ''
        for letter in self.word:
            if letter in self.guesses:
                display_word += letter + ' '
            else:
                display_word += '_ '
        self.word_label.config(text=display_word.strip())
    
    def guess_letter(self, letter):
        if letter in self.guesses:
            messagebox.showinfo("Hangman", f"You've already guessed '{letter}'!")
            return

        self.guesses += letter
        self.letter_buttons[letter].config(state="disabled", bg="#95a5a6")

        if letter in self.word:
            self.update_word_display()
            if "_" not in self.word_label.cget("text"):
                messagebox.showinfo("Hangman", f"Congratulations! You guessed the word: {self.word}")
                self.disable_all_buttons()
        else:
            self.tries -= 1
            self.tries_label.config(text=f"Tries Left: {self.tries}")
            self.update_hangman_image()
            if self.tries == 0:
                messagebox.showinfo("Hangman", f"Game Over! The word was: {self.word}")
                self.disable_all_buttons()
    
    def update_hangman_image(self):
        image_index = 6 - self.tries
        if image_index < 0: 
            image_index = 0
        elif image_index > 6: 
            image_index = 6
        self.hangman_label.config(image=self.hangman_images[image_index])
    
    def disable_all_buttons(self):
        for button in self.letter_buttons.values():
            button.config(state="disabled")
    
    def reset_game(self):
        self.word = self.get_random_word().upper()
        self.tries = 6
        self.guesses = ' '
        self.update_word_display()
        self.tries_label.config(text=f"Tries Left: {self.tries}")
        for button in self.letter_buttons.values():
            button.config(state="normal", bg="#8e44ad")
        self.hangman_label.config(image=self.hangman_images[0])
    

root = tk.Tk()
game = HangmanGame(root)
root.mainloop()
