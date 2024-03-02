import Game
import Ship

if __name__ == "__main__":
    game_over = False
    game = Game()

    while not game_over:
        print("Welcome to Battleship!")
        names = {1:"Carrier (5 cells)", 2:"Battleship (4 cells)", 3:"Cruiser (3 cells)", 4:"Submarine (3 cells)", 5:"Destroyer (2 cells)"}

        # Add all ships to board:
        for ship_type in range(1,6):
            orientation = ""

            flag = 0 # Will be stuck in while loop if input is no good.
            while not flag:
                orientation = input(f"Input {names[ship_type]} Orientation (H/V): ")
                if orientation == "H":
                    flag = 1
                elif orientation == "V":
                    flag = 2
        
                coord = ""
                if flag == 0:
                    continue
                elif flag == 1:
                    coord = input("Input Leftmost Coordinate (x,y): ")
                else:
                    coord = input("Input Topmost Coordinate (x,y): ")
                splitstring = coord.split(",")
                x = int(splitstring[0][1:])
                y = int(splitstring[1][:-1])

                new_ship = Ship(ship_type, orientation, (x,y))

                if new_ship.add_ship() and game.addShip(new_ship):
                    print(f"You have added a {names[ship_type]} at coordinates ({x},{y}) at orientation {orientation}")
                    game.toString
                else:
                    print("Invalid input, try again:")
                    flag = 0
                    game.toString
            
