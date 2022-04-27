from scipy.special import comb
import time
import sys
import ast
COND_EXAMPLE = [[[1, 1], [3],[5],[1, 1],[2]],[[3],[2],[3, 1],[1,1],[1, 2]]]
UNKNOWN = -1  # Unknown cell in presented with -1
BLACK = 1  # Black cell is presented with 1
WHITE = 0  # White cell is presented with 0


def delete_dup(lst):
    """
    deletes all duplicates from list
    :param lst: the list changed
    :type lst: list
    :return: new list without duplicates
    :rtype list
    """
    # I used this func instead of list(set(lst)) of list(dict.fromkeys(lst))
    #  because they cant handle lists in them
    new_lst = []
    for var in lst:
        if not var in new_lst:
            new_lst.append(var)
    return new_lst


def count_row_variations(length, blocks):
    """
    the func counts all the possibilities to paint a row with the length cells
    :param length: the rows length
    :type length: int
    :param blocks: the conditions on the row
    :type blocks: list
    :return: number of options to paint
    :rtype: int
    """
    # the logic is to create a unit from every block and count in how many places
    # they can be placed in the line in the order
    num_of_units = len(blocks)
    units_length = sum(blocks)
    new_length = length - units_length + 1  # the +1 is because the new length is supposed to be
    #  length - units_length + num_of_units, but there are seperators between them. num of seperators:
    #  num_of_units - 1.
    #  put together: n - (n-1) = 1

    return int(comb(new_length, num_of_units))


def get_row_variations(row, blocks):
    """
    the function gets all the options to paint a row to match the blocks
    :param row: the starting row
    :type row: list
    :param blocks: the conditions on the row
    :type blocks: list
    :return: all the paint options
    :rtype: list
    """
    return help_get_row_variations(row, blocks, [], count_row_variations(len(row), blocks))


def help_get_row_variations(row, blocks, answers, max_options):
    """
    gets all the options to paint a line
    :param row: the line
    :type row: list
    :param blocks: the condition for the line
    :type blocks: list
    :param answers: all the possible answers in the beggining
    :type answers: list
    :param max_options: the max num of options to paint that is supposed
                to be the len of the end list
    :type max_options: int
    :return: all the possible answers to paint the line.
    :rtype: list
    """
    if len(delete_dup(answers)) == max_options:
        return delete_dup(answers)

    new_ans = []
    if is_solved(row, blocks):  # checks if the row fits to the condition
        answers.append(row)
        return [row]

    for i in range(len(row)):
        if row[i] == UNKNOWN:
            if row.count(BLACK) <= sum(blocks):
                new_row = [row[j] for j in range(0, i)] + [BLACK] + [row[j] for j in range(i + 1, len(row))]
                [new_ans.append(j) for j in help_get_row_variations(new_row, blocks, answers, max_options)
                 if not j in new_ans or j == []]

            new_row = [row[j] for j in range(0, i)] + [WHITE] + [row[j] for j in range(i + 1, len(row))]
            [new_ans.append(j) for j in help_get_row_variations(new_row, blocks, answers, max_options)
             if not j in new_ans and j != []]

    return new_ans


def is_solved(row, blocks):
    """
    checks if the row stands in the conditions of blocks
    :param row: the row checked
    :type row: list
    :param blocks: the conditions
    :type blocks: list
    :return: does the row stands in the conditions
    :rtype: bool
    """

    if UNKNOWN in row:
        return False

    tot = 0
    place = 0
    new_row = row + [0]
    if new_row[0]:  # the for starts from one, so if the row starts
        tot += 1  # with 0 it wont be counted as a block, but, you have to check the first

    for i in range(1, len(new_row)):
        if not new_row[i] and new_row[i - 1]:
            if place >= len(blocks) or tot != blocks[place]:
                return False
            tot = 0
            place += 1
        elif new_row[i]:
            tot += 1
    if not BLACK in row and blocks == [0]:
        place += 1
    return place == len(blocks)


"""
if some of the cells are unknown and some of them 
are one colored, I chose to leave them unknown because:

if we assume that one ceil is in the colour of the others, but in the end, it turns to be the opposite colour, 
we would have to change back the colour and go a few steps back.
I think it would be faster to fix the colour when you know it and you wont have to fix it later. 
"""


def get_intersection_row(rows):
    """
    the function finds the intersection of all rows given and returns a list of it:
    return[i] = intersection of i column in rows
    :param rows: the rows given
    :type rows: list of lists of int
    :return: the intersection
    :rtype: list of int
    """
    inter_row = [i for i in rows[0]]
    for col in range(len(rows[0])):
        for line in range(0, len(rows)):
            if rows[line][col] != rows[line - 1][col]:
                inter_row[col] = UNKNOWN
    return inter_row


def get_intersection_board(row_board, col_board):
    """
    get the intersection of the boards list given by the rules down to a new board
    :param row_board: the first board, of rows
    :type row_board: list
    :param col_board: the second board, of columns
    :type col_board: list
    :return: a new board, and is the board possible
    :rtype: tuple of list and bool
    """
    # (1 + 0 -> X) / (1 + -1 -> 1) / (0 + -1 -> 0) / (1 + 1 ->1) / (0 + 0 -> 0) / (-1 + -1 -> -1)
    # X means a mistake
    new_board = []
    is_possible = True  # is_possible says if the board is possible
    for line in range(len(row_board)):
        new_board.append([])
        for cell in range(len(row_board[line])):
            if row_board[line][cell] == BLACK:
                new_board[-1].append(BLACK)
                if col_board[line][cell] == WHITE:
                    is_possible = False
                    break
            elif row_board[line][cell] == WHITE:
                new_board[-1].append(WHITE)
                if col_board[line][cell] == BLACK:
                    is_possible = False
                    break
            else:
                new_board[-1].append(col_board[line][cell])

    return new_board, is_possible


