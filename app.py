"""
================================================================================
                    CODEALPHA PYTHON INTERNSHIP: TASK 1
                        UNLIMITED HANGMAN GAME ENGINE
================================================================================
Key Concepts Demonstrated:
  1. random     -> Picking topics, random word lengths, and choosing from word pools
  2. while loop -> Main guessing loop and game replay loop
  3. if-else    -> Checking guesses, input validation, and online/offline fallbacks
  4. strings    -> Word masking, case conversion (.upper()), slicing, and joins
  5. lists      -> Storing ASCII gallows art, candidate words, and guessed letters
================================================================================
Features:
  - UNLIMITED RANDOM WORDS: Fetches dynamic words & definitions in real-time
  - AUTOMATIC MIDDLE-LETTER CLUE: Pre-reveals the center letter to help you start
  - RELIABLE OFFLINE FALLBACK: Built-in backup words so it never crashes
  - WEB UI + TERMINAL CLI: Play in your browser or directly in the terminal
================================================================================
"""

import json
import os
import random
import re
import sys
import urllib.request
from flask import Flask, jsonify, render_template, send_from_directory


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

MAX_LIVES = 6

# Set to keep track of words already used in the current session (no repeats!)
used_words = set()

# Diverse topics used to fetch fresh, unlimited random words
TOPICS = [
    "technology", "computer", "science", "nature", "animal",
    "space", "planet", "ocean", "music", "travel", "sports",
    "robot", "weather", "history", "art", "language"
]

# Reliable offline backup pool in case the internet connection is unavailable
OFFLINE_BACKUP_WORDS = {
    "PYTHON": "A popular high-level programming language known for clean syntax",
    "DEVELOPER": "A person who designs, builds, and maintains software applications",
    "VARIABLE": "A named container in memory used to store data values",
    "FUNCTION": "A reusable block of code that executes a specific task",
    "ALGORITHM": "A step-by-step procedure or set of rules to solve a problem",
    "DATABASE": "An organized collection of structured information or data",
    "FRONTEND": "The client-facing visual part of an application users interact with",
    "BACKEND": "The server side of an application managing data, logic, and APIs",
    "DEBUGGING": "The process of detecting, diagnosing, and fixing errors in code",
    "KEYBOARD": "An input device with keys used to type code and commands",
    "TERMINAL": "A text-based command-line interface for running system commands",
    "COMPILER": "A program that translates source code into machine code",
    "INTERNET": "A global network connecting computers worldwide",
    "SOFTWARE": "Programs and operating information used by a computer system",
    "HARDWARE": "The physical components and circuits of a computer",
    "BROWSER": "An application used to navigate and view websites on the World Wide Web",
    "SECURITY": "The practice of defending digital systems and data from attacks",
    "LOOPING": "Repeating a block of instructions until a specific condition is met"
}


# ------------------------------------------------------------------------------
# Concept 1, 3 & 4: RANDOM, STRINGS & IF-ELSE
# Dynamic Unlimited Random Word Fetcher with Definition Clues
# ------------------------------------------------------------------------------
def sanitize_hint(word, hint):
    """
    Cleans dictionary formatting and masks the target word if it appears
    inside the definition text so it doesn't spoil the answer.
    """
    # Remove dictionary part-of-speech prefix (e.g. 'n\t', 'adj\t')
    if "\t" in hint:
        hint = hint.split("\t", 1)[-1].strip()

    # Mask the secret word if it appears in the definition
    clean_word = re.escape(word)
    hint = re.sub(clean_word, "[the word]", hint, flags=re.IGNORECASE)
    return hint


