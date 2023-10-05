from player import Player
from ship import Ship
import os

class Battleship:
    def __init__(self):
        pass

    def play_battleship(self):
        player1 = Player("Player 1")
        player2 = Player("Player 2")

        self.place_ships(player1)
        self.clear_screen()
        self.place_ships(player2)
        self.clear_screen()
        
        current_player = player1
        while True:
            self.clear_screen()
            other_player = player2 if current_player == player1 else player1
            print(f"{current_player.name}'s turn.")
            hit = current_player.take_turn(other_player)
            if hit and other_player.ships_left() == 0:
                print(f"{current_player.name} wins!")
                break
            current_player, other_player = other_player, current_player

    def place_ships(self, player):
        for name, size in [("Destroyer", 2), ("Submarine", 3), ("Battleship", 4), ("Aircraft Carrier", 5)]:
            ship = Ship(name, size)
            while True:
                self.clear_screen()
                print(f"{player.name}, place your {name} ({size} spaces).")
                player.print_board()

                coords = input("Enter starting coordinates (ex. D6): ")
                if len(coords) < 2 or not coords[0].isalpha() or not coords[1:].isdigit():
                    print("Invalid coordinates. Try again.")
                    continue
                x = coords[0].upper()
                y = int(coords[1:])
                if not ('A' <= x <= 'J') or not (1 <= y <= 10):
                    print("Invalid coordinates. Try again.")
                    continue

                h = input("Horizontal? (y/n): ").lower()
                while h not in ['y', 'n']:
                    h = input("Invalid input. Horizontal? (y/n): ").lower()
                horizontal = h == 'y'

                if player.can_place_ship(ship, x, y, horizontal):
                    player.place_ship(ship, x, y, horizontal)
                    break
                else:
                    print("Invalid location. Try again.")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
