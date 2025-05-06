# Enhanced Number Guessing Game

This is a command-line Number Guessing Game built in Python with a smart hint system.

## Features

- **Difficulty Levels**: Choose between Easy, Medium, and Hard.
    - Easy: Guess a number between 1 and 50 (10 attempts).
    - Medium: Guess a number between 1 and 100 (7 attempts).
    - Hard: Guess a number between 1 and 200 (5 attempts).
- **Random Number Generation**: The computer picks a random number in the chosen range.
- **Interactive Guessing**: Enter your guess and get feedback (Too high, Too low, Correct).
- **Smart Hint System**:
    - Type `hint` to get a suggestion for your next guess.
    - The hint is based on an optimal search strategy (like binary search), considering your previous guesses to narrow down the possible range.
    - Using a hint does not consume an attempt, but adds `1` to a hint penalty, affecting your final score for high score tracking.
- **Limited Attempts**: Each difficulty level has a set number of attempts.
- **High Score Tracking**: 
    - The game saves and displays the best score for each difficulty level during the session.
    - The score is calculated as `actual guesses + hint penalty`.
- **Play Again**: Option to play another round without restarting the script.

## How to Run

1.  Ensure you have Python installed on your system.
2.  Navigate to the `number-guessing-game` directory in your terminal.
3.  Run the game using the command:
    ```bash
    python guessing_game.py
    ```

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