def get_random_word():
    """
    Fetches an unlimited random word with its dictionary definition.
    - Online: Queries the open Datamuse dictionary API across random topics.
    - Offline fallback: Seamlessly picks from backup words if offline.
    - Automatically extracts the middle letter as a helpful starter clue.
    """
    global used_words

    # Attempt dynamic online fetch for unlimited random words
    try:
        topic = random.choice(TOPICS)
        # Random word length between 5 and 8 characters
        pattern = "?" * random.randint(5, 8)
        url = f"https://api.datamuse.com/words?topics={topic}&sp={pattern}&md=d&max=50"
        
        req = urllib.request.Request(url, headers={"User-Agent": "HangmanGame/1.0"})
        with urllib.request.urlopen(req, timeout=3.5) as response:
            data = json.loads(response.read().decode("utf-8"))

            candidates = []
            for item in data:
                w = item.get("word", "")
                defs = item.get("defs", [])
                # Filter for valid English alphabetic words with definitions
                if 4 <= len(w) <= 9 and w.isalpha() and defs:
                    upper_w = w.upper()
                    if upper_w not in used_words:
                        raw_hint = defs[0]
                        clean_hint = sanitize_hint(upper_w, raw_hint)
                        candidates.append((upper_w, clean_hint))

            if candidates:
                word, hint = random.choice(candidates)
                used_words.add(word)
                middle_index = len(word) // 2
                middle_letter = word[middle_index]
                return {
                    "word": word,
                    "hint": hint,
                    "middle_letter": middle_letter,
                    "length": len(word),
                    "source": "online"
                }
    except Exception:
        # If offline or request fails, seamlessly continue to fallback
        pass

    # Fallback to local offline dictionary if needed
    unused = [w for w in OFFLINE_BACKUP_WORDS if w not in used_words]
    if not unused:
        used_words.clear()
        unused = list(OFFLINE_BACKUP_WORDS.keys())

    word = random.choice(unused)
    used_words.add(word)
    hint = OFFLINE_BACKUP_WORDS[word]
    middle_index = len(word) // 2
    middle_letter = word[middle_index]

    return {
        "word": word,
        "hint": hint,
        "middle_letter": middle_letter,
        "length": len(word),
        "source": "offline_backup"
    }


# ------------------------------------------------------------------------------
# Concept 4 & 5: STRINGS & LISTS
# Formatting the secret word with revealed letters and underscores
# ------------------------------------------------------------------------------
def format_display_word(target_word, guessed_letters):
    """
    Returns a formatted spaced string (e.g. 'P Y T H _ N')
    showing revealed letters and underscores for hidden letters.
    """
    display_letters = []
    for char in target_word:
        # Concept 3: IF-ELSE
        if char in guessed_letters:
            display_letters.append(char)
        else:
            display_letters.append("_")
    
    # Strings: join list into space-separated string
    return " ".join(display_letters)


# ------------------------------------------------------------------------------
# Concept 2 & 3: WHILE LOOPS & IF-ELSE
# Interactive terminal gameplay function
# ------------------------------------------------------------------------------
def play_terminal_game():
    """
    Runs the command-line interface (CLI) edition of Hangman.
    Demonstrates while loops, if-else logic, lists, and strings.
    """
    print("\n" + "=" * 65)
    print("   CODEALPHA PYTHON INTERNSHIP: TASK 1 - HANGMAN (UNLIMITED WORDS)")
    print("=" * 65)

    score_wins = 0
    score_losses = 0

    # WHILE LOOP 1: Replay loop across multiple rounds
    while True:
        data = get_random_word()
        target_word = data["word"]
        hint = data["hint"]
        middle_letter = data["middle_letter"]

        # Lists: track all guessed letters
        guessed_letters = [middle_letter]
        incorrect_guesses = 0

        print(f"\n[💡] Clue/Definition : {hint}")
        print(f"[💡] Starter Clue    : Middle letter '{middle_letter}' has been revealed!")

        # WHILE LOOP 2: Turn-by-turn game loop
        while incorrect_guesses < MAX_LIVES:
            print(HANGMAN_PICS[incorrect_guesses])
            print(f" Lives remaining : {MAX_LIVES - incorrect_guesses} / {MAX_LIVES}")
            print(f" Secret Word     : {format_display_word(target_word, guessed_letters)}")
            print(f" Guessed Letters : {', '.join(sorted(guessed_letters))}")

            # Check if all letters have been revealed
            word_solved = True
            for char in target_word:
                if char not in guessed_letters:
                    word_solved = False
                    break

            # IF-ELSE: check win condition
            if word_solved:
                print(f"\n🎉 Congratulations! You guessed the word: {target_word}!")
                score_wins += 1
                break

            # STRINGS: take input, strip whitespace, and convert to uppercase
            guess = input("\n>> Enter a letter (or guess the whole word): ").strip().upper()

            # Input validation with if-else
            if not guess.isalpha():
                print("Please enter letters only!")
                continue

            if len(guess) > 1:
                # Full word guess
                if guess == target_word:
                    print(f"\n🎉 Amazing! You guessed the entire word: {target_word}!")
                    score_wins += 1
                    break
                else:
                    print(f"'{guess}' is incorrect!")
                    incorrect_guesses += 1
                    continue

            # Single letter guess
            if guess in guessed_letters:
                print(f"You already guessed '{guess}'! Try another letter.")
                continue

            # Add guess to list
            guessed_letters.append(guess)

            # IF-ELSE: check if letter is in the target word
            if guess in target_word:
                print(f"Correct! '{guess}' is in the word.")
            else:
                print(f"Wrong! '{guess}' is not in the word.")
                incorrect_guesses += 1

        else:
            # Executes if while loop finishes because lives reached 0
            print(HANGMAN_PICS[6])
            print(f"\n💀 Game Over! The stickman was hung.")
            print(f"The secret word was: {target_word}")
            score_losses += 1

        print(f"\nScoreboard -> Wins: {score_wins} | Losses: {score_losses}")

        # Replay prompt
        replay = input("\nPlay another random word? (y/n): ").strip().lower()
        if replay not in ("y", "yes"):
            print("Thanks for playing CodeAlpha Hangman!\n")
            break


