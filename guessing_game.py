import random

HIGH_SCORES = {} # Stores best score for each difficulty

DIFFICULTY_LEVELS = {
    "easy": {"range": (1, 50), "attempts": 10},
    "medium": {"range": (1, 100), "attempts": 7},
    "hard": {"range": (1, 200), "attempts": 5}
}

def get_high_score(difficulty):
    return HIGH_SCORES.get(difficulty, float('inf'))

def update_high_score(difficulty, score, guesses_raw, hints_penalty):
    if score < get_high_score(difficulty):
        HIGH_SCORES[difficulty] = score
        print(f"New high score for {difficulty} level: {score} (raw guesses: {guesses_raw}, hint penalty: {hints_penalty})!")

def play_game():
    print("\nWelcome to the Enhanced Number Guessing Game!")

    while True:
        print("\nChoose a difficulty level:")
        for i, level in enumerate(DIFFICULTY_LEVELS.keys(), 1):
            print(f"{i}. {level.capitalize()}")
        
        choice = input(f"Enter choice (1-{len(DIFFICULTY_LEVELS)}): ")
        
        difficulty_key = None
        if choice.isdigit() and 1 <= int(choice) <= len(DIFFICULTY_LEVELS):
            difficulty_key = list(DIFFICULTY_LEVELS.keys())[int(choice)-1]
        else:
            print("Invalid choice. Please select a valid number.")
            continue
        
        current_difficulty = DIFFICULTY_LEVELS[difficulty_key]
        min_num, max_num = current_difficulty["range"]
        allowed_attempts = current_difficulty["attempts"]
        
        secret_number = random.randint(min_num, max_num)
        guesses_taken = 0
        hints_used_penalty = 0
        current_min_range = min_num
        current_max_range = max_num
        
        print(f"\nDifficulty: {difficulty_key.capitalize()}")
        print(f"I've picked a number between {min_num} and {max_num}. You have {allowed_attempts} attempts.")
        current_best = get_high_score(difficulty_key)
        if current_best != float('inf'):
            print(f"Current high score for this level: {current_best} guesses (score includes hint penalties if any).")
        else:
            print("No high score set for this level yet. Be the first!")

        while guesses_taken < allowed_attempts:
            guess_str = input(f"Attempt {guesses_taken + 1}/{allowed_attempts} - Enter your guess (or type 'hint'): ").lower()
            
            if guess_str == 'hint':
                if current_min_range > current_max_range:
                    print("Hint: Cannot provide a hint, your previous guesses are conflicting.")
                elif current_min_range == current_max_range:
                    print(f"Hint: The number must be {current_min_range}!")
                else:
                    suggested_guess = (current_min_range + current_max_range) // 2
                    print(f"Hint: Try guessing around {suggested_guess}. (This will add 1 to your hint penalty)")
                    hints_used_penalty += 1
                continue # Doesn't count as an attempt

            try:
                if not guess_str.isdigit():
                    print("Invalid input. Please enter a number or 'hint'.")
                    continue
                guess = int(guess_str)
            except ValueError:
                print("Invalid input. Please enter a number or 'hint'.")
                continue

            guesses_taken += 1

            if guess < secret_number:
                print("Too low!")
                current_min_range = max(current_min_range, guess + 1)
            elif guess > secret_number:
                print("Too high!")
                current_max_range = min(current_max_range, guess - 1)
            else:
                final_score = guesses_taken + hints_used_penalty
                print(f"Congratulations! You guessed the number {secret_number} in {guesses_taken} guesses.")
                if hints_used_penalty > 0:
                    print(f"(Hint penalty: {hints_used_penalty}. Total score: {final_score})")
                update_high_score(difficulty_key, final_score, guesses_taken, hints_used_penalty)
                break
        else: # Loop finished without a break (ran out of attempts)
            print(f"Sorry, you've run out of attempts. The number was {secret_number}.")

        play_again = input("Play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye.")
            break

if __name__ == "__main__":
    play_game() 