# 🎯 CodeAlpha Internship Project: Task 1 - Enterprise Hangman Game

A full-stack, enterprise-grade **Hangman Game & CS Knowledge Platform** built with Python and modern Web technologies. Developed for the **CodeAlpha Python Programming Internship**.

---

## 📌 Project Overview & Technical Scope

- **Goal:** Create an interactive Hangman game capable of serving **unlimited random words** with real-time dictionary definitions, avoiding any fixed or repetitive word lists.
- **Unlimited Dynamic Dictionary:** Uses Python's standard `urllib.request` to dynamically query the open Datamuse Dictionary API in real-time across varied topics (technology, science, nature, space, animals, planet, etc.).
- **Automatic Middle-Letter Foothold:** Pre-reveals the **middle character** of the target word as a starter clue to prevent frustration with long words.
- **Fail-Safe Offline Mode:** Includes a local fallback word dictionary so the game remains 100% playable even if internet connection drops.
- **Dual Execution Environments:** Run via modern responsive Flask Web UI with live animations, or directly in the terminal via `python app.py --cli`.
- **Cloud Ready:** Fully configured with `vercel.json` and serverless entrypoint `api/index.py` for 1-click Vercel deployment.

---

## 🧠 5 Key Concepts Used (Internship Task Rubric)

This project thoroughly demonstrates all 5 foundational Python concepts required by the CodeAlpha internship specification:

### 1. `random` Module
* **Dynamic Topic & Length Selection:** `random.choice(TOPICS)` and `random.randint(5, 8)` generate random query patterns for the dictionary API.
* **Random Word Selection:** `random.choice(candidates)` picks a random word from the fetched pool, and `used_words.add(word)` prevents repeats.
```python
topic = random.choice(TOPICS)
pattern = "?" * random.randint(5, 8)
word, hint = random.choice(candidates)
```

---

### 2. `while` Loops
* **Continuous Turn Execution:** `while not session.is_finished:` keeps the gameplay turn loop alive while lives remain and the secret word has blanks.
* **Session Replay Loop:** `while True:` wraps the game session so the player can seamlessly play consecutive rounds.
* **Input Validation Loop:** `while True:` prompts for player input until a valid non-empty alphabetic character is received.
```python
while not session.is_finished:
    # Display gallows, prompt for letter/word, process turn
    ...
```

---

### 3. `if-else` Conditional Logic
* **Single vs. Full-Word Guess:** Evaluates `if len(guess) > 1:` to branch between full-concept deductions and individual character checks.
* **Character Matching:** `if letter in target:` checks if the input character exists in the secret word; `else:` penalizes a life.
* **Win/Loss State Detection:** Evaluates whether `all(c in guessed for c in target)` to trigger a win, or `if incorrect_guesses >= max_lives:` to trigger defeat.
```python
if letter in target:
    if all(c in session.guessed_letters for c in target):
        session.status = GameStatus.WON
    else:
        message = f"Bravo! Letter '{letter}' is in the word."
else:
    session.incorrect_guesses += 1
    if session.incorrect_guesses >= session.max_lives:
        session.status = GameStatus.LOST
```

---

### 4. `strings` (Sanitization, Membership, Formatting)
* **Sanitization & Normalization:** `raw_guess.strip().upper()` ensures consistent capitalization and strips accidental whitespace.
* **Input Validation:** `.isalpha()` verifies that only valid English letters are submitted.
* **Membership & Counting:** `letter in target` and `target.count(letter)` verify occurrences in the secret string.
* **Middle-Letter Slicing:** `idx = len(word) // 2; mid_char = word[idx]` calculates and extracts the middle character for the starter clue.
* **Dynamic String Joining:** `"  ".join(...)` dynamically formats the spaced letter blanks (`P  Y  T  H  _  N`).

---

### 5. `lists` (Collections, Framing, Display)
* **Gallows ASCII Art Stages:** `HANGMAN_PICS` is a list of multi-line strings representing the 7 visual stages (0 to 6 mistakes).
* **Word Taxonomy Catalogues:** `_CATALOGUE: List[WordEntry]` holds curated computer science concepts.
* **Masked Word Letter Arrays:** `get_masked_word()` uses list comprehension:
```python
def get_masked_word(self) -> List[Optional[str]]:
    return [c if c in self.guessed_letters else None for c in self.word_entry.word]
```
* **Sorted Guessed Lists:** `sorted(list(session.guessed_letters))` renders the historical guessed characters in alphabetical order.

