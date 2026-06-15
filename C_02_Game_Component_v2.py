import random
from tkinter import *
from functools import partial  # To prevent unwanted windows
from C_05_Get_All_Capital_Cities_v1 import quiz_data


def get_round_questions(how_many):
    """
    Randomly selects questions from the quiz data list.
    Returns a list of question dictionaries for the round.
    :param how_many: number of rounds the user wants to play
    :return: list of selected questions
    """

    # Make sure we don't ask for more questions than we have
    num_questions = min(how_many, len(quiz_data))

    # Randomly sample from the quiz data without replacement
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

    # Build the options list and shuffle so correct answer isn't always first
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

        # Integer / variable setup
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.user_score = IntVar()
        self.user_score.set(0)

        # Lists to track scores and results
        self.all_scores_list = []
        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        # Retrieve question list for this game
        self.question_list = get_round_questions(how_many)
        self.current_question = []
        self.current_options = []
        self.hint_used = False

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
            [self.hints_stats_frame, "50:50🍀", "#FF8000", self.use_hint, 16, 0, 0],
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
        self.country_label.config(text=f"What is the capital of {self.current_question[0]}?")

        # Clear hint label and results label
        self.hint_label.config(text="")
        self.results_label.config(text="Choose your answer! 🌍", bg="#D5E8D4")

        # Update answer buttons with shuffled options
        for count, item in enumerate(self.answer_button_ref):
            item.config(text=self.current_options[count], state=NORMAL)

        # Re-enable hint button, disable next button until answer chosen
        self.hint_button.config(state=NORMAL, bg="#FF8000")
        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):
        """
        Checks the user's answer against the correct answer,
        updates score and results label accordingly
        """

        # Get the answer the user chose
        chosen_answer = self.current_options[user_choice]
        correct_answer = self.current_question[1]
        country_fact = self.current_question[2]

        # Retrieve current score
        current_score = self.user_score.get()

        if chosen_answer == correct_answer:
            # Correct answer - award points (less if hint was used)
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

            # Track rounds won
            rounds_won = self.rounds_won.get()
            self.rounds_won.set(rounds_won + 1)

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

            # Highlight the correct answer button in green
            for count, item in enumerate(self.answer_button_ref):
                if self.current_options[count] == correct_answer:
                    item.config(bg="#228B22")

        # Update score and results label
        self.user_score.set(current_score)
        self.score_label.config(text=f"Score: {current_score}")
        self.results_label.config(text=result_text, bg=result_bg)

        # Add score to list for stats
        self.all_scores_list.append(current_score)

        # Disable all answer buttons and hint button
        for item in self.answer_button_ref:
            item.config(state=DISABLED)
        self.hint_button.config(state=DISABLED)

        # Check if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")
        else:
            self.next_button.config(state=NORMAL)

        # Enable stats button
        self.stats_button.config(state=NORMAL)

    def use_hint(self):
        """
        50/50 hint - removes two wrong answer buttons and tells the
        user they now have a 50/50 chance of getting it right
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
        self.hint_button.config(state=DISABLED, bg="#AAAAAA")

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