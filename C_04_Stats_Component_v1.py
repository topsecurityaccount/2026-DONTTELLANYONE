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
        self.rounds_won = IntVar()

        # Test data for Stats component (comment/uncomment to test different scenarios)

        # All correct test data...
        # self.all_scores_list = [10, 10, 10, 10, 10]
        # self.rounds_won.set(5)

        # All wrong test data...
        # self.all_scores_list = [-3, -3, -3, -3, -3]
        # self.rounds_won.set(0)

        # Mixed score test data...
        self.all_scores_list = [10, -3, 4, -5, 10]
        self.rounds_won.set(3)

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

        # Retrieve rounds won as a number (not the IntVar container)
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_scores_list]

        Stats(self, stats_bundle)


class Stats:
    """
    Displays statistics for the Capital Cities Quiz game
    """

    def __init__(self, partner, all_stats_info):

        # Extract information from the stats bundle
        rounds_won = all_stats_info[0]
        user_scores = all_stats_info[1]

        self.stats_box = Toplevel()
        self.stats_box.title("Game Statistics")

        # Disable stats button while window is open
        partner.stats_button.config(state=DISABLED)

        # If user presses X at the top, close stats and re-enable button
        self.stats_box.protocol("WM_DELETE_WINDOW",
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200)
        self.stats_frame.grid()

        # Maths to calculate stats figures
        rounds_played = len(user_scores)
        total_score = sum(user_scores)
        best_score = max(user_scores)
        average_score = total_score / rounds_played

        if rounds_played > 0:
            success_rate = rounds_won / rounds_played * 100
        else:
            success_rate = 0

        # Build stats strings
        success_string = (f"Success Rate: {rounds_won} / {rounds_played} "
                          f"({success_rate:.0f}%)")
        total_score_string = f"Total Score: {total_score}"
        best_score_string = f"Best Round Score: {best_score}"
        average_score_string = f"Average Score Per Round: {average_score:.0f}"

        # Custom comment based on performance
        if rounds_won == rounds_played:
            comment_string = "Amazing! You got every single round correct!"
            comment_colour = "#D5E8D4"

        elif rounds_won == 0:
            comment_string = ("Oops - you didn't win any rounds! "
                              "Try using the Hints next time!")
            comment_colour = "#F8CECC"
            best_score_string = "Best Round Score: n/a"

        else:
            comment_string = f"Well done - you won {rounds_won} out of {rounds_played} rounds!"
            comment_colour = "#FFF2CC"

        # Label list (text | font | sticky)
        all_stats_strings = [
            ["Statistics", ("Arial", 16, "bold"), ""],
            [success_string, ("Arial", 14), "W"],
            [total_score_string, ("Arial", 14), "W"],
            [best_score_string, ("Arial", 14), "W"],
            [average_score_string, ("Arial", 14), "W"],
            [comment_string, ("Arial", 13), "W"],
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
