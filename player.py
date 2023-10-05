import random


class Player:
    def __init__(self, name):
        self.name = name
        self.board = [[None for _ in range(10)] for _ in range(10)]
        self.hit_board = [['-' for _ in range(10)] for _ in range(10)]
        self.ships = []
        self.shots = set()

    def place_ship(self, ship, x, y, horizontal):
        x = ord(x) - ord('A')
        y = y - 1
        for i in range(ship.size):
            if horizontal:
                self.board[x][y + i] = ship
            else:
                self.board[x + i][y] = ship
        ship.location = (x, y, horizontal)
        self.ships.append(ship)

    def can_place_ship(self, ship, x, y, horizontal):
        if not ('A' <= x <= 'J') or not (1 <= int(y) <= 10):
            return False

        x = ord(x) - ord('A')
        y = int(y) - 1

        if horizontal and y + ship.size > 10:
            return False
        if not horizontal and x + ship.size > 10:
            return False
        for i in range(ship.size):
            if horizontal and self.board[x][y + i] is not None:
                return False
            if not horizontal and self.board[x + i][y] is not None:
                return False
        return True

    def take_turn(self, opponent):
        print(f"{self.name}'s board:")
        self.print_board()
        print(f"{opponent.name}'s board:")
        opponent.print_board(hidden=True)
        while True:
            move = input("Enter coordinates to fire at (ex. A5): ").upper()
            if not self.is_valid_move(move):
                print("Invalid coordinates. Try again.")
                continue
            x = ord(move[0]) - ord('A')
            y = int(move[1:]) - 1
            if (x, y) in self.shots:
                print("You have already fired at this coordinate. Try again.")
                continue
            self.shots.add((x, y))
            if opponent.board[x][y] is not None:
                print("Hit!")
                idx = y - opponent.board[x][y].location[1] if opponent.board[x][y].location[2] else x - opponent.board[x][y].location[0]
                if opponent.board[x][y].hit(idx):
                    print(f"{opponent.board[x][y].name} sunk!")
                self.hit_board[x][y] = '*'
                return True
            else:
                print("Miss.")
                self.hit_board[x][y] = 'O'
                return False

    def is_valid_move(self, move):
        if len(move) < 2 or len(move) > 3:
            return False
        if not move[0].isalpha() or not move[1:].isdigit():
            return False
        x = ord(move[0]) - ord('A')
        y = int(move[1:]) - 1
        if x < 0 or x >= 10 or y < 0 or y >= 10:
            return False
        return True

    def print_board(self, hidden=False):
        print("  1 2 3 4 5 6 7 8 9 10")
        for i, row in enumerate(self.board):
            row_str = chr(ord('A') + i) + " "
            for j, cell in enumerate(row):  # Add enumerate for index access
                if cell is None:
                    row_str += f"{self.hit_board[i][j]} "
                elif hidden:
                    x_offset = i - cell.location[0]
                    y_offset = j - cell.location[1]
                    if 0 <= x_offset < cell.size and 0 <= y_offset < cell.size:
                        if cell.hits[x_offset] if not cell.location[2] else cell.hits[y_offset]:
                            row_str += "* "
                        else:
                            row_str += f"{self.hit_board[i][j]} "
                    else:
                        row_str += f"{self.hit_board[i][j]} "
                else:
                    row_str += f"{self.hit_board[i][j]} "
            print(row_str)

    def ships_left(self):
        return sum(1 for ship in self.ships if not ship.is_sunk())
