# 🎯 CodeAlpha Internship Project: Task 1 - Hangman Game

A modern, clean, and intuitive text-based **Hangman Game** built with pure Python. Developed as part of the **CodeAlpha Python Programming Internship**.

---

## 📌 Project Overview & Task Scope

- **Goal:** Create a text-based Hangman game where the player guesses a secret word one letter at a time.
- **Predefined Word Bank:** Uses a clean list of 5 curated programming-themed words with clues.
- **Lives / Mistake Limit:** Strictly capped at **6 incorrect guesses** corresponding to the standard 6 anatomical parts of the stickman (Head, Torso, Left Arm, Right Arm, Left Leg, Right Leg).
- **Environment:** Pure console input/output with cross-platform ANSI styling (compatible with Windows CMD, PowerShell, macOS Terminal, and Linux).
- **Zero External Dependencies:** Built entirely with standard Python libraries.

---

## 🚀 Key Python Concepts Demonstrated

| Concept | Implementation in Code |
| :--- | :--- |
| **`random` Module** | Used `random.randint()` to randomly pick a secret word and its hint from the word bank. |
| **`while` Loops** | Powers the main gameplay loop (`while incorrect_guesses < 6`), the replay loop, and robust input validation loops. |
| **`if-else` Logic** | Evaluates whether guessed letters exist in the secret word, tracks lives, and determines win/loss outcomes. |
| **`strings`** | String sanitization (`.strip()`, `.upper()`), membership testing (`char in target_word`), character counting, and formatting. |
| **`lists`** | Stores predefined words (`WORDS`), corresponding clues (`HINTS`), ASCII gallows art (`HANGMAN_PICS`), and tracks guessed letters (`guessed_letters`). |

---

## 🎨 Design & User Experience Features

1. **Aesthetic ASCII Art Gallows:**
   - 7 visual stages rendering gallows and stickman progress from 0 to 6 mistakes.
2. **Dynamic Dashboard:**
   - **Visual Life Counter:** Visual hearts/pips (`♥♥♥♥··`) with exact remaining count `(4/6)`.
   - **Clue / Category System:** Each word includes an intuitive hint to keep the game engaging.
   - **Letter Progress Display:** Spaced underscores with correctly guessed letters highlighted in color.
   - **Guessed Letters History:** Sorted list of all tried letters to prevent redundant guessing.
3. **Friendly Input Validation:**
   - Automatically ignores empty inputs and non-alphabetic characters.
   - Alerts players if a letter was already guessed **without penalizing their remaining lives**.
   - Supports guessing the **full word** directly for confident players!
4. **Session Scoreboard & Replay System:**
   - Tracks games played, wins, losses, and win rate percentage across multiple rounds.
   - Graceful exit with `Ctrl+C` or typing `n` at the replay prompt.

---

## 📂 Project Structure

```
D:\DAV PROJECT\codealpha intership project\
├── Hangman Game\
│   ├── hangman.py          # Classic CLI console game (ANSI colored)
│   ├── app.py              # Flask server for Web UI edition
│   ├── index.html          # Standalone Web edition (double-clickable)
│   ├── static/
│   │   └── style.css       # Modern dark-mode glassmorphic styling
│   ├── templates/
│   │   └── index.html      # Jinja2 Flask web template
│   └── README.md           # Documentation and walkthrough
├── Advanced Chatbot\       # Previous project
└── Stock Portfolio Tracker\ # Previous project
```

---

## 🎮 How to Run

### Option 1: Classic Console Terminal (CLI)
1. Open PowerShell or Command Prompt in the project folder:
   ```powershell
   python hangman.py
   ```

### Option 2: Modern Web Interface (Standalone Browser)
- Simply double-click `index.html` in File Explorer or open with your favorite browser.

### Option 3: Flask Local Web Server
1. Launch the local Flask server:
   ```powershell
   python app.py
   ```
2. Open your browser at `http://127.0.0.1:5002`.

---

## 🕹️ Gameplay Preview

```
=================================================================
       [#] CODEALPHA PYTHON INTERNSHIP: TASK 1 - HANGMAN [#]       
=================================================================

        +---+
        |   |
        O   |
       /|   |
            |
            |
      =========
    
 Lives:        ♥ ♥ ♥ · · · (3/6 lives remaining)
 Hint / Clue:  A versatile high-level programming language
 ---------------------------------------------------------------

 Secret Word:  P  Y  T  H  _  N

 Guessed:      [ H, P, T, Y, Z, X, M ]
 ---------------------------------------------------------------
 [+] Correct! 'H' is in the word (1 time).

 >> Enter a letter (A-Z) or guess the full word:
```

---

## 📜 Word Bank & Hint Features

- **Non-Repeating Shuffled Deck:** Words are served in a randomized queue that exhausts all 18 tech words before reshuffling. Words will **never repeat consecutively**!
- **Middle-Letter Starter Clue:** At the start of every game, the letter in the **middle** of the secret word is automatically revealed (e.g. `L` in `DEVELOPER` or `A` in `VARIABLE`) to give you an immediate foothold.
- **In-Game Hint Support:**
  - **Terminal (CLI):** Type `hint` anytime to reveal an extra letter.
  - **Web UI:** Click the **"💡 Reveal Letter"** button to uncover another letter.

### Curated Tech Words:
1. `PYTHON` &bull; 2. `DEVELOPER` &bull; 3. `VARIABLE` &bull; 4. `FUNCTION` &bull; 5. `ALGORITHM` &bull; 6. `DATABASE`
7. `FRONTEND` &bull; 8. `BACKEND` &bull; 9. `DEBUGGING` &bull; 10. `KEYBOARD` &bull; 11. `TERMINAL` &bull; 12. `COMPILER`
13. `INTERNET` &bull; 14. `SOFTWARE` &bull; 15. `HARDWARE` &bull; 16. `BROWSER` &bull; 17. `SECURITY` &bull; 18. `LOOPING`

---
*Created for CodeAlpha Internship - Task 1 (Hangman Game)*
