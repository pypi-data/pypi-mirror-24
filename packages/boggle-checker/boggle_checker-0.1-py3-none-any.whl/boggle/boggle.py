import random


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def boggle_checker(board, guess):
    '''  Given a 2D array which is a Boggle board, return True if the second arguement is a valid word
     on the Boggle board'''

    # Set the x, y coordinates to negative numbers for the first iteration of get_adj_positions
    x = -10
    y = -10
    curr_word = ""
    count = 0

    # to visualise the board and word we are looking for
    print(guess)
    for row in board:
        print(row)

    # if checkLetter comes back True the word is found and we return True.
    if checkLetter(get_adj_positions(x, y, len(board)), board, count, guess, curr_word):
        return True
    # Else the word isn't a legal word on this board so return False
    return False


def board_marker(board, x, y):
    """" Mark the position found with an x so it can't be checked twice """
    board[x][y] = "x"
    return board


def get_adj_positions(x, y, max):
    """" Return all legal positions adjoining the x, y coordinate given or return all positions
    if it is the first time being called """

    adj_pos = []
    if (x == -10) or (y == -10):
        x = 0
        y = 0
        for x, y in [(x + i, y + j) for i in range(0, max) for j in range(0, max)]:
            adj_pos.append([x, y])

        return adj_pos
    else:
        # Generate all coordinates of all squares surrounding given position
        for x, y in [(x + i, y + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            adj_pos.append([x, y])
        # Remove any coordinates that are not on the board
        adj_pos = list(filter(lambda x_y: -1 < x_y[0] < max and -1 < x_y[1] < max, adj_pos))

        return adj_pos


def checkLetter(position, board, count, guess, curr_word):
    """ Once all adjacent tiles are located, this checks to see if any of them tiles contain the next letter we need.
    If the next letter exists in the adjacent tiles, but that isn't the end of the word then the function is called again """

    # check each adjacent tile
    for item in position:
        x = item[0]
        y = item[1]
        if board[x][y] == guess[count]:
            # add the letter found to our current word variable
            curr_word += guess[count]
            if count + 1 < len(guess):
                # call this function again with updated variables
                return checkLetter(get_adj_positions(x, y, len(board)), board_marker(board, x, y), count+1, guess, curr_word)
            else:
                # word is found, return True to exit function
                print(curr_word)
                return True


def board_generate():
    """" Random board generator for testing purposes"""

    board_size = random.randint(3, 7)
    board = [[alphabet[random.randint(0, 25)] for a in range(board_size)] for b in range(board_size)]
    return(board)


def guess_generate():
    """" Generate a random string for testing purposes"""

    guess = ""
    length = random.randint(2,3)
    for i in range(length):
        guess += alphabet[random.randint(0, 25)]
    return guess






