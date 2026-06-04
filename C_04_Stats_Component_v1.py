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
        Launches Play class with test data for testing Stats component
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
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        # Test data for Stats component (comment/uncomment to test different scenarios)

        # All correct test data...
        # self.correct_count = 5
        # self.wrong_count = 0
        # self.final_score = 50
        # self.rounds_played.set(5)

        # All wrong test data...
        # self.correct_count = 0
        # self.wrong_count = 5
        # self.final_score = -15
        # self.rounds_played.set(5)

        # Mixed score test data...
        self.correct_count = 3
        self.wrong_count = 2
        self.final_score = 16
        self.rounds_played.set(5)

        self.play_box = Toplevel()
        self.play_box.title("Capital Cities Quiz")

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Capital Cities Quiz",
                                   font=("Arial", 16, "bold"), padx=5, pady=5)
        self.heading_label.grid(row=0)

        # Stats button - launches the Stats class
        self.stats_button = Button(self.game_frame, font=("Arial", 14, "bold"),
                                   text="Stats", width=15, fg="#FFFFFF",
                                   bg="#333333", padx=10, pady=10,
                                   command=self.to_stats)
        self.stats_button.grid(row=1)

    def to_stats(self):
        """
        Retrieves everything needed to display the game statistics
        """

        rounds_played = self.rounds_played.get()
        stats_bundle = [self.final_score, self.correct_count,
                        self.wrong_count, rounds_played]

        Stats(self, stats_bundle)


class Stats:
    """
    Displays statistics for the Capital Cities Quiz game
    """

    def __init__(self, partner, all_stats_info):

        # Extract information from the stats bundle
        final_score   = all_stats_info[0]
        correct_count = all_stats_info[1]
        wrong_count   = all_stats_info[2]
        rounds_played = all_stats_info[3]

        self.stats_box = Toplevel()
        self.stats_box.title("Game Statistics")

        # Disable stats button while window is open
        partner.stats_button.config(state=DISABLED)

        # If user presses X at the top, close stats and re-enable button
        self.stats_box.protocol("WM_DELETE_WINDOW",
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200)
        self.stats_frame.grid()

        # Calculate accuracy
        if rounds_played > 0:
            accuracy = correct_count / rounds_played * 100
        else:
            accuracy = 0

        # Build stats strings
        final_score_string  = f"Final Score:       {final_score}"
        correct_string      = f"Correct Answers:   {correct_count}"
        wrong_string        = f"Wrong Answers:     {wrong_count}"
        accuracy_string     = f"Accuracy:          {accuracy:.0f}%"

        # Custom comment based on accuracy
        if accuracy == 100:
            comment_string = "Amazing! You got every single question correct!"
            comment_colour = "#D5E8D4"

        elif accuracy == 0:
            comment_string = ("Oops - you didn't get any correct! "
                              "Try using the 50/50 Hints next time!")
            comment_colour = "#F8CECC"

        else:
            comment_string = (f"Well done - {correct_count} correct out of "
                              f"{rounds_played} questions ({accuracy:.0f}%)!")
            comment_colour = "#FFF2CC"

        heading_font = ("Arial", 16, "bold")
        normal_font  = ("Arial", 14)
        comment_font = ("Arial", 13)

        # Label list (text | font | sticky)
        all_stats_strings = [
            ["Statistics",       heading_font, ""],
            [final_score_string,  normal_font, "W"],
            [correct_string,      normal_font, "W"],
            [wrong_string,        normal_font, "W"],
            [accuracy_string,     normal_font, "W"],
            [comment_string,     comment_font, "W"],
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            make_stats_label = Label(self.stats_frame, text=item[0],
                                     font=item[1], anchor="w",
                                     justify="left", padx=30, pady=5)
            make_stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(make_stats_label)

        # Configure the comment label background colour
        comment_label = stats_label_ref_list[5]
        comment_label.config(bg=comment_colour)

        self.dismiss_button = Button(self.stats_frame, font=("Arial", 16, "bold"),
                                     text="Dismiss", bg="#333333", fg="#FFFFFF",
                                     width=20,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=6, padx=10, pady=10)

    def close_stats(self, partner):
        """
        Closes stats dialogue box and re-enables stats button
        """
        # Put stats button back to normal
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Capital Cities Quiz")
    StartGame()
    root.mainloop()