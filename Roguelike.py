import random


def main():
    MOVES = ["w",'a','s','d','q']
    number_of_additional_rooms = 2

    #Player starting position
    player_row = 1
    player_col = 1

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


    # Function to create rooms based on a fake "seed" or random generation
    def create_rooms(seed=None):
        rooms = []
        seed_string = ""  # Initialize seed string to store room dimensions and door locations

        # Generate dimensions for the first room
        if seed:
            # Extract rows, columns, and door location from the seed value
            seed_str = str(seed)
            rows = int(seed_str[:2]) // 10  # Divide the first two digits by 10 for rows
            cols = int(seed_str[:2]) % 10   # Use the remainder of the division for columns
            door_row = int(seed_str[2:4]) // 10
            door_col = int(seed_str[2:4]) % 10
            remaining_seed = seed_str[4:]   # Remaining part of the seed for additional rooms
        else:
            rows = random.randint(4, 7)
            cols = random.randint(4, 7)
            while True:
                door_row = random.randint(1, rows - 2)
                door_col = random.choice([0, cols - 1])
                if not (door_row == 1 and door_col == 1):
                    break
            remaining_seed = None

        # Create the first room
        room = []
        for i in range(rows):
            if i == 0 or i == rows - 1:
                # Top and bottom walls
                room.append(["#"] * cols)
            else:
                # Middle rows with walls on the sides
                row = ["#"] + [" "] * (cols - 2) + ["#"]
                room.append(row)

        # Add the door to the first room
        room[door_row][door_col] = "D"
        print(f"Debug: Created first room with dimensions {rows}x{cols} and door at ({door_row}, {door_col})")
        rooms.append(room)

        # Append dimensions and door location of the first room to the seed string
        seed_string += f"{rows}{cols}{door_row}{door_col}"

        # Create additional rooms with random sizes
        for _ in range(number_of_additional_rooms):
            if remaining_seed and len(remaining_seed) >= 4:
                # Extract dimensions and door location from the remaining seed
                rows = int(remaining_seed[:2]) // 10
                cols = int(remaining_seed[:2]) % 10
                door_row = int(remaining_seed[2:4]) // 10
                door_col = int(remaining_seed[2:4]) % 10
                remaining_seed = remaining_seed[4:]
            else:
                rows = random.randint(4, 7)
                cols = random.randint(4, 7)
                while True:
                    door_row = random.randint(1, rows - 2)
                    door_col = random.choice([0, cols - 1])
                    if not (door_row == 1 and door_col == 1):
                        break

            room = []
            for i in range(rows):
                if i == 0 or i == rows - 1:
                    # Top and bottom walls
                    room.append(["#"] * cols)
                else:
                    # Middle rows with walls on the sides
                    row = ["#"] + [" "] * (cols - 2) + ["#"]
                    room.append(row)

            # Add the door
            room[door_row][door_col] = "D"

            print(f"Debug: Created additional room with dimensions {rows}x{cols} and door at ({door_row}, {door_col})")
            rooms.append(room)

            # Append dimensions and door location of the room to the seed string
            seed_string += f"{rows}{cols}{door_row}{door_col}"

        print(f"Debug: Generated seed string for rooms: {seed_string}")
        return rooms, seed_string

    def play_room(game_map, player_row, player_col):
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
                if move == 'w':
                    if game_map[player_row - 1][player_col] == 'D':
                        print("You found the door! Moving to the next room...")
                        room_moves += 1
                        continue_game = False
                    elif game_map[player_row - 1][player_col] != '#':
                        delete_old_pos(player_row, player_col)
                        player_row -= 1
                        print_if_moved(move)
                        room_moves += 1

                elif move == 'd':
                    if game_map[player_row][player_col + 1] == 'D':
                        print("You found the door! Moving to the next room...")
                        room_moves += 1
                        continue_game = False
                    elif game_map[player_row][player_col + 1] != '#':
                        delete_old_pos(player_row, player_col)
                        player_col += 1
                        print_if_moved(move)
                        room_moves += 1

                elif move == 's':
                    if game_map[player_row + 1][player_col] == 'D':
                        print("You found the door! Moving to the next room...")
                        room_moves += 1
                        continue_game = False
                    elif game_map[player_row + 1][player_col] != '#':
                        delete_old_pos(player_row, player_col)
                        player_row += 1
                        print_if_moved(move)
                        room_moves += 1

                elif move == 'a':
                    if game_map[player_row][player_col - 1] == 'D':
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
        return room_moves



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
        room_moves_value = play_room(game_map, 1, 1)
        total_moves += room_moves_value
        rome_moves.append(room_moves_value)

        print(f"Moves in this room: {room_moves_value}")
        print(f"Total moves so far: {total_moves}")

    print("Congratulations! You've completed all rooms!")
    print(f"Total moves in all rooms: {total_moves}")
    print("Moves in each room:", rome_moves)
    print("Seed used for room generation:", seed_string)  # Display the seed string generated
    print("You can use this seed to recreate the same room layout in future games to try and get a higher score.")
    print("Thank you for playing!")

if __name__ == "__main__":
        main()
    