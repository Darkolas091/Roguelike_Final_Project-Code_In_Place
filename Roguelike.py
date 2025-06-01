import random


def main():
    MOVES = ["w",'a','s','d','q']
    number_of_additional_rooms = 2
    lives = 2
    coins = 0

    #Player starting position
    player_row = 1
    player_col = 1

    #Flag to control the game loop
    continue_game = True

    #Create an empty grid with walls and a door
    game_map = []

    #FUNCTION DEFINITIONS
    #Debug message for movement
    def print_if_moved(direction):
        print(f"\nDebug: Moved {direction}")
    
    #Delete the old position of the player and print debug message
    def delete_old_pos(row, col):
        print("Debug: deleted old position")
        game_map[row][col] = " "

    #Function to create rooms based on a seed or random generation
    def create_rooms(seed=None):
        rooms = []
        seed_string = ""
        number_of_rooms = number_of_additional_rooms + 1  #total rooms including the first

        if seed:
            seed_str = str(seed)
            remaining_seed = seed_str
        else:
            remaining_seed = None

        for room_index in range(number_of_rooms):
            #Generate dimensions and door location
            if remaining_seed and len(remaining_seed) >= 4:
                rows = int(remaining_seed[:2]) // 10
                cols = int(remaining_seed[:2]) % 10
                door_row = int(remaining_seed[2:4]) // 10
                door_col = int(remaining_seed[2:4]) % 10
                remaining_seed = remaining_seed[4:]
            else:
                rows = random.randint(5, 8)
                cols = random.randint(5, 8)
                #Place the door on a random border (not in the corners)
                while True:
                    border = random.choice(['top', 'bottom', 'left', 'right'])
                    if border == 'top':
                        door_row = 0
                        door_col = random.randint(1, cols - 2)
                    elif border == 'bottom':
                        door_row = rows - 1
                        door_col = random.randint(1, cols - 2)
                    elif border == 'left':
                        door_row = random.randint(1, rows - 2)
                        door_col = 0
                    else:  #right
                        door_row = random.randint(1, rows - 2)
                        door_col = cols - 1
                    #Avoid player start position
                    if not (door_row == 1 and door_col == 1):
                        break

            #Create the room grid
            room = []
            for i in range(rows):
                if i == 0 or i == rows - 1:
                    room.append(["#"] * cols)
                else:
                    row = ["#"] + [" "] * (cols - 2) + ["#"]
                    room.append(row)

            #Add the door
            room[door_row][door_col] = "D"
            print(f"Debug: Created room {room_index+1} with dimensions {rows}x{cols} and door at ({door_row}, {door_col})")
            rooms.append(room)

            #Randomly place wall in the room, with a maximum number of attempts to avoid infinite loops
            wall_placed = False
            wall_attempts = 0
            max_wall_attempts = 20
            while not wall_placed and wall_attempts < max_wall_attempts:
                if cols < 5:
                    break  # Not enough space for a wall
                wallstart_col = random.randint(2, cols - 3)
                print(f" Debug: Placing wall at column {wallstart_col}")
                gap_row = random.randint(1, rows - 2)
                wall_possible = True
                for i in range(1, rows - 1):
                    if i == gap_row or (i == door_row + 1 and wallstart_col == door_col) or (i == door_row - 1 and wallstart_col == door_col):
                        continue
                    if room[i][wallstart_col] == "D":
                        wall_possible = False
                        break
                if wall_possible:
                    for i in range(1, rows - 1):
                        if i == gap_row or (i == door_row + 1 and wallstart_col == door_col) or (i == door_row - 1 and wallstart_col == door_col):
                            continue
                        room[i][wallstart_col] = "#"
                    wall_placed = True
                wall_attempts += 1

            #Add an Enemy (E) at a random position in the room, not 2 spaces away from start, with a maximum number of attempts
            enemy_placed = False
            enemy_attempts = 0
            max_enemy_attempts = 50
            while not enemy_placed and enemy_attempts < max_enemy_attempts:
                enemy_row = random.randint(1, rows - 2)
                enemy_col = random.randint(1, cols - 2)
                if (abs(enemy_row - 1) > 2 or abs(enemy_col - 1) > 2) and (room[enemy_row][enemy_col] == " "):
                    room[enemy_row][enemy_col] = "E"
                    enemy_placed = True
                enemy_attempts += 1
            if not enemy_placed:
                print("Debug: Could not place enemy after many attempts.")

            #Add a Coin (C) at a random position in the room, not 2 spaces away from start, with a maximum number of attempts
            coin_placed = False
            coin_attempts = 0
            max_coin_attempts = 50
            while not coin_placed and coin_attempts < max_coin_attempts:
                coin_row = random.randint(1, rows - 2)
                coin_col = random.randint(1, cols - 2)
                if (abs(coin_row - 1) > 2 or abs(coin_col - 1) > 2) and (room[coin_row][coin_col] == " "):
                    room[coin_row][coin_col] = "C"
                    coin_placed = True
                coin_attempts += 1
            if not coin_placed:
                print("Debug: Could not place coin after many attempts.")

            #Append dimensions and door location to the seed string
            seed_string += f"{rows}{cols}{door_row}{door_col}{enemy_row}{enemy_col}{coin_row}{coin_col}"

        print(f"Debug: Generated seed string for rooms: {seed_string}")
        return rooms, seed_string

    def play_room(game_map, player_row, player_col,lives,coins):
        #Reset player position to (1, 1) in the new room
        player_row, player_col = 1, 1
        game_map[player_row][player_col] = "P"
        
        continue_game = True
        room_moves = 0  #Counter for moves in the current room

        while continue_game:
            #Input of movement, WASD converted to lower to check against list
            move = input()
            move = move.lower()
            if move in MOVES:
                if lives < 0:
                    print("\nYou have no lives left! Game over!")
                    continue_game = False

                    break

                if move == 'w':
                    if game_map[player_row][player_col + 1] == 'C':
                        print("You found a coin! You now have", coins + 1, "coins.")
                        coins += 1
                        delete_old_pos(player_row, player_col)
                        player_col += 1
                        room_moves += 1
                    elif game_map[player_row - 1][player_col] == 'E':
                        print("You encountered an enemy! You lost a life!")
                        lives -= 1
                        print("You have", lives, "revives left.")
                        delete_old_pos(player_row, player_col)
                        player_row -= 1
                        room_moves += 1
                    elif game_map[player_row - 1][player_col] == 'D':
                        print("You found the door! Moving to the next room...")
                        room_moves += 1
                        continue_game = False
                    elif game_map[player_row - 1][player_col] != '#':
                        delete_old_pos(player_row, player_col)
                        player_row -= 1
                        print_if_moved(move)
                        room_moves += 1

                elif move == 'd':
                    if game_map[player_row][player_col + 1] == 'C':
                        print("You found a coin! You now have", coins + 1, "coins.")
                        coins += 1
                        delete_old_pos(player_row, player_col)
                        player_col += 1
                        room_moves += 1
                    elif game_map[player_row][player_col + 1] == 'E':
                        print("You encountered an enemy! You lost a life!")
                        lives -= 1
                        print("You have", lives, "revives left.")
                        delete_old_pos(player_row, player_col)
                        player_col += 1
                        room_moves += 1
                    elif game_map[player_row][player_col + 1] == 'D':
                        print("You found the door! Moving to the next room...")
                        room_moves += 1
                        continue_game = False
                    elif game_map[player_row][player_col + 1] != '#':
                        delete_old_pos(player_row, player_col)
                        player_col += 1
                        print_if_moved(move)
                        room_moves += 1

                elif move == 's':
                    if game_map[player_row + 1][player_col] == 'C':
                        print("You found a coin! You now have", coins + 1, "coins.")
                        coins += 1
                        delete_old_pos(player_row, player_col)
                        player_row += 1
                        room_moves += 1
                    elif game_map[player_row + 1][player_col] == 'E':
                        print("You encountered an enemy! You lost a life!")
                        lives -= 1
                        print("You have", lives, "revives left.")
                        delete_old_pos(player_row, player_col)
                        player_row += 1
                        room_moves += 1
                    elif game_map[player_row + 1][player_col] == 'D':
                        print("You found the door! Moving to the next room...")
                        room_moves += 1
                        continue_game = False
                    elif game_map[player_row + 1][player_col] != '#':
                        delete_old_pos(player_row, player_col)
                        player_row += 1
                        print_if_moved(move)
                        room_moves += 1

                elif move == 'a':
                    if game_map[player_row][player_col - 1] == 'C':
                        print("You found a coin! You now have", coins + 1, "coins.")
                        coins += 1
                        delete_old_pos(player_row, player_col)
                        player_col -= 1
                        room_moves += 1
                    elif game_map[player_row][player_col - 1] == 'E':
                        print("You encountered an enemy! You lost a life!")
                        lives -= 1
                        print("You have", lives, "revives left.")
                        delete_old_pos(player_row, player_col)
                        player_col -= 1
                        room_moves += 1
                    elif game_map[player_row][player_col - 1] == 'D':
                        print("You found the door! Moving to the next room...")
                        room_moves += 1
                        continue_game = False
                    elif game_map[player_row][player_col - 1] != '#':
                        delete_old_pos(player_row, player_col)
                        player_col -= 1
                        print_if_moved(move)
                        room_moves += 1

                elif move == 'q':
                    continue_game = False
                    #Display the map
                    for row in game_map:
                        print(" ".join(row))
                    print("\nDebug: quit")
                    print(f"Room moves: {room_moves}")
                    exit(0)

                print("Debug: tried to move")
                game_map[player_row][player_col] = "P"

                #Display the map
                for row in game_map:
                    print(" ".join(row))

        print(f"Room completed in {room_moves} moves.")
        return room_moves, lives, coins



    #GAME START CODE
    #Create rooms with a seed
    seed_string = ""
    seed = input("Enter a seed (or press Enter to skip): ")
    seed = seed.strip()  # Remove any leading/trailing whitespace
    rooms,seed_string = create_rooms(seed)

    #Set the first room as the initial game map
    game_map = rooms[0]
    #Place the player in the initial room
    game_map[player_row][player_col] = "P"

    #Print instructions
    print("\nInstructions:")
    print("Use 'W' to move up, 'A' to move left, 'S' to move down, 'D' to move right.\n")
    print("Try to find the door (D) to exit the room as efficiently as u can.")


    #Loop through rooms
    total_moves = 0  #nitialize total moves counter
    rome_moves = []
    for room in rooms:
        game_map = room
        game_map[1][1] = "P"
        for row in game_map:
            print(" ".join(row))
        room_moves_value, lives, coins = play_room(game_map, 1, 1, lives, coins)
        total_moves += room_moves_value
        rome_moves.append(room_moves_value)

        print(f"Moves in this room: {room_moves_value}")
        print(f"Total moves so far: {total_moves}")
        print(f"Revives left: {lives}")

    #Score calculation
    score = 0
    monsters_defeated = 0
    if lives == 1:
        score += 50
        monsters_defeated = 1
    elif lives == 0:
        score += 100 
        monsters_defeated = 2
    score += coins * 100 - total_moves * 5

    print("\n\n\n")
    if lives == -1:
        print("\nYou got defeated!")
        print("FINAL SCORE: ", score)
        print(f"Monsters defeated: 2 {2 * 50}points")
        print(f"Coins collected: {coins} {coins * 100}points")
        print(f"Total moves in all rooms: {total_moves} {total_moves * -5 * 2}points DOUBLE PENALTY FOR DYING") 
    else:
        print("FINAL SCORE: ", score)
        print(f"Monsters defeated: {monsters_defeated} {monsters_defeated * 50}points")
        print(f"Coins collected: {coins} {coins * 100}points")
        print(f"Total moves in all rooms: {total_moves} {total_moves * -5}points")
        print("Moves in each room:", rome_moves)


    print("\nSeed used for room generation:", seed_string)  # Display the seed string generated
    print("You can use this seed to recreate the same room layout in future games to try and get a higher score.")
    print("Thank you for playing!")

    explain = input("If you want to explain the seed meaning, type yes, otherwise press Enter to exit: ")
    if explain.lower() == 'yes':
            print("\nSeed Explanation:")
            print("The seed string is a sequence of numbers that stores the dimensions and door locations of each room.")
            print("Each room's data is represented as follows:")
            print("Rows, Columns, Door Row, Door Column, Enemy Row, Enemy Column, Coin Row, Coin Column")
            print("For example, a seed string '750343517544515387503435' is broken down:")
            print("This is the first room 75034351")
            print("Room 1: 7 rows, 5 columns, door at (0, 3), enemy at (4, 3), coin at (5, 1)")

if __name__ == "__main__":
    
        main()
    