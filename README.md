# Advanced CLI Number Guessing Game

This is a feature-rich, command-line Number Guessing Game built in Python, featuring user profiles, persistent high scores, advanced hints, and more.

## Core Features

- **User Profiles & Persistent Data**:
    - Enter a username to play.
    - Game progress, high scores, and statistics are saved per user in `game_data.json`.
- **Difficulty Levels**: Choose between Easy, Medium, and Hard, each with different number ranges, attempts, and hint allowances.
    - Easy: Range 1-50, 10 attempts, 3 hints.
    - Medium: Range 1-100, 7 attempts, 2 hints.
    - Hard: Range 1-200, 5 attempts, 1 hint.
- **Advanced Hint System**:
    - **Strategic Suggestion**: Get a hint for an optimal guess (binary search style).
    - **Parity Hint**: Reveals if the secret number is even or odd.
    - **Primality Hint**: Reveals if the secret number is prime (available for smaller number ranges).
    - **Automatic Warmth Feedback**: After each guess, the game tells you if you're "Warmer" or "Colder" than your previous guess.
    - Hints consume a limited per-round allowance and add a penalty to your score for that round.
- **Comprehensive Statistics**:
    - Tracks per-user: Games Played, Total Wins, Average Guesses per Win.
    - Personal best scores for each difficulty level.
- **Overall Leaderboard**: View the top scores across all users and difficulties.
- **Interactive Menu System**:
    - Main Menu: Play, View My Stats, View Leaderboard, Change User, Quit.
- **Engaging Console UI**: Utilizes simple text formatting for a clearer and more structured presentation.

## How to Run

1.  Ensure you have Python 3.x installed.
2.  Navigate to the `number-guessing-game` directory in your terminal.
3.  Run the game:
    ```bash
    python guessing_game.py
    ```
4.  Follow the on-screen prompts to enter a username and navigate the menus.

## Gameplay Flow

1.  **Login/Register**: Enter your username. If new, a profile is created.
2.  **Main Menu**: 
    - Choose to play a new round.
    - View your personal statistics.
    - Check the overall leaderboard.
    - Logout to change user.
    - Quit the game (saves data).
3.  **Playing a Round**:
    - Select a difficulty level.
    - Make guesses. Input `hint` to access the hint menu.
    - Automatic "Warmer/Colder" feedback is provided after the second guess onwards.
    - Win by guessing the number, or lose if attempts run out.
    - Scores (guesses + hint penalties) are recorded.

## Data Storage

- User data and high scores are stored in `game_data.json` in the same directory as the script.
- Deleting this file will reset all saved progress and scores.

## Dependencies

- Python 3.x
- `json` module (standard library)
- `os` module (standard library)
- `random` module (standard library)

## Gameplay Example (with Hint)

```
Welcome to the Enhanced Number Guessing Game!

Choose a difficulty level:
1. Easy
2. Medium
3. Hard
Enter choice (1-3): 1

Difficulty: Easy
I've picked a number between 1 and 50. You have 10 attempts.
No high score set for this level yet. Be the first!
Attempt 1/10 - Enter your guess (or type 'hint'): 25
Too high!
Attempt 2/10 - Enter your guess (or type 'hint'): 10
Too low!
Attempt 3/10 - Enter your guess (or type 'hint'): hint
Hint: Try guessing around 17. (This will add 1 to your hint penalty)
Attempt 3/10 - Enter your guess (or type 'hint'): 17
Too high!
Attempt 4/10 - Enter your guess (or type 'hint'): 13
Congratulations! You guessed the number 13 in 4 guesses.
(Hint penalty: 1. Total score: 5)
New high score for easy level: 5 (raw guesses: 4, hint penalty: 1)!
Play again? (yes/no): no
Thanks for playing! Goodbye.
```

**Note**: The hint system provides guidance based on narrowing the numerical range. It's a form of strategic help, not machine learning prediction. 