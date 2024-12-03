#!/usr/bin/python3

import random


def part1():
    """
    Part 1:

    Given a message and a map of characters, return the message found by replacing every character
    in the input string with the matching character in the map. Every character in the input string
    is guaranteed to have an entry in the characterMap, but the characterMap itself may have entries
    for unused characters.

    Example:
        replaceCharacters('abc', {'a': 'd', 'b': 'e', 'c': 'f'}) -> 'def'
        replaceCharacters('hello', {'h': 'p', 'e': 'i', 'l': 'z', 'o': 'a'}) -> 'pizza'
    """

    def replaceCharacters(inputString, characterMap):
        return "".join([characterMap[character] for character in inputString])

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    rot13Map = {alphabet[i]: alphabet[(i + 13) % 26] for i in range(26)}
    characterReplaceTests = [
        ["abc", {"a": "d", "b": "e", "c": "f"}, "def"],
        ["hello", {"h": "p", "e": "i", "l": "z", "o": "a"}, "pizza"],
        ["jrevqrngqnja", rot13Map, "werideatdawn"],
    ]

    for i, m, e in characterReplaceTests:
        print(f"{i} became {replaceCharacters(i,m)}. Expected {e}.")


def part2():
    """
    Part 2:

    Given a string, return whether that string is a pangram (a string that has every character in
    the english alphabet at least once). You may assume all characters are either letters or spaces
    and that all letters are lowercase.
    """

    def isPangram(inputString):
        return len(set("".join(inputString.split(" ")))) == 26

    # Examples of using the isPangram function.
    pangramTests = [
        ["abcdefghijklmnopqrstuvwxyz", True],
        ["the quick brown fox jumps over the lazy dog", True],
        ["this sentence is short", False],
    ]

    for pangramString, expectedBoolean in pangramTests:
        print(
            f'Got {isPangram(pangramString)}, expected {expectedBoolean} for the sentence "{pangramString}"'
        )


"""
Part 3: Implement the following game.

This game is played on a rectangular grid. At the beginning of the game, each space on
the board is filled in with a random piece, chosen from a predefined set of possible
types of pieces. The player selects a location on the board where there are at least
two of the same type of piece adjacent to each other (vertically or horizontally), and
the selected piece and all connected pieces of the same type are removed from the board,
at which time pieces above them (if any) fall down to take their place.

For example, if the user selected the middle space of the following board:

x o x
o o o
x x x

the result would be this

x   x
x x x

since all the connected o's were removed. The user could then select any of the x's, and
the entire board would be cleared, since the x's are all connected.

On the following board, there are no legal moves, since there are no connected pieces of
the same type. At this point, the game is over:

o x o
x o x

The user gets points based on how many pieces he removes at a time. Each piece removed in
a single move is worth one more point than the last piece. So for example,

1 piece = 1 point
2 pieces = 1 + 2 = 3 points
3 pieces = 1 + 2 + 3 = 6 points

and so on. When there are no longer any legal moves, you deduct points for remaining pieces:

1 piece left = -1 point
2 pieces left = -1 - 2 = -3 points
3 pieces left = -1 - 2 - 3 = -6 points

and so on. When the game is over, you should display the final score to the user and exit.

A skeleton class for the game is already prepared for you. The board is a simple rectangular
array of integers indexing into the pieceTypes array, with 0 representing a blank space.
The play() function currently loops forever, asking the user for a move (it guarantees the
space entered is on the board), clearing the space they entered, and re-drawing the board.
You should replace this logic with the correct logic described above.

Time permitting, you may write a computer player that plays the game automatically, trying to get the
highest possible score.
"""