---

## 🏛️ Advanced Software Engineering Architecture

| Engineering Paradigm | Implementation in `app.py` |
| :--- | :--- |
| **Object-Oriented Design (OOP)** | Modular domain architecture: `WordEntry`, `GameSession`, `WordRepository`, `ScoreEngine`, `HangmanService`. |
| **Type Safety & Dataclasses** | PEP 484 type annotations (`List`, `Dict`, `Optional`, `Tuple`, `Set`) and `@dataclass(frozen=True)` value objects. |
| **Domain Enums** | Strict typing for `Difficulty`, `Category`, and `GameStatus` with calculated properties. |
| **Custom Exception Hierarchy** | `HangmanException`, `InvalidGuessException`, `SessionNotFoundException`, `HintExhaustedException`. |
| **Algorithmic Scoring** | Mathematical score engine factoring base length, remaining health, elapsed speed, streak multipliers, and hint penalties. |
| **State Machine & REST API** | RESTful JSON endpoints (`/api/game/new`, `/api/game/guess`, `/api/game/hint`, `/api/meta`). |

## 🎨 Enterprise UI & Feature Highlights

1. **Category & Taxonomy Filtering:**
   - 🐍 *Python & Core Concepts*
   - ⚡ *Algorithms & Data Structures*
   - 🌐 *Full Stack Web Development*
   - 🛡️ *Cybersecurity & Cryptography*
   - ☁️ *Cloud & DevOps Architecture*
   - 🤖 *Artificial Intelligence & Data*
2. **Adaptive Difficulty Modes:**
   - **Easy:** 8 Lives &bull; 3 Strategic Hints &bull; 1.0x Multiplier
   - **Normal:** 6 Lives &bull; 2 Strategic Hints &bull; 1.5x Multiplier
   - **Hard:** 5 Lives &bull; 1 Strategic Hint &bull; 2.2x Multiplier
   - **Expert:** 4 Lives &bull; 0 Hints &bull; 3.5x Multiplier
3. **Web Audio Synthesizer:**
   - Synthesizes click blips, harmonic correct chimes, defeat buzzes, and polyphonic victory fanfares with sound toggle.
4. **Live Round Timer & Speed Bonus:**
   - Tracks elapsed seconds with a live clock, awarding bonus score points for lightning-fast solves.
5. **Interactive Confetti Engine:**
   - Canvas-based particle explosion celebrating victorious rounds.
6. **Technical Explanations on Conclusion:**
   - Displays real-world computer science definitions upon winning or losing to maximize educational value.

---

## 📂 Project Structure

```
Hangman Game/
├── api/
│   └── index.py         # Vercel serverless function entrypoint
├── static/
│   └── style.css        # Modern glassmorphism stylesheet & animations
├── templates/
│   └── index.html       # Primary Flask web application template
├── app.py               # Enterprise Python OOP engine (Web + REST + CLI)
├── index.html           # Standalone offline/hybrid web edition
├── requirements.txt     # Flask dependency specification
├── vercel.json          # Vercel serverless rewrite configuration
├── .gitignore           # Python and cloud ignore rules
└── README.md            # Comprehensive project documentation
```

---

## 🎮 How to Run

### Option 1: Modern Web Application (Recommended)
1. Open PowerShell or Command Prompt in the project directory:
   ```powershell
   python app.py
   ```
2. Open your web browser at:
   ```
   http://127.0.0.1:5002
   ```

### Option 2: Console Terminal Mode (CLI)
Run the ANSI-colored terminal game directly:
```powershell
python app.py --cli
```

### Option 3: Standalone Browser Edition
- Double-click `index.html` in File Explorer to launch the complete client-side game without any server.

---

## 🌐 Deploy to Vercel (Live Worldwide URL)

The repository includes pre-configured serverless files (`vercel.json` and `api/index.py`).

1. Push your code to GitHub:
   ```powershell
   git add .
   git commit -m "Deploy Enterprise Hangman to Vercel"
   git push -u origin main
   ```
2. Go to **[vercel.com/new](https://vercel.com/new)**.
3. Import your GitHub repository and click **Deploy**.

---
*Created for CodeAlpha Internship - Task 1 (Enterprise Hangman Game)*
