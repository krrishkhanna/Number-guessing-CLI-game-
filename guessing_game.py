import random
import json
import os

DATA_FILE = "game_data.json"

DIFFICULTY_LEVELS = {
    "easy": {"range": (1, 50), "attempts": 10, "max_hints": 3},
    "medium": {"range": (1, 100), "attempts": 7, "max_hints": 2},
    "hard": {"range": (1, 200), "attempts": 5, "max_hints": 1}
}

# --- Data Handling ---
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Error loading game data. Starting fresh.")
            return {}
    return {}

def save_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        print("Error saving game data.")

def get_user_data(username, all_data):
    if username not in all_data:
        all_data[username] = {
            "high_scores": {level: float('inf') for level in DIFFICULTY_LEVELS},
            "games_played": 0,
            "total_wins": 0,
            "total_guesses_in_wins": 0 # For avg calculation
        }
    return all_data[username]

# --- UI Elements (Simple Text Art) ---
def print_header(text):
    print("\n" + "="*40)
    print(f"{text:^40}")
    print("="*40)

def print_separator():
    print("-"*40)

# --- Game Logic ---
def get_best_score(user_data, difficulty):
    return user_data["high_scores"].get(difficulty, float('inf'))

def update_user_stats_on_win(user_data, difficulty, score, raw_guesses):
    user_data["total_wins"] += 1
    user_data["total_guesses_in_wins"] += raw_guesses
    if score < user_data["high_scores"].get(difficulty, float('inf')):
        user_data["high_scores"][difficulty] = score
        print(f"NEW PERSONAL BEST for {difficulty} level: {score} points!")
    save_data(game_data) # Save immediately after stat update

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def play_round(username, user_data):
    print_header("Number Guessing Challenge")
    
    # Choose difficulty
    print("\nChoose Difficulty Level:")
    levels = list(DIFFICULTY_LEVELS.keys())
    for i, level in enumerate(levels, 1):
        print(f"  {i}. {level.capitalize()} (Range: {DIFFICULTY_LEVELS[level]['range'][0]}-{DIFFICULTY_LEVELS[level]['range'][1]}, Attempts: {DIFFICULTY_LEVELS[level]['attempts']}, Hints: {DIFFICULTY_LEVELS[level]['max_hints']})")
    
    choice = input(f"Enter choice (1-{len(levels)}): ")
    if not choice.isdigit() or not (1 <= int(choice) <= len(levels)):
        print("Invalid difficulty. Returning to main menu.")
        return
    difficulty_key = levels[int(choice)-1]
    config = DIFFICULTY_LEVELS[difficulty_key]
    min_num, max_num = config["range"]
    allowed_attempts = config["attempts"]
    max_hints_allowed = config["max_hints"]

    secret_number = random.randint(min_num, max_num)
    guesses_taken = 0
    hints_used_penalty_score = 0
    hints_requested_this_round = 0
    
    current_min_range = min_num
    current_max_range = max_num
    last_guess_diff = float('inf')

    user_data["games_played"] += 1
    print(f"\n--- {difficulty_key.capitalize()} Mode --- Number between {min_num}-{max_num} ---")
    personal_best = get_best_score(user_data, difficulty_key)
    if personal_best != float('inf'):
        print(f"Your best for this level: {personal_best} points.")

    while guesses_taken < allowed_attempts:
        prompt = f"Attempt {guesses_taken + 1}/{allowed_attempts} | Hints left: {max_hints_allowed - hints_requested_this_round} | Guess or type 'hint': "
        user_input = input(prompt).lower().strip()

        if user_input == 'hint':
            if hints_requested_this_round >= max_hints_allowed:
                print("No more hints allowed this round.")
                continue

            print("\nAvailable Hints:")
            print("  1. Suggest a guess (binary search style)")
            print("  2. Parity (is the number even or odd?)")
            if min_num <= 100 and max_num >=1 : # Prime hint only for smaller ranges
                 print("  3. Primality (is the number prime?)")
            hint_choice = input("Choose hint type (or 'cancel'): ").lower()

            valid_hint_chosen = False
            if hint_choice == '1':
                if current_min_range > current_max_range: print("Hint: Range conflict from guesses.")
                elif current_min_range == current_max_range: print(f"Hint: Must be {current_min_range}!")
                else: print(f"Hint: Try around {(current_min_range + current_max_range) // 2}.")
                valid_hint_chosen = True
            elif hint_choice == '2':
                print(f"Hint: The number is {'even' if secret_number % 2 == 0 else 'odd'}.")
                valid_hint_chosen = True
            elif hint_choice == '3' and min_num <=100 and max_num >=1:
                print(f"Hint: The number is {'prime' if is_prime(secret_number) else 'not prime'}.")
                valid_hint_chosen = True
            elif hint_choice == 'cancel':
                print("Hint cancelled.")
            else:
                print("Invalid hint choice.")
            
            if valid_hint_chosen:
                hints_used_penalty_score += 2 # Penalty for using a hint
                hints_requested_this_round += 1
                print("(Hint used. Penalty +2 to score for this round.)")
            print_separator()
            continue # Hint does not consume an attempt
        
        if not user_input.isdigit():
            print("Invalid input. Please enter a number or 'hint'.")
            continue
        
        guess = int(user_input)
        guesses_taken += 1
        current_guess_diff = abs(secret_number - guess)

        if guess == secret_number:
            final_score = guesses_taken + hints_used_penalty_score
            print(f"\n*** Correct! The number was {secret_number}! ***")
            print(f"You guessed it in {guesses_taken} raw guesses.")
            if hints_used_penalty_score > 0:
                print(f"Hint penalty: +{hints_used_penalty_score}")
            print(f"Your final score for this round: {final_score} points.")
            update_user_stats_on_win(user_data, difficulty_key, final_score, guesses_taken)
            return # End round
        elif guess < secret_number:
            print("Too low!")
            current_min_range = max(current_min_range, guess + 1)
        else: # guess > secret_number
            print("Too high!")
            current_max_range = min(current_max_range, guess - 1)
        
        # Warmth hint (automatic)
        if guesses_taken > 1 and current_guess_diff != float('inf'):
            if current_guess_diff < last_guess_diff:
                print("  (You're getting warmer!)")
            elif current_guess_diff > last_guess_diff:
                print("  (You're getting colder.)")
        last_guess_diff = current_guess_diff
        
        if guesses_taken == allowed_attempts:
            print(f"\n--- Game Over --- You ran out of attempts.")
            print(f"The secret number was: {secret_number}")
            break
    save_data(game_data) # Save data at the end of a round (win or loss)

