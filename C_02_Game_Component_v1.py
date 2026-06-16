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
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Launches Play class with 5 rounds for testing
        """
        Play(5)
        # Hide root window (ie: hide rounds choice window)
        root.withdraw()


class Play:
    """
    Interface for playing the Capital Cities Quiz
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()
        self.play_box.title("Capital Cities Quiz")

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # Body font for most labels
        body_font = ("Arial", "12")

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), None, 0],
            ["Score: 0", body_font, "#FFF2CC", 1],
            ["What is the capital of... Good luck! 🌍", body_font, "#D5E8D4", 2],
            ["You chose... result will appear here", body_font, "#D5E8D4", 5]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            make_label = Label(self.game_frame, text=item[0], font=item[1],
                               bg=item[2], wraplength=300, justify="left")
            make_label.grid(row=item[3], pady=10, padx=10)
            play_labels_ref.append(make_label)

        # Retrieve labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.score_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # Country name label (the question)
        self.country_label = Label(self.game_frame, text="Country Name",
                                   font=("Arial", 14, "bold"),
                                   bg="#FFFFFF", relief="solid", width=25)
        self.country_label.grid(row=3, pady=10, padx=10)

        # Hint text label (updated when 50/50 is used)
        self.hint_label = Label(self.game_frame, text="",
                                font=body_font, bg="#FFF2CC",
                                wraplength=300, justify="left")
        self.hint_label.grid(row=4, pady=5, padx=10)

        # Frame for 4 answer buttons in a 2x2 grid
        self.answer_frame = Frame(self.game_frame)
        self.answer_frame.grid(row=6)

        # Create four answer buttons in a 2x2 grid
        for item in range(0, 4):
            self.answer_button = Button(self.answer_frame, font=("Arial", 12),
                                        text="Capital City", width=15)
            self.answer_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)

        # Frame to hold hint and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=8)

        # Button details (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", "", 21, 7, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 16, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 16, 0, 1],
            [self.game_frame, "End Game", "#990000", self.close_play, 21, 9, None]
        ]

        # Create buttons and add to reference list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)
            control_ref_list.append(make_control_button)

        # Store button references for enabling/disabling later
        self.next_button = control_ref_list[0]
        self.hint_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]

    def close_play(self):
        """
        Closes the play window and returns to the start screen
        """
        # Reshow start screen and close quiz window
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Capital Cities Quiz")
    StartGame()
    root.mainloop()