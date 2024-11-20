import subprocess
import ollama  # Make sure to run 'ollama pull llama3.2:3b' on terminal in order to download the needed ollama model
import random
import tkinter as tk
from tkinter import scrolledtext

# Set model name to whichever model is used
model_name = "llama3.2:3b"

# Define different prompt variations for each difficulty level
prompts = {
    'easy': [
        "Come up with a simple animal trivia question which has a one-word answer. Use a method of randomizing the question. It must be formatted as follows '||| Question ||| answer to question |||'.",
        "Generate an easy animal trivia question with a one-word answer. Format it like this: '||| Question ||| answer to question |||'.",
        "Create a basic animal trivia question with a single-word answer. It should look like this: '||| Question ||| answer to question |||'.",
        "Make a straightforward animal trivia question with a one-word answer. Use this format: '||| Question ||| answer to question |||'.",
        "Develop a simple animal trivia question that can be answered with one word. Format it like this: '||| Question ||| answer to question |||'.",
        "Come up with an easy animal trivia question that requires a single-word answer. It must be formatted as follows '||| Question ||| answer to question |||'.",
        "Generate a basic animal trivia question that can be answered with one word. Use this format: '||| Question ||| answer to question |||'.",
        "Create an easy animal trivia question that requires a one-word answer. It should look like this: '||| Question ||| answer to question |||'.",
        "Make a simple animal trivia question with a single-word answer. Format it like this: '||| Question ||| answer to question |||'.",
        "Develop an easy animal trivia question that has a one-word answer. Use this format: '||| Question ||| answer to question |||'."
    ],
    'medium': [
        "Create a moderately difficult animal trivia question with a one-word answer. It should look like this: '||| Question ||| answer to question |||'.",
        "Make a medium-level animal trivia question that can be answered with one word. Format it like this: '||| Question ||| answer to question |||'.",
        "Develop a moderately challenging animal trivia question with a single-word answer. Use this format: '||| Question ||| answer to question |||'.",
        "Come up with a medium-difficulty animal trivia question that requires a one-word answer. It must be formatted as follows '||| Question ||| answer to question |||'.",
        "Generate a moderately difficult animal trivia question that has a one-word answer. Format it like this: '||| Question ||| answer to question |||'.",
        "Create a medium-level animal trivia question with a single-word answer. It should look like this: '||| Question ||| answer to question |||'.",
        "Make a moderately challenging animal trivia question that can be answered with one word. Use this format: '||| Question ||| answer to question |||'.",
        "Develop a medium-difficulty animal trivia question that requires a one-word answer. Format it like this: '||| Question ||| answer to question |||'.",
        "Come up with a moderately difficult animal trivia question that has a one-word answer. It must be formatted as follows '||| Question ||| answer to question |||'.",
        "Generate a medium-level animal trivia question with a one-word answer. Use this format: '||| Question ||| answer to question |||'."
    ],
    'hard': [
        "Create a challenging animal trivia question with a one-word answer. It should look like this: '||| Question ||| answer to question |||'.",
        "Make a difficult animal trivia question that can be answered with one word. Format it like this: '||| Question ||| answer to question |||'.",
        "Develop a hard animal trivia question with a single-word answer. Use this format: '||| Question ||| answer to question |||'.",
        "Come up with a challenging animal trivia question that requires a one-word answer. It must be formatted as follows '||| Question ||| answer to question |||'.",
        "Generate a difficult animal trivia question that has a one-word answer. Format it like this: '||| Question ||| answer to question |||'.",
        "Create a hard animal trivia question with a single-word answer. It should look like this: '||| Question ||| answer to question |||'.",
        "Make a challenging animal trivia question that can be answered with one word. Use this format: '||| Question ||| answer to question |||'.",
        "Develop a difficult animal trivia question that requires a one-word answer. Format it like this: '||| Question ||| answer to question |||'.",
        "Come up with a hard animal trivia question that has a one-word answer. It must be formatted as follows '||| Question ||| answer to question |||'.",
        "Generate a challenging animal trivia question with a one-word answer. Use this format: '||| Question ||| answer to question |||'."
    ]
}

class TriviaGame:
    """Class to manage the animal trivia game, its UI elements, and game logic."""
    def __init__(self):
        """Initialize the game, including difficulty, UI components, and fetching the first question."""
        
        self.streak_mode = False
        self.streak_count = 0

        self.difficulty = 'easy'  # Start at easy difficulty
        self.stop = 0  # Correct answers count
        self.total = 0  # Total questions asked

        # Set up the main window and its properties
        self.root = tk.Tk()
        self.root.title("Trivia Game")
        self.root.state('zoomed')  # Make the window fullscreen

        # Create a canvas for the gradient background
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack()

        # Apply gradient background
        self.gradient_background()

        # Create and position the difficulty label
        self.difficulty_label = tk.Label(self.root, text="Difficulty: Easy", font=("Arial", 24), fg="white", bg="#3b3f54")
        self.difficulty_label.place(relx=0.5, rely=0.05, anchor="center")

        # Create and position the question label
        self.question_label = tk.Label(self.root, text="", wraplength=800, font=("Arial", 24), fg="white", bg="#3b3f54")
        self.question_label.place(relx=0.5, rely=0.15, anchor="center")

        # Create the answer entry box
        self.answer_entry = tk.Entry(self.root, font=("Arial", 24), fg="black", bg="#FF69B4")
        self.answer_entry.place(relx=0.5, rely=0.25, anchor="center")
        self.answer_entry.focus_set()

        # Bind the Enter key to trigger the check_answer function
        self.root.bind("<Return>", self.check_answer)

        # Create and position the feedback label
        self.feedback_label = tk.Label(self.root, text="", wraplength=800, font=("Arial", 24), fg="white", bg="#3b3f54")
        self.feedback_label.place(relx=0.5, rely=0.35, anchor="center")

        # Create a scrollable text box for displaying previous questions and answers
        self.text_box = scrolledtext.ScrolledText(self.root, width=100, height=10, font=("Arial", 18), fg="black", bg="#FF69B4")
        self.text_box.place(relx=0.5, rely=0.6, anchor="center")

        # Create and position the score label
        self.score_label = tk.Label(self.root, text="Score: 0/0", font=("Arial", 24), fg="white", bg="#3b3f54")
        self.score_label.place(relx=0.5, rely=0.9, anchor="center")

        # Fetch and display the first question
        self.get_question()

    def gradient_background(self):
        """Draws a smooth gradient from black to purple on the background canvas."""
        (self.r1, self.g1, self.b1) = (0, 0, 0)  # Start color (black)
        (self.r2, self.g2, self.b2) = (75, 0, 130)  # End color (purple)
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.root.winfo_screenwidth(), self.root.winfo_screenheight(), fill="#3b3f54", outline="#3b3f54")
        # Create the gradient effect using horizontal lines
        for i in range(self.root.winfo_screenheight()):
            r = int(self.r1 + i / self.root.winfo_screenheight() * (self.r2 - self.r1))
            g = int(self.g1 + i / self.root.winfo_screenheight() * (self.g2 - self.g1))
            b = int(self.b1 + i / self.root.winfo_screenheight() * (self.b2 - self.b1))
            self.canvas.create_line(0, i, self.root.winfo_screenwidth(), i, fill="#{:02x}{:02x}{:02x}".format(r, g, b), width=2)

    def get_question(self):
        """Fetches a trivia question from the model, ensuring the answer is in the correct format."""
        prompt = random.choice(prompts[self.difficulty])
        prompt += "Additionally, the first letter of the answer shouldn't be capitalized."

        # Run the model with the chosen prompt using a subprocess call
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding='utf-8',
        )

        ollama_response = result.stdout.strip()
        parsed_array = ollama_response.split('|||')

        # Ensure the response is valid and meets criteria
        while len(parsed_array) < 3 or len(parsed_array[2].strip().split()) > 1:
            result = subprocess.run(
                ["ollama", "run", model_name, prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                encoding='utf-8',
            )
            ollama_response = result.stdout.strip()
            parsed_array = ollama_response.split('|||')

        # Assign the answer and lowercase its first letter if necessary
        self.answer = parsed_array[2].strip()
        if self.answer and self.answer[0].isupper():
            self.answer = self.answer[0].lower() + self.answer[1:]

        # Display the question text
        self.question_label['text'] = parsed_array[1]
        print(self.answer)
        # Update the total number of questions asked and update the score label
        self.total += 1
        self.score_label['text'] = f"Score: {self.stop}/{self.total}"

        # Update the background based on the current difficulty level
        if self.difficulty == 'easy':
            self.gradient_background_easy()
        elif self.difficulty == 'medium':
            self.gradient_background_medium()
        elif self.difficulty == 'hard' and self.streak_mode == False:
            self.gradient_background_hard()

    def gradient_background_easy(self):
        '''Sets background when difficulty is easy to specified gradient'''
        (self.r1, self.g1, self.b1) = (0, 0, 0)
        (self.r2, self.g2, self.b2) = (0, 255, 0)
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.root.winfo_screenwidth(), self.root.winfo_screenheight(), fill="#3b3f54", outline="#3b3f54")
        for i in range(self.root.winfo_screenheight()):
            r = int(self.r1 + i / self.root.winfo_screenheight() * (self.r2 - self.r1))
            g = int(self.g1 + i / self.root.winfo_screenheight() * (self.g2 - self.g1))
            b = int(self.b1 + i / self.root.winfo_screenheight() * (self.b2 - self.b1))
            self.canvas.create_line(0, i, self.root.winfo_screenwidth(), i, fill="#{:02x}{:02x}{:02x}".format(r, g, b), width=2)


    def gradient_background_medium(self):
        '''Sets background when difficulty is medium to specified gradient'''

        (self.r1, self.g1, self.b1) = (255, 255, 0)
        (self.r2, self.g2, self.b2) = (255, 0, 0)
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.root.winfo_screenwidth(), self.root.winfo_screenheight(), fill="#3b3f54", outline="#3b3f54")
        for i in range(self.root.winfo_screenheight()):
            r = int(self.r1 + i / self.root.winfo_screenheight() * (self.r2 - self.r1))
            g = int(self.g1 + i / self.root.winfo_screenheight() * (self.g2 - self.g1))
            b = int(self.b1 + i / self.root.winfo_screenheight() * (self.b2 - self.b1))
            self.canvas.create_line(0, i, self.root.winfo_screenwidth(), i, fill="#{:02x}{:02x}{:02x}".format(r, g, b), width=2)

    def gradient_background_hard(self):
        '''Sets background when difficulty is hard to specified gradient'''

        (self.r1, self.g1, self.b1) = (0, 0, 255)
        (self.r2, self.g2, self.b2) = (75, 0, 130)
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.root.winfo_screenwidth(), self.root.winfo_screenheight(), fill="#3b3f54", outline="#3b3f54")
        for i in range(self.root.winfo_screenheight()):
            r = int(self.r1 + i / self.root.winfo_screenheight() * (self.r2 - self.r1))
            g = int(self.g1 + i / self.root.winfo_screenheight() * (self.g2 - self.g1))
            b = int(self.b1 + i / self.root.winfo_screenheight() * (self.b2 - self.b1))
            self.canvas.create_line(0, i, self.root.winfo_screenwidth(), i, fill="#{:02x}{:02x}{:02x}".format(r, g, b), width=2)

    def check_answer(self, event):
        """Checks if the player's answer is correct and updates the score."""
        user_input = self.answer_entry.get()

        # Log the question and user's answer in the text box
        self.text_box.insert(tk.END, "Question: " + self.question_label['text'] + "\n")
        self.text_box.insert(tk.END, "Your answer: " + user_input + "\n")

        # Check if the user's answer matches the correct answer
        if user_input == self.answer:
            self.streak_count += 1
            if self.streak_count >= 2 and not self.streak_mode:
                self.streak_mode = True
                self.difficulty_label['text'] = "Streak: 2"
                self.gradient_background_streak()
            elif self.streak_mode:
                self.difficulty_label['text'] = f"Streak: {self.streak_count}"
            self.feedback_label['text'] = "Good Job! That is the right answer"
            self.text_box.insert(tk.END, "Feedback: Good Job! That is the right answer\n\n")
            self.stop += 1

            # Increase difficulty if correct
            if self.difficulty == 'easy':
                self.difficulty = 'medium'
                self.difficulty_label['text'] = "Difficulty: Medium"
            elif self.difficulty == 'medium':
                self.difficulty = 'hard'
                self.difficulty_label['text'] = "Difficulty: Hard"
        else:
            self.streak_mode = False
            self.streak_count = 0
            self.difficulty_label['text'] = f"Difficulty: {self.difficulty.capitalize()}"
            if self.difficulty == 'easy':
                self.gradient_background_easy()
            elif self.difficulty == 'medium':
                self.gradient_background_medium()
            elif self.difficulty == 'hard' and not self.streak_mode:
                self.gradient_background_hard()
            self.feedback_label['text'] = "Wrong, better luck next time..."
            self.text_box.insert(tk.END, "Feedback: Wrong, better luck next time...\n")
            self.text_box.insert(tk.END, "The answer is " + self.answer + "\n\n")

            # Decrease difficulty if incorrect
            if self.difficulty == 'hard':
                self.difficulty = 'medium'
                self.difficulty_label['text'] = "Difficulty: Medium"
            elif self.difficulty == 'medium':
                self.difficulty = 'easy'
                self.difficulty_label['text'] = "Difficulty: Easy"

        # Clear the answer entry and fetch a new question
        self.answer_entry.delete(0, tk.END)
        self.get_question()
    def gradient_background_streak(self):
        '''Sets background when streak mode is active to a randomized gradient'''
        print("background randomized")
        # Generate random colors for gradient start and end
        (self.r1, self.g1, self.b1) = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        (self.r2, self.g2, self.b2) = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # Clear the canvas
        self.canvas.delete("all")
        
        # Draw gradient lines
        for i in range(self.root.winfo_screenheight()):
            r = int(self.r1 + i / self.root.winfo_screenheight() * (self.r2 - self.r1))
            g = int(self.g1 + i / self.root.winfo_screenheight() * (self.g2 - self.g1))
            b = int(self.b1 + i / self.root.winfo_screenheight() * (self.b2 - self.b1))
            # Use the calculated gradient color
            color = "#{:02x}{:02x}{:02x}".format(r, g, b)
            # Draw a line for each row to create the gradient effect
            self.canvas.create_line(0, i, self.root.winfo_screenwidth(), i, fill=color, width=1)
        
        # Update the canvas to ensure changes are displayed
        self.canvas.update()


    def run(self):
        '''Start the main event loop for the GUI'''
        self.root.mainloop()

# Start the trivia game when this script is executed
if __name__ == "__main__":
    game = TriviaGame()
    game.run()