class Game:
    def __init__(self):
        self.pieceTypes = [" ", "o", "x", "$"]
        self.width = 8
        self.height = 8
        self.board = [
            [random.randrange(1, len(self.pieceTypes)) for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.score = 0

    def getMoveInput(self):
        try:
            a, b = input()
        except ValueError:
            print("Move format should be like: b4")
            return self.getMoveInput()
        else:
            col = max(min(ord(a) - ord("a"), self.width - 1), 0)
            row = max(min(ord(b) - ord("1"), self.height - 1), 0)
            return row, col

    def render(self):
        print("  " + " ".join(chr(ord("a") + i) for i in range(self.width)))
        for j in range(self.height):
            print(
                str(j + 1)
                + " "
                + " ".join(self.pieceTypes[self.board[j][i]] for i in range(self.width))
            )
        print("Current score: {}\n".format(self.score))

    # +==========+
    # TODO: Implement game logic.
    # A fully-working solution must do the following:
    def play(self):
        self.score = 0
        while self.playableBoard():
            self.render()

            row, col = self.getMoveInput()
            #   Check if the player's move is valid (i.e., the space is nonempty and has adjacent matches).
            selected_value = self.board[row][col]
            if (selected_value > 0):
                # Get set of adjacent values
                self.highlightOrthogonal(row, col)
                grouped_cells = []
                for row_iter in range(0, self.height):
                    for col_iter in range(0, self.width):
                        if self.board[row_iter][col_iter] == len(self.pieceTypes):
                            grouped_cells.append([row_iter, col_iter])
                # If the user selected a cell that has any identical adjacent values
                if len(grouped_cells) > 1:
                    # Add the points from selection to score
                    # Sort cells according to row, this prevents a bug with the gravity later on
                    grouped_cells.sort(key=lambda coordinates: coordinates[0])
                    self.score += self.scorePoints(len(grouped_cells))
                    # Remove all connected pieces of the same type on a valid move.
                    # Handle logic for making pieces fall when spaces below them are empty.
                    for cell in grouped_cells:
                        cell_row, cell_col = cell
                        self.board[cell_row][cell_col] = 0
                        for row_iter in range(cell_row, 0, -1):
                            self.board[row_iter][cell_col] = self.board[row_iter - 1][cell_col]
                        self.board[0][cell_col] = 0
                else:
                    self.board[row][col] = selected_value
                    
        #   End the game when there are no valid moves, and display the final score.
        
        remaining_pieces = 0
        for row in self.board:
            for value in row:
                if value > 0:
                    remaining_pieces += 1
                    
        penalty = self.scorePoints(remaining_pieces)

        self.score -= penalty
        # self.render()
        print(f"Final score: {self.score}")
        
            
    def playableBoard(self):
        for row in range(0, self.height):
            for col in range(0, self.width - 1):
                if self.board[row][col] > 0:
                    if self.board[row][col] == self.board[row][col + 1]:
                        return True
                    
        for col in range(0, self.width):
            for row in range(0, self.height - 1):
                if self.board[row][col] > 0:
                    if self.board[row][col] == self.board[row + 1][col]:
                        return True
        
        return False
            
    def highlightOrthogonal(self, row, col):
        # len(self.pieceTypes) will be 1 greate than the max valid value in the board, thus it is highlighted
        if self.board[row][col] != len(self.pieceTypes):
            original = self.board[row][col]
            self.board[row][col] = len(self.pieceTypes)
            for cell_offset in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
                row_offset, col_offset = cell_offset
                adjacent_row = row + row_offset
                if adjacent_row >= 0 and adjacent_row < self.height:
                    adjacent_col = col + col_offset
                    if adjacent_col >= 0 and adjacent_col < self.width:
                        if self.board[adjacent_row][adjacent_col] == original:
                            self.highlightOrthogonal(adjacent_row, adjacent_col)
            
    def scorePoints(self, piece_count):
        if piece_count > 1:
            return piece_count + self.scorePoints(piece_count - 1)
        return piece_count


if __name__ == "__main__":
    print("Part 1")
    print("------")
    part1()
    print("")

    print("Part 2")
    print("------")
    part2()
    print("")

    print("Part 3:")
    Game().play()