def rotate(board):
    """
    the function rotates the board counterclockwise
    :param board: the board to rotate
    :type board: list of lists of chars
    :return: a rotated board
    :rtype: list of lists of chars
    """
    return [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]





def help_solve_easy_nonogram(constraints, board):
    """
    the reursive func to solve a simple board
    :param constraints: the conditions of the board
    :type constraints: list
    :param board: the board checked
    :type board: list
    :return: a new board, solved as much as possible or None if impossible
    :rtype: list or None
    """
    row_board = []
    col_board = []

    for line in range(len(constraints[0])):
        if constraints[0][line] == []:
            rows = []
            for i in board[0]:
                rows.append(WHITE)
            row_board.append(rows)
        elif len(constraints[0][line]) == 1 and constraints[0][line][0] == len(board[0]):
            rows = []
            for i in board[0]:
                rows.append(BLACK)
            row_board.append(rows)
        else:
            rows = get_row_variations(board[line], constraints[0][line])
            if rows == []:
                return  # that means the row in impossible
            else:
                row_board.append(get_intersection_row(rows))
    for col in range(len(constraints[1])):
        if constraints[1][col] == []:
            cols = []
            for i in board:
                cols.append(WHITE)
            col_board.append(cols)
        elif len(constraints[1][col]) == 1 and constraints[1][col][0] == len(board):
            cols = []
            for i in board:
                cols.append(BLACK)
            col_board.append(cols)
        else:
            cols = get_row_variations([line[col] for line in board], constraints[1][col])
            if cols == []:
                return  # that means the col is impossible
            col_board.append(get_intersection_row(cols))
    new_board, is_poss = get_intersection_board(row_board, rotate(col_board))
    if not is_poss:
        return


    if easy_solved(new_board, constraints):
        return new_board
    if new_board == None:
        return
    if new_board == board:
        return new_board
    return help_solve_easy_nonogram(constraints, new_board)



def solve_easy_nonogram(constraints):
    """
    creates a new board of UNKNOWNs and sends it to recursive help func
    :param constraints: the conditions of the board
    :type constraints: list
    :return: the new board solved as much as possible or None if impossible
    :rtype: 2d list of ints
    """
    board = []
    for i in range(len(constraints[0])):  # this part creates a new board
        board.append([])  # in the required lengths of UNKNOWNs to send to the help func
        for i in range(len(constraints[1])):
            board[-1].append(UNKNOWN)

    return help_solve_easy_nonogram(constraints, board)


def easy_solved(board, blocks):
    """
    checks if the board is solved, which means it has no
     unknown and all lines and cols fit to conditions
    :param board: the board checked
    :type board: list
    :param blocks: the conditions
    :type blocks: list
    :return: is the board solved
    :rtype: bool
    """
    lines = blocks[0]
    cols = blocks[1]
    for line in range(len(board)):
        if UNKNOWN in board[line] or not is_solved(board[line], lines[line]):
            return False

    for col in range(len(board[0])):
        if not is_solved([line[col] for line in board], cols[col]):
            return False

    return True


def help_solve_nonogram(constraints, board, answers):
    """
    help func to solve nonogram game
    :param constraints: the conditions on the board
    :type constraints: list
    :param board: the max solved board by help_solve_easy_nonogram
    :type board: list
    :param answers: the possible answers
    :type answers: list
    :return: all the possibilities to solve
    :rtype: list
    """
    board = help_solve_easy_nonogram(constraints, board)
    if board == None:
        return []
    if easy_solved(board, constraints):
        return answers + [board]

    new_answers = []
    for line in range(len(board)):
        for cell in range(len(board[line])):
            if board[line][cell] == UNKNOWN:
                new_board = board[0:line] + [board[line][0:cell] + [BLACK] + board[line][cell + 1:]] + board[line + 1:]
                [new_answers.append(option) for option in help_solve_nonogram(constraints, new_board, answers)
                 if option != [] and not option in new_answers]
                new_board = board[0:line] + [board[line][0:cell] + [WHITE] + board[line][cell + 1:]] + board[line + 1:]
                [new_answers.append(option) for option in help_solve_nonogram(constraints, new_board, answers)
                 if option != [] and not option in new_answers]

    return new_answers


def solve_nonogram(constraints):
    """
    solves the nonogram game
    :param constraints: the conditions on the board
    :type constraints: list
    :return: all the possible solutions
    :rtype: list
    """
    solution = solve_easy_nonogram(constraints)
    if solution is None:
        return []
    elif easy_solved(solution, constraints):
        return [solution]
    else:  # the board isn't totally solved
        return help_solve_nonogram(constraints, solution, [])


def print_board(board):
    """
    debugging func to print boards
    :param board: the board printed
    :type board: list of lists of ints
    """

    for line in board:
        for cell in line:
            if cell == UNKNOWN:
                print(cell, end="  ")
            else:
                print("", cell, end="  ")
        print()
    print("**************")


if __name__ == "__main__":
    cond = COND_EXAMPLE
    if len(sys.argv) == 2:
        cond = ast.literal_eval(sys.argv[1])

    res = solve_nonogram(cond)
    print("there {} {} optinal sulotions".format("is" if len(res) == 1 else "are", len(res)))
    for i in res:
        print_board(i)
