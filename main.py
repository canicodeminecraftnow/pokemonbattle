import json
import hashlib
import os
import random
import getpass
import sys

# Path to the users data file
USERS_FILE = 'users.json'

# Hard-coded list of Generation 1 Pokémon
POKEMONS = [
    {"name": "Bulbasaur", "hp": 45, "attack": 49, "defense": 49, "speed": 45},
    {"name": "Charmander", "hp": 39, "attack": 52, "defense": 43, "speed": 65},
    {"name": "Squirtle", "hp": 44, "attack": 48, "defense": 65, "speed": 43},
    {"name": "Pikachu", "hp": 35, "attack": 55, "defense": 40, "speed": 90},
    {"name": "Eevee", "hp": 55, "attack": 55, "defense": 50, "speed": 55},
    {"name": "Jigglypuff", "hp": 115, "attack": 45, "defense": 20, "speed": 20},
    {"name": "Meowth", "hp": 40, "attack": 45, "defense": 35, "speed": 90},
    {"name": "Psyduck", "hp": 50, "attack": 52, "defense": 48, "speed": 55},
    {"name": "Geodude", "hp": 40, "attack": 80, "defense": 100, "speed": 20},
    {"name": "Snorlax", "hp": 160, "attack": 110, "defense": 65, "speed": 30}
]

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    users = load_users()
    print("\n=== Register ===")
    while True:
        username = input("Enter a username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue
        if username in users:
            print("Username already exists. Please choose a different one.")
        else:
            break
    while True:
        # Using getpass to hide password input
        password = getpass.getpass("Enter a password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
        elif not password:
            print("Password cannot be empty.")
        else:
            break
    hashed_pw = hash_password(password)
    users[username] = {"password": hashed_pw, "wins": 0, "losses": 0}
    save_users(users)
    print(f"Account created successfully for {username}!\n")

def login():
    users = load_users()
    print("\n=== Login ===")
    username = input("Enter your username: ").strip()
    if username not in users:
        print("Username does not exist. Please register first.\n")
        return None
    password = getpass.getpass("Enter your password: ")
    hashed_pw = hash_password(password)
    if hashed_pw != users[username]["password"]:
        print("Incorrect password. Please try again.\n")
        return None
    print(f"Logged in successfully as {username}!\n")
    return username

def select_pokemon(current_user, users):
    print("=== Select Your Pokémon ===")
    print("Available Pokémon:")
    for idx, pokemon in enumerate(POKEMONS, start=1):
        print(f"{idx}. {pokemon['name']} (HP: {pokemon['hp']}, Attack: {pokemon['attack']}, Defense: {pokemon['defense']}, Speed: {pokemon['speed']})")
    while True:
        try:
            choice = int(input("Select a Pokémon by number: "))
            if 1 <= choice <= len(POKEMONS):
                selected_pokemon = POKEMONS[choice - 1]
                print(f"You selected {selected_pokemon['name']}!\n")
                break
            else:
                print(f"Please enter a number between 1 and {len(POKEMONS)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    return selected_pokemon

def battle(player1, player2, user1, user2, users):
    print("\n=== Battle Start ===")
    print(f"{user1} has {player1['name']} (HP: {player1['hp']})")
    print(f"{user2} has {player2['name']} (HP: {player2['hp']})\n")

    # Determine turn order based on speed
    if player1['speed'] >= player2['speed']:
        turn_order = [(user1, player1, user2, player2), (user2, player2, user1, player1)]
    else:
        turn_order = [(user2, player2, user1, player1), (user1, player1, user2, player2)]

    # Clone HP to track during battle
    hp1 = player1['hp']
    hp2 = player2['hp']

    while hp1 > 0 and hp2 > 0:
        for attacker_user, attacker_pokemon, defender_user, defender_pokemon in turn_order:
            # Calculate damage
            damage = max(1, attacker_pokemon['attack'] - defender_pokemon['defense'])
            if defender_user == user1:
                hp1 -= damage
                current_hp = hp1
            else:
                hp2 -= damage
                current_hp = hp2
            print(f"{attacker_user}'s {attacker_pokemon['name']} attacks {defender_user}'s {defender_pokemon['name']} for {damage} damage.")
            print(f"{defender_user}'s {defender_pokemon['name']} HP is now {current_hp}.\n")
            if current_hp <= 0:
                print(f"{defender_user}'s {defender_pokemon['name']} has fainted!")
                if defender_user == "Computer":
                    print(f"{attacker_user} wins the battle!\n")
                    users[attacker_user]['wins'] += 1
                    # No need to update 'Computer's losses
                else:
                    print(f"{attacker_user} wins the battle!\n")
                    users[attacker_user]['wins'] += 1
                    users[defender_user]['losses'] += 1
                save_users(users)
                return
    print("The battle ended in a draw!\n")

def view_stats(current_user, users):
    user_data = users[current_user]
    print("\n=== Your Statistics ===")
    print(f"Wins: {user_data['wins']}")
    print(f"Losses: {user_data['losses']}\n")

def main_menu():
    users = load_users()
    current_user = None
    while True:
        print("=== Pokémon Battle Game ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option: ").strip()
        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                current_user = user
                user_menu(current_user, users)
        elif choice == '3':
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please select 1, 2, or 3.\n")

def user_menu(current_user, users):
    while True:
        print(f"=== Welcome, {current_user}! ===")
        print("1. View Statistics")
        print("2. Battle with a Friend")
        print("3. Logout")
        choice = input("Select an option: ").strip()
        if choice == '1':
            view_stats(current_user, users)
        elif choice == '2':
            print("\n=== Battle Mode ===")
            print("1. Battle against another user")
            print("2. Battle against the computer")
            battle_choice = input("Select battle mode: ").strip()
            if battle_choice == '1':
                battle_against_user(current_user, users)
            elif battle_choice == '2':
                battle_against_computer(current_user, users)
            else:
                print("Invalid choice. Returning to user menu.\n")
        elif choice == '3':
            print(f"Logging out {current_user}...\n")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.\n")

def battle_against_user(current_user, users):
    users_list = list(users.keys())
    users_list.remove(current_user)
    if not users_list:
        print("No other users available to battle. Please register another account.\n")
        return
    print("\nAvailable opponents:")
    for idx, user in enumerate(users_list, start=1):
        print(f"{idx}. {user} (Wins: {users[user]['wins']}, Losses: {users[user]['losses']})")
    while True:
        try:
            choice = int(input("Select an opponent by number: "))
            if 1 <= choice <= len(users_list):
                opponent = users_list[choice - 1]
                break
            else:
                print(f"Please enter a number between 1 and {len(users_list)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    print(f"\nYou are battling against {opponent}!\n")
    print(f"=== {current_user}'s Turn to Select Pokémon ===")
    player1 = select_pokemon(current_user, users)
    print(f"=== {opponent}'s Turn to Select Pokémon ===")
    # Opponent selects a random Pokémon
    player2 = random.choice(POKEMONS)
    print(f"{opponent} selected {player2['name']}!\n")
    battle(player1, player2, current_user, opponent, users)

def battle_against_computer(current_user, users):
    print("\n=== Computer Battle ===")
    print(f"=== {current_user}'s Turn to Select Pokémon ===")
    player1 = select_pokemon(current_user, users)
    # Computer selects a random Pokémon
    player2 = random.choice(POKEMONS)
    print(f"Computer selected {player2['name']}!\n")
    battle(player1, player2, current_user, "Computer", users)

if __name__ == "__main__":
    main_menu()
