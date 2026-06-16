from tkinter import *
from functools import partial  # To prevent unwanted windows


class StartGame:
    """
    Initial Game interface (asks users how many rounds they
    would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Create play button (simplified for testing Play class)
        self.play_button = Button(self.start_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1, padx=20, pady=20)

    def check_rounds(self):
        """
        Launches Play class with 5 rounds for testing
        """
        rounds_wanted = 5
        self.to_play(rounds_wanted)

    def to_play(self, num_rounds):
        """
        Invokes game GUI and takes across number of rounds to be played
        """
        Play(num_rounds)
        # Hide root window (ie: hide rounds choice)
        root.withdraw()


class Play:
    """
    Interface for playing the Capital Cities Quiz
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()
        self.play_box.title("Country Capitals")

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Country Capitals",
                                   font=("Arial", 16, "bold"), padx=5, pady=5)
        self.heading_label.grid(row=0)

        # Hints button - launches the DisplayHints class
        self.hints_button = Button(self.game_frame, font=("Arial", 14, "bold"),
                                   text="50:50", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10,
                                   command=self.to_hints)
        self.hints_button.grid(row=1)

    def to_hints(self):
        """
        Displays hints/help information for playing the game
        """
        DisplayHints(self)


class DisplayHints:
    """
    Displays help / hints dialogue box
    """

    def __init__(self, partner):

        # Setup dialogue box
        background = "#ffe6cc"
        self.help_box = Toplevel()
        self.help_box.title("Help/50:50")

        # Disable hints button while help is open
        partner.hints_button.config(state=DISABLED)

        # If user presses X at the top, close help and re-enable button
        self.help_box.protocol("WM_DELETE_WINDOW",
                               partial(self.close_hints, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, text="Hints / Help",
                                        font=("Arial", 14, "bold"),
                                        bg=background)
        self.help_heading_label.grid(row=0, pady=10)

        # Give user the instructions on what the 50:50 (chance) button is
        help_text = ("When you use the 50:50 button during the quiz, you will "
                     "be given a 50/50 chance!\n\n"
                     "Two of the four wrong answers will be removed, leaving "
                     "you with just two options - the correct answer and one wrong answer.\n\n"
                     "However, using hints affects your score:\n\n"
                     "Correct answer (no hint):     +10 points\n"
                     "Correct answer (with hint):    +4 points\n\n"
                     "Wrong answer (no hint):        -3 points\n"
                     "Wrong answer (with hint):      -5 points\n\n"
                     "Think carefully before using your 50/50 - "
                     "it could cost you more if you get it wrong!\n\n"
                     "Good luck! \U0001f340")

        self.help_text_label = Label(self.help_frame, text=help_text,
                                     wraplength=350, justify="left",
                                     bg=background, padx=10, pady=5)
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame, font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#CC6600", fg="#FFFFFF",
                                     command=partial(self.close_hints, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    def close_hints(self, partner):
        """
        Closes hints dialogue box and re-enables hints button
        """
        # Put hints button back to normal
        partner.hints_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Capital Cities Quiz")
    StartGame()
    root.mainloop()