"""
- Also IMPORTANT NOTE: As far as I am aware this workspace has gspread installed.
- I have double, triple check this project before sending it in 
to make sure no errors come up with this code.
- If the error has come up with gspread type pip install gspread into the 
below terminal. I am sotty about this but I have tried to fix the problem.
"""
# imports
import random
import gspread
from words import word_list

# This code is for linking the google spread
sa = gspread.service_account(filename="keys.json")
sh = sa.open("pp3_hangman")
wks = sh.worksheet("user")


def next_available_row(worksheet: str) -> str:
    """
    This function will return the number of the next empty row.
    @param worksheet(str): This will get the length of the row
    and then add 1 to add new value to the row.
    """
    str_list = list(filter(None, worksheet.col_values(1)))
    return len(str_list)+1


def get_word():
    """
    Get word function.
    This will generate random words from my words.py list.
    It will also return the users input with an uppercase.
    """
    word = random.choice(word_list)
    return word.upper()


def play(word: str) -> str:
    """
    Play function.
    This is the main function that will run the game.
    This is also the introduction to the game for the user.
    @param word(str): This will generate a word from the
    word list.
    """
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    # This is the introduction for the user.
    print("Are you ready to play Hangman, the Irish county edition?")
    print(display_hangman(tries))
    print(word_completion)
    print(" \n")
    while not guessed and tries > 0:
        # This is the input for the users guesses.
        guess = input("Please guess a letter: \n").upper()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed that letter", guess)
            elif guess not in word:
                # This will let the user know if the guess they have guessed
                # is incorrect.
                print(guess, "is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                # This will let the user know if the guess they have guessed
                # is correct.
                print("Great guess,", guess, "is in the word!")
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter ==
                           guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guess this word", guess)
                # This will let the user know that they have already guessed
                # word and need to replay the game.
            elif guess != word:
                print(guess, "is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            print("Sorry the guess you entered is not valid")
            # This will come up if the guess is invalid as in a number.
        print(display_hangman(tries))
        print(word_completion)
        print("\n")
    if guessed:
        print("Congratulations, you guessed the CORRECT word. You WON!")
    else:
        print("Sorry, you have run out of tries the word was " + word + "."
              "Why not try again!")


def display_hangman(tries: int) -> int:
    """
    This function will display the main hangman game.
    As the user plays each stage will appear depending on the guess.
    @param tries(int): This will calculate the tries left and display
    the appropriate stage below.
    """
    stages = [  # This is the hangman visual. Final state = full body.
                """
      +------------+
      |            |
      |            O
      |           /|\\
      |           / \\
      |
      |
      +--------+
   """,
                # This is the second last state with just the arm missing.
                """
      +------------+
      |            |
      |            O
      |            |\\
      |           / \\
      |
      |
      +--------+
   """,
                # This state has everything but both arms.
                """
      +------------+
      |            |
      |            O
      |            |
      |           / \\
      |
      |
      +--------+
                """,
                # This state has everything but both arms and a leg.
                 """
      +------------+
      |            |
      |            O
      |            |
      |           /
      |
      |
      +--------+
                """,
                # This state has only the head and body.
                 """
      +------------+
      |            |
      |            O
      |            |
      |
      |
      |
      +--------+
                """,
                # This state has only the head.
                """
      +------------+
      |            |
      |            O
      |
      |
      |
      |
      +--------+
                """,
                # This state has only the noose.
                """
      +------------+
      |            |
      |
      |
      |
      |
      |
      +--------+
                """,
    ]
    return stages[tries]


def main():
    """
    This will prin the logo for the game.
    This appears in the main introduction before the game starts.
    """
    print("""
{}    {}    {}{}     {}    {}    {}}}}}    {}      {}    {}{}     {}    {}
{}    {}   {}  {}    {}}}  {}   {}    {}   {}}}  {{{}   {}  {}    {}}}  {}
{}{{}}{}  {}{{}}{}   {} {} {}   {}         {} {{}} {}  {}{{}}{}   {} {} {}
{}    {}  {}    {}   {}  {{{}   {}  {{{{   {}  {}  {}  {}    {}   {}  {{{}
{}    {}  {}    {}   {}    {}    {}}}}}    {}      {}  {}    {}   {}    {}
        """)
    name = input("Enter your name: \n")
    row = next_available_row(wks)
    wks.update_cell(row, 1, name)
    print("Welcome", name, "!")

    word = get_word()
    play(word)
    # This function runs the game or allows the user to replay.
    wks.update_cell(row, 2, "NO")
    while input("Play Again? (YES / NO) \n").upper() == "YES":
        wks.update_cell(row, 2, "YES")
        word = get_word()
        play(word)


if __name__ == "__main__":
    main()
