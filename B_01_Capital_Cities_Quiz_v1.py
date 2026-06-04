import random
from tkinter import *
from functools import partial  # To prevent unwanted windows
from Quiz_Data import quiz_data


# Helper functions go here
def get_round_questions(how_many):
    """
    Randomly selects questions from the quiz data list.
    :param how_many: number of rounds the user wants to play
    :return: list of selected question entries
    """

    # Make sure we don't ask for more questions than we have available
    num_questions = min(how_many, len(quiz_data))

    # Randomly sample from quiz data without replacement
    selected = random.sample(quiz_data, num_questions)

    return selected


def get_question_options(question):
    """
    Builds a shuffled list of 4 answer options for the given question.
    Always includes the correct answer plus 3 randomly chosen wrong answers
    drawn from the full capitals pool so every game has different distractors.
    :param question: a single question entry from quiz_data
    :return: shuffled list of 4 answer strings
    """

    correct = question[1]

    # Build a pool of all capitals except the correct one
    all_capitals = [entry[1] for entry in quiz_data if entry[1] != correct]

    # Pick 3 random wrong answers from the pool
    wrong_answers = random.sample(all_capitals, 3)

    # Combine correct answer with wrong answers then shuffle
    options = [correct] + wrong_answers
    random.shuffle(options)

    return options


