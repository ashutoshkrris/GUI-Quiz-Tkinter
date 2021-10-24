from tkinter import Tk, Canvas, StringVar, Label, Radiobutton, Button, messagebox
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain) -> None:
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("iQuiz App")
        self.window.geometry("850x530")

        # Display Title
        self.display_title()

        # Creating a canvas for question text, and dsiplay question
        self.canvas = Canvas(width=800, height=250)
        self.question_text = self.canvas.create_text(400, 125,
                                                     text="Question here",
                                                     width=680,
                                                     fill=THEME_COLOR,
                                                     font=(
                                                         'Ariel', 15, 'italic')
                                                     )
        self.canvas.grid(row=2, column=0, columnspan=2, pady=50)
        self.display_question()

        # Declare a StringVar to store user's answer
        self.user_answer = StringVar()

        # Display four options(radio buttons)
        self.opts = self.radio_buttons()
        self.display_options()

        # To show whether the answer is correct or wrong
        self.feedback = Label(self.window, pady=10, font=("ariel", 15, "bold"))
        self.feedback.place(x=300, y=380)

        # Next and Quit Button
        self.buttons()

        # Mainloop
        self.window.mainloop()

    def display_title(self):
        """To display title"""

        # Title
        title = Label(self.window, text="iQuiz Application",
                      width=50, bg="green", fg="white", font=("ariel", 20, "bold"))

        # place of the title
        title.place(x=0, y=2)

    def display_question(self):
        """To display the question"""

        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)

    def radio_buttons(self):
        """To create four options (radio buttons)"""

        # initialize the list with an empty list of options
        choice_list = []

        # position of the first option
        y_pos = 220

        # adding the options to the list
        while len(choice_list) < 4:

            # setting the radio button properties
            radio_btn = Radiobutton(self.window, text="", variable=self.user_answer,
                                    value='', font=("ariel", 14))

            # adding the button to the list
            choice_list.append(radio_btn)

            # placing the button
            radio_btn.place(x=200, y=y_pos)

            # incrementing the y-axis position by 40
            y_pos += 40

        # return the radio buttons
        return choice_list

    def display_options(self):
        """To display four options"""

        val = 0

        # deselecting the options
        self.user_answer.set(None)

        # looping over the options to be displayed for the
        # text of the radio buttons.
        for option in self.quiz.current_question.choices:
            self.opts[val]['text'] = option
            self.opts[val]['value'] = option
            val += 1

    def next_btn(self):
        """To show feedback for each answer and keep checking for more questions"""

        # Check if the answer is correct
        if self.quiz.check_answer(self.user_answer.get()):
            self.feedback["fg"] = "green"
            self.feedback["text"] = 'Correct answer! \U0001F44D'
        else:
            self.feedback['fg'] = 'red'
            self.feedback['text'] = ('\u274E Oops! \n'
                                     f'The right answer is: {self.quiz.current_question.correct_answer}')

        if self.quiz.has_more_questions():
            # Moves to next to display next question and its options
            self.display_question()
            self.display_options()
        else:
            # if no more questions, then it displays the score
            self.display_result()

            # destroys the self.window
            self.window.destroy()

    def buttons(self):
        """To show next button and quit button"""

        # The first button is the Next button to move to the
        # next Question
        next_button = Button(self.window, text="Next", command=self.next_btn,
                             width=10, bg="green", fg="white", font=("ariel", 16, "bold"))

        # palcing the button  on the screen
        next_button.place(x=350, y=460)

        # This is the second button which is used to Quit the self.window
        quit_button = Button(self.window, text="Quit", command=self.window.destroy,
                             width=5, bg="red", fg="white", font=("ariel", 16, " bold"))

        # placing the Quit button on the screen
        quit_button.place(x=700, y=50)

    def display_result(self):
        """To display the result using messagebox"""
        correct, wrong, score_percent = self.quiz.get_score()

        correct = f"Correct: {correct}"
        wrong = f"Wrong: {wrong}"

        # calculates the percentage of correct answers
        result = f"Score: {score_percent}%"

        # Shows a message box to display the result
        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}")