def view_my_stats(username, user_data):
    print_header(f"Stats for {username}")
    print(f"  Games Played: {user_data['games_played']}")
    print(f"  Total Wins: {user_data['total_wins']}")
    if user_data['total_wins'] > 0:
        avg_guesses = user_data['total_guesses_in_wins'] / user_data['total_wins']
        print(f"  Average Guesses per Win: {avg_guesses:.2f}")
    else:
        print("  Average Guesses per Win: N/A")
    print("\n  Personal Best Scores (lower is better):")
    for level, score in user_data['high_scores'].items():
        score_display = score if score != float('inf') else "Not set"
        print(f"    - {level.capitalize()}: {score_display}")
    print_separator()

def view_leaderboard(all_data):
    print_header("Overall Leaderboard")
    leaderboard = []
    for user, data in all_data.items():
        for level, score in data['high_scores'].items():
            if score != float('inf'):
                leaderboard.append((user, level, score))
    
    if not leaderboard:
        print("No scores on the leaderboard yet!")
        return

    # Sort by score (ascending), then by user, then by difficulty
    leaderboard.sort(key=lambda x: (x[2], x[0], x[1]))
    
    print("(Top 10 scores shown)")
    for i, (user, level, score) in enumerate(leaderboard[:10]):
        print(f"  {i+1}. {user} ({level.capitalize()}) - {score} points")
    print_separator()

# --- Main Application Flow ---
game_data = load_data()

def main():
    print_header("Welcome to the Advanced Number Guesser!")
    
    while True:
        current_username = input("\nEnter your username (or type 'exit' to quit): ").strip()
        if not current_username:
            print("Username cannot be empty.")
            continue
        if current_username.lower() == 'exit':
            break

        current_user_data = get_user_data(current_username, game_data)
        print(f"\nWelcome, {current_username}!")

        while True:
            print_header(f"Main Menu - Logged in as {current_username}")
            print("  1. Play New Round")
            print("  2. View My Stats")
            print("  3. View Overall Leaderboard")
            print("  4. Change User / Logout")
            print("  5. Quit Game")
            menu_choice = input("Select an option: ").strip()

            if menu_choice == '1':
                play_round(current_username, current_user_data)
            elif menu_choice == '2':
                view_my_stats(current_username, current_user_data)
            elif menu_choice == '3':
                view_leaderboard(game_data)
            elif menu_choice == '4':
                print(f"Logging out {current_username}...")
                break # Breaks to outer username input loop
            elif menu_choice == '5':
                print("Thanks for playing! Goodbye.")
                save_data(game_data) # Final save before exiting
                return # Exits application
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 