# ------------------------------------------------------------------------------
# FLASK WEB APPLICATION (Serves Web UI & Simple API for Vercel)
# ------------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(BASE_DIR, "templates")
static_dir = os.path.join(BASE_DIR, "static")

app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)


# WSGI Middleware to restore original request paths behind Vercel serverless rewrites
class VercelPathFix:
    def __init__(self, wsgi):
        self.wsgi = wsgi

    def __call__(self, env, start_response):
        matched = (
            env.get("HTTP_X_MATCHED_PATH")
            or env.get("HTTP_X_FORWARDED_URI")
            or env.get("HTTP_X_INVOKE_PATH")
        )
        if matched:
            env["PATH_INFO"] = matched.split("?")[0]
        return self.wsgi(env, start_response)


app.wsgi_app = VercelPathFix(app.wsgi_app)


def get_html_content():
    """Locates and reads index.html safely across local, Docker, and Vercel environments."""
    candidate_paths = [
        os.path.join(BASE_DIR, "templates", "index.html"),
        os.path.join(BASE_DIR, "index.html"),
        os.path.join(BASE_DIR, "public", "index.html"),
        os.path.join(os.path.dirname(BASE_DIR), "templates", "index.html"),
        os.path.join(os.path.dirname(BASE_DIR), "index.html"),
        os.path.join(os.path.dirname(BASE_DIR), "public", "index.html"),
    ]
    for path in candidate_paths:
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass
    try:
        return render_template("index.html")
    except Exception:
        return "<h1>Hangman Game</h1><p>Please refresh...</p>"


@app.route("/")
@app.route("/index")
@app.route("/index.html")
@app.route("/api/index")
@app.route("/api/index.py")
@app.route("/api")
def home():
    """Serves the interactive web page across all path variants."""
    return get_html_content(), 200, {"Content-Type": "text/html; charset=utf-8"}


@app.route("/api/word")
@app.route("/word")
def api_word():
    """
    Returns an unlimited fresh random word, its definition hint,
    and middle starter letter in JSON format.
    """
    return jsonify(get_random_word())


@app.route("/style.css")
@app.route("/static/style.css")
def serve_css():
    """Serves CSS styling sheet with correct Content-Type."""
    for path in [
        os.path.join(static_dir, "style.css"),
        os.path.join(BASE_DIR, "static", "style.css"),
        os.path.join(BASE_DIR, "style.css"),
        os.path.join(os.path.dirname(BASE_DIR), "static", "style.css"),
    ]:
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read(), 200, {"Content-Type": "text/css; charset=utf-8"}
            except Exception:
                pass
    return send_from_directory(static_dir, "style.css", mimetype="text/css")


@app.route("/static/<path:filename>")
def static_files(filename):
    """Serves static files."""
    return send_from_directory(static_dir, filename)


@app.errorhandler(404)
def handle_404(e):
    """Fallback handler to prevent 404 error page on Vercel."""
    from flask import request
    if request.path.endswith("/word") or request.path.endswith("api/word"):
        return jsonify(get_random_word())
    return get_html_content(), 200, {"Content-Type": "text/html; charset=utf-8"}


# ------------------------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--cli", "-c", "cli"):
        play_terminal_game()
    else:
        print("\n" + "=" * 65)
        print("  🎮 CodeAlpha Hangman Web Server (Unlimited Words)")
        print("  📍 Open in your browser : http://127.0.0.1:5002")
        print("  🕹️  Terminal CLI Mode    : python app.py --cli")
        print("=" * 65 + "\n")
        app.run(debug=True, port=5002)