# Classes start here
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

        # Strings for labels
        intro_string = ("In each round you will be invited to complete a quiz game. "
                        "Your goal is to beat the game and guess the capital cities. "
                        "You have to complete the game and you decide the amount of "
                        "rounds/games you want to play.\n\n"
                        "Correct Answer: +10 points\n"
                        "Correct Answer using 50/50: +4 points\n"
                        "False Answer: -3 points\n"
                        "False Answer using 50/50: -5 points\n\n"
                        "(The 50/50 component gives more opportunity to answer the question correctly, "
                        "so wrong answers using them cost more!)")

        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Country Capital Quiz \U0001f30d", ("Arial", 16, "bold"), None],
            [intro_string, ("Arial", 12), None],
            [choose_string, ("Arial", 12, "bold"), "#009900"]
        ]

        # Create labels and add them to the reference list...
        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2],
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # Extract choice label so that it can be changed to an error message
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button...
        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve number of rounds wanted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        # Check that a whole number above zero has been entered
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Clear entry box and reset instruction label
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")

                # Invoke Play class and take across number of rounds
                Play(rounds_wanted)
                # Hide root window (ie: hide rounds choice window)
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # Display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", 10, "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for playing the Capital Cities Quiz
    """

    def __init__(self, how_many):

        # Integer / variable setup
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.user_score = IntVar()
        self.user_score.set(0)

        # Counters for stats
        self.correct_count = 0
        self.wrong_count = 0

        # Retrieve question list for this game
        self.question_list = get_round_questions(how_many)
        self.current_question = []
        self.current_options = []
        self.hint_used = False

        self.play_box = Toplevel()
        self.play_box.title("Country Capital Quiz")

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # Body font for most labels
        body_font = ("Arial", "12")

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), None, 0],
            ["Score: 0", body_font, "#FFF2CC", 1],
            ["Choose A Capital City Below... Good luck! \U0001f30d", body_font, "#D5E8D4", 2],
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

        self.answer_button_ref = []

        # Button colours for the four answer buttons
        button_colour_list = ["#FF69B4", "#1565C0", "#90EE90", "#CC6600"]

        # Create four answer buttons in a 2x2 grid
        for item in range(0, 4):
            make_answer_button = Button(self.answer_frame, font=("Arial", 12),
                                        text="Capital City", width=15, fg="#FFFFFF",
                                        bg=button_colour_list[item],
                                        command=partial(self.round_results, item))
            make_answer_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)
            self.answer_button_ref.append(make_answer_button)

        # Frame to hold hint and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=8)

        # Button details (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", self.new_round, 21, 7, None],
            [self.hints_stats_frame, "50/50", "#FF8000", self.to_hints, 16, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", self.to_stats, 16, 0, 1],
            [self.game_frame, "End Game \U0001f30d", "#990000", self.close_play, 21, 9, None]
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
        self.hints_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # Once interface is set up, start the first round
        self.new_round()

    def new_round(self):
        """
        Sets up the next question - updates heading, country label
        and answer buttons with new question data
        """

        # Retrieve and increment rounds played
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # Reset hint used flag for new round
        self.hint_used = False

        # Retrieve the current question from the list
        self.current_question = self.question_list[rounds_played - 1]
        self.current_options = get_question_options(self.current_question)

        # Update heading label
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")

        # Update country label with the question
        self.country_label.config(
            text=f"What is the capital of {self.current_question[0]}?")

        # Clear hint label and reset results label
        self.hint_label.config(text="")
        self.results_label.config(text="Choose your answer! \U0001f30d",
                                  bg="#D5E8D4")

        # Update answer buttons with shuffled options and re-enable them
        for count, item in enumerate(self.answer_button_ref):
            item.config(text=self.current_options[count], state=NORMAL)

        # Re-enable hint button, disable next button until answer is chosen
        self.hints_button.config(state=NORMAL, bg="#FF8000")
        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):
        """
        Checks the user's chosen answer against the correct answer,
        updates the score and results label accordingly
        """

        # Get the answer the user chose and the correct answer
        chosen_answer = self.current_options[user_choice]
        correct_answer = self.current_question[1]
        country_fact = self.current_question[3]

        # Retrieve current score
        current_score = self.user_score.get()

        if chosen_answer == correct_answer:
            # Correct answer - award points (fewer if hint was used)
            if self.hint_used:
                points = 4
                result_text = (f"True \u2705  +{points} points (50/50 used)\n\n"
                               f"\U0001f4a1 Did you know? {country_fact}")
            else:
                points = 10
                result_text = (f"True \u2705  +{points} points\n\n"
                               f"\U0001f4a1 Did you know? {country_fact}")

            result_bg = "#82B366"
            current_score += points

            # Track correct answers
            self.correct_count += 1

        else:
            # Wrong answer - deduct points (more if hint was used)
            if self.hint_used:
                points = 5
                result_text = (f"False \u274c  -{points} points (50/50 used)\n"
                               f"Correct: {correct_answer}")
            else:
                points = 3
                result_text = (f"False \u274c  -{points} points\n"
                               f"Correct: {correct_answer}")

            result_bg = "#F8CECC"
            current_score -= points

            # Track wrong answers
            self.wrong_count += 1

            # Highlight the correct answer button in green
            for count, item in enumerate(self.answer_button_ref):
                if self.current_options[count] == correct_answer:
                    item.config(bg="#228B22")

        # Update score and results label
        self.user_score.set(current_score)
        self.score_label.config(text=f"Score: {current_score}")
        self.results_label.config(text=result_text, bg=result_bg)

        # Disable all answer buttons and hint button
        for item in self.answer_button_ref:
            item.config(state=DISABLED)
        self.hints_button.config(state=DISABLED, bg="#AAAAAA")

        # Check if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")
        else:
            self.next_button.config(state=NORMAL)

        # Enable stats button once at least one answer has been given
        self.stats_button.config(state=NORMAL)

    def to_hints(self):
        """
        Activates 50/50 hint - removes two wrong answer buttons and
        informs the user they have a 50/50 chance of getting it right.
        Launches DisplayHints popup for detailed hint info if hints not yet used.
        """

        if self.hint_used:
            return

        # Update hint label to inform user about 50/50
        self.hint_label.config(text="50/50! Two wrong answers have been removed. "
                                    "You now have a 50/50 chance of getting it right. "
                                    "Good luck! \U0001f3af")

        # Find all wrong answer indices
        correct_answer = self.current_question[1]
        wrong_indices = []

        for count, option in enumerate(self.current_options):
            if option != correct_answer:
                wrong_indices.append(count)

        # Remove two wrong answers by disabling and greying them out
        remove_two = random.sample(wrong_indices, 2)
        for idx in remove_two:
            self.answer_button_ref[idx].config(state=DISABLED,
                                               bg="#888888", fg="#CCCCCC",
                                               text="\u2715")

        # Mark hint as used and disable hint button
        self.hint_used = True
        self.hints_button.config(state=DISABLED, bg="#AAAAAA")

    def to_stats(self):
        """
        Retrieves everything needed to display the game statistics
        """

        final_score = self.user_score.get()
        rounds_played = self.rounds_played.get()
        stats_bundle = [final_score, self.correct_count,
                        self.wrong_count, rounds_played]

        Stats(self, stats_bundle)

    def close_play(self):
        """
        Closes the play window and returns to the start screen
        """
        # Reshow start screen and close quiz window
        root.deiconify()
        self.play_box.destroy()


class Stats:
    """
    Displays statistics for the Capital Cities Quiz game
    """

    def __init__(self, partner, all_stats_info):

        # Extract information from the stats bundle
        final_score    = all_stats_info[0]
        correct_count  = all_stats_info[1]
        wrong_count    = all_stats_info[2]
        rounds_played  = all_stats_info[3]

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
        final_score_string   = f"Final Score:       {final_score}"
        correct_string       = f"Correct Answers:   {correct_count}"
        wrong_string         = f"Wrong Answers:     {wrong_count}"
        accuracy_string      = f"Accuracy:          {accuracy:.0f}%"

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
            ["Statistics",      heading_font, ""],
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
    root.title("Country Capital Quiz")
    StartGame()
    root.mainloop()