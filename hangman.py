"""
================================================================================
                   CODEALPHA INTERNSHIP PROJECT - TASK 1
                                HANGMAN GAME
================================================================================
"""

import os
import random
import sys

# Ensure UTF-8 output encoding across Windows / Linux / macOS terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Initialize ANSI color sequences on Windows
if os.name == "nt":
    os.system("")

COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_CYAN = "\033[96m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_MAGENTA = "\033[95m"

HANGMAN_PICS = [
    r"""
        +---+
        |   |
            |
            |
            |
            |
      =========
    """,
    r"""
        +---+
        |   |
        O   |
            |
            |
            |
      =========
    """,
    r"""
        +---+
        |   |
        O   |
        |   |
            |
            |
      =========
    """,
    r"""
        +---+
        |   |
        O   |
       /|   |
            |
            |
      =========
    """,
    r"""
        +---+
        |   |
        O   |
       /|\  |
            |
            |
      =========
    """,
    r"""
        +---+
        |   |
        O   |
       /|\  |
       /    |
            |
      =========
    """,
    r"""
        +---+
        |   |
        O   |
       /|\  |
       / \  |
            |
      =========
    """
]

WORD_BANK = [
    ("PYTHON", "A popular high-level programming language known for clean syntax"),
    ("DEVELOPER", "A person who designs, builds, and maintains software applications"),
    ("VARIABLE", "A named container in memory used to store data values"),
    ("FUNCTION", "A reusable block of code that executes a specific task"),
    ("ALGORITHM", "A step-by-step procedure or set of rules to solve a problem"),
    ("DATABASE", "An organized collection of structured information or data"),
    ("FRONTEND", "The client-facing visual part of an application users interact with"),
    ("BACKEND", "The server side of an application managing data, logic, and APIs"),
    ("DEBUGGING", "The process of detecting, diagnosing, and fixing errors in code"),
    ("KEYBOARD", "An input device with keys used to type code and commands"),
    ("TERMINAL", "A text-based command-line interface for running system commands"),
    ("COMPILER", "A program that translates source code into machine code"),
    ("INTERNET", "A global network connecting computers worldwide"),
    ("SOFTWARE", "Programs and operating information used by a computer system"),
    ("HARDWARE", "The physical components and circuits of a computer"),
    ("BROWSER", "An application used to navigate and view websites on the World Wide Web"),
    ("SECURITY", "The practice of defending digital systems and data from attacks"),
    ("LOOPING", "Repeating a block of instructions until a specific condition is met")
]

MAX_INCORRECT_GUESSES = 6
available_word_indices = []


def get_next_word_entry():
    global available_word_indices
    if not available_word_indices:
        available_word_indices = list(range(len(WORD_BANK)))
        random.shuffle(available_word_indices)
    idx = available_word_indices.pop()
    return WORD_BANK[idx]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print(f"{COLOR_CYAN}{COLOR_BOLD}" + "=" * 65 + f"{COLOR_RESET}")
    print(f"{COLOR_YELLOW}{COLOR_BOLD}       [#] CODEALPHA PYTHON INTERNSHIP: TASK 1 - HANGMAN [#]       {COLOR_RESET}")
    print(f"{COLOR_CYAN}{COLOR_BOLD}" + "=" * 65 + f"{COLOR_RESET}")


def format_word_display(target_word, guessed_letters):
    letters_display = []
    for char in target_word:
        if char in guessed_letters:
            letters_display.append(f"{COLOR_GREEN}{COLOR_BOLD}{char}{COLOR_RESET}")
        else:
            letters_display.append(f"{COLOR_YELLOW}_{COLOR_RESET}")
    return "  ".join(letters_display)


def format_lives_display(incorrect_count):
    lives_left = MAX_INCORRECT_GUESSES - incorrect_count
    hearts = ("♥ " * lives_left) + ("· " * incorrect_count)
    return f"{COLOR_RED}{hearts}{COLOR_RESET}({lives_left}/{MAX_INCORRECT_GUESSES} lives remaining)"


def display_game_status(target_word, guessed_letters, incorrect_count, hint, starter_letter, message=""):
    clear_screen()
    print_header()
    print(f"{COLOR_RED}{HANGMAN_PICS[incorrect_count]}{COLOR_RESET}")
    print(f" {COLOR_BOLD}Lives:{COLOR_RESET}        {format_lives_display(incorrect_count)}")
    print(f" {COLOR_BOLD}Hint / Clue:{COLOR_RESET}  {COLOR_CYAN}{hint}{COLOR_RESET}")
    print(f" {COLOR_BOLD}Middle Clue:{COLOR_RESET}  {COLOR_YELLOW}'{starter_letter}' was pre-revealed in the middle to help you!{COLOR_RESET}")
    print(" " + "-" * 63)
    masked_word = format_word_display(target_word, guessed_letters)
    print(f"\n {COLOR_BOLD}Secret Word:{COLOR_RESET}  {masked_word}\n")
    if guessed_letters:
        guessed_str = ", ".join(sorted(guessed_letters))
        print(f" {COLOR_BOLD}Guessed:{COLOR_RESET}      [ {COLOR_MAGENTA}{guessed_str}{COLOR_RESET} ]")
    print(" " + "-" * 63)
    if message:
        print(f" {message}\n")


def get_player_guess(already_guessed, target_word):
    while True:
        try:
            prompt = f" {COLOR_BOLD}>> Enter a letter (A-Z), guess the full word, or type 'hint':{COLOR_RESET} "
            user_input = input(prompt).strip().upper()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{COLOR_YELLOW}[!] Game session interrupted. Goodbye!{COLOR_RESET}")
            sys.exit(0)

        if not user_input:
            print(f" {COLOR_YELLOW}[!] Input cannot be blank. Please enter a letter.{COLOR_RESET}")
            continue

        if user_input == "HINT":
            return "HINT"

        if not user_input.isalpha():
            print(f" {COLOR_YELLOW}[!] Invalid character! Please use letters only (A-Z).{COLOR_RESET}")
            continue

        if len(user_input) == 1:
            if user_input in already_guessed:
                print(f" {COLOR_YELLOW}[*] You have already guessed '{user_input}'. Pick another letter!{COLOR_RESET}")
                continue
            return user_input
        else:
            return user_input


def play_round():
    target_word, hint = get_next_word_entry()
    incorrect_guesses = 0
    guessed_letters = set()

    middle_index = len(target_word) // 2
    starter_letter = target_word[middle_index]
    guessed_letters.add(starter_letter)

    feedback_message = f"{COLOR_GREEN}[💡] Starter Clue: Middle letter '{starter_letter}' has been revealed!{COLOR_RESET}"

    while incorrect_guesses < MAX_INCORRECT_GUESSES:
        is_solved = all(char in guessed_letters for char in target_word)
        if is_solved:
            display_game_status(target_word, guessed_letters, incorrect_guesses, hint, starter_letter, feedback_message)
            print(f" {COLOR_GREEN}{COLOR_BOLD}🎉 CONGRATULATIONS! You solved the word '{target_word}'! 🎉{COLOR_RESET}\n")
            return True

        display_game_status(target_word, guessed_letters, incorrect_guesses, hint, starter_letter, feedback_message)
        guess = get_player_guess(guessed_letters, target_word)

        if guess == "HINT":
            unrevealed = [c for c in target_word if c not in guessed_letters]
            if unrevealed:
                extra_hint = random.choice(unrevealed)
                guessed_letters.add(extra_hint)
                feedback_message = f"{COLOR_CYAN}[💡] Free Hint: Letter '{extra_hint}' has been revealed!{COLOR_RESET}"
            else:
                feedback_message = f"{COLOR_YELLOW}[i] All letters are already revealed!{COLOR_RESET}"
            continue

        if len(guess) > 1:
            if guess == target_word:
                for c in target_word:
                    guessed_letters.add(c)
                display_game_status(target_word, guessed_letters, incorrect_guesses, hint, starter_letter)
                print(f" {COLOR_GREEN}{COLOR_BOLD}🌟 INCREDIBLE! You guessed the entire word '{target_word}' correctly! 🌟{COLOR_RESET}\n")
                return True
            else:
                incorrect_guesses += 1
                lives_left = MAX_INCORRECT_GUESSES - incorrect_guesses
                feedback_message = f"{COLOR_RED}[-] '{guess}' is incorrect! You lost 1 life. ({lives_left}/{MAX_INCORRECT_GUESSES} remaining){COLOR_RESET}"
                continue

        guessed_letters.add(guess)
        if guess in target_word:
            occurrences = target_word.count(guess)
            plural = "s" if occurrences > 1 else ""
            feedback_message = f"{COLOR_GREEN}[+] Correct! '{guess}' is in the word ({occurrences} time{plural}).{COLOR_RESET}"
        else:
            incorrect_guesses += 1
            lives_left = MAX_INCORRECT_GUESSES - incorrect_guesses
            feedback_message = f"{COLOR_RED}[-] '{guess}' is not in the word! ({lives_left}/{MAX_INCORRECT_GUESSES} remaining){COLOR_RESET}"

    display_game_status(target_word, guessed_letters, incorrect_guesses, hint, starter_letter)
    print(f" {COLOR_RED}{COLOR_BOLD}💀 GAME OVER! The stickman was hung.{COLOR_RESET}")
    print(f" {COLOR_YELLOW}The secret word was: {COLOR_BOLD}{target_word}{COLOR_RESET}\n")
    return False


def main():
    total_played = 0
    wins = 0
    losses = 0

    while True:
        has_won = play_round()
        total_played += 1
        if has_won:
            wins += 1
        else:
            losses += 1

        win_percentage = (wins / total_played) * 100 if total_played > 0 else 0.0

        print(f" {COLOR_CYAN}{COLOR_BOLD}[#] SESSION SCOREBOARD:{COLOR_RESET}")
        print(f"     Total Games : {total_played}")
        print(f"     Wins        : {COLOR_GREEN}{wins}{COLOR_RESET}")
        print(f"     Losses      : {COLOR_RED}{losses}{COLOR_RESET}")
        print(f"     Win Rate    : {COLOR_YELLOW}{win_percentage:.1f}%{COLOR_RESET}\n")

        while True:
            try:
                choice = input(f" {COLOR_BOLD}>> Play another word? (y/n): {COLOR_RESET}").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print(f"\n{COLOR_YELLOW}[!] Exiting. Thanks for playing!{COLOR_RESET}")
                return

            if choice in ("y", "yes"):
                break
            elif choice in ("n", "no"):
                print(f"\n{COLOR_GREEN}[*] Thanks for playing CodeAlpha Hangman! Great job!{COLOR_RESET}\n")
                return
            else:
                print(f" {COLOR_YELLOW}[!] Please type 'y' for yes or 'n' for no.{COLOR_RESET}")


if __name__ == "__main__":
    main()