#initialization
import pygame
import time
pygame.init()
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Chess")
font = pygame.font.Font('freesansbold.ttf', 20)
timer = pygame.time.Clock()
fps = 60

# game variables and images
A = True
B = True
C = True
D = True
MOVE1 = True
MOVE2 = True

white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

white_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
white_options = []
black_options = []
captured_pieces_white = []
captured_pieces_black = []
white_ep = (100, 100)
black_ep = (100, 100)

white_promotions = ["bishop", "knight", "rook", "queen"]
black_promotions = ["bishop", "knight", "rook", "queen"]
# 0 - whites turn, no selection: 1 - whites turn, piece selected: 2 - black turn, no selection: 3 - black turn, piece selected
turn_step = 0
selection = 100
valid_moves = []
# load in game piece images (queen, king, rook, bishop, knight, pawn)
black_queen = pygame.image.load('assets/black_queen.png')
black_queen = pygame.transform.scale(black_queen, (90, 90))

black_king = pygame.image.load('assets/black_king.png')
black_king = pygame.transform.scale(black_king, (90, 90))

black_knight = pygame.image.load('assets/black_knight.png')
black_knight = pygame.transform.scale(black_knight, (90, 90))

black_bishop = pygame.image.load('assets/black_bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (90, 90))

black_rook = pygame.image.load('assets/black_rook.png')
black_rook = pygame.transform.scale(black_rook, (90, 90))

black_pawn = pygame.image.load('assets/black_pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (90, 90))

white_queen = pygame.image.load('assets/white_queen.png')
white_queen = pygame.transform.scale(white_queen, (90, 90))

white_king = pygame.image.load('assets/white_king.png')
white_king = pygame.transform.scale(white_king, (90, 90))

white_knight = pygame.image.load('assets/white_knight.png')
white_knight = pygame.transform.scale(white_knight, (90, 90))

white_bishop = pygame.image.load('assets/white_bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (90, 90))

white_rook = pygame.image.load('assets/white_rook.png')
white_rook = pygame.transform.scale(white_rook, (90, 90))

white_pawn = pygame.image.load('assets/white_pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (90, 90))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]

black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]

# this corresponds to the white_images/black_images indexes
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# time settings
initial_time = 10 * 60  # 10 minutes in seconds
white_time = black_time = initial_time


def display_time(white_time, black_time):
    white_time_str = format_time(white_time)
    black_time_str = format_time(black_time)

    white_text = font.render(white_time_str, True, (255, 255, 255))
    black_text = font.render(black_time_str, True, (255, 255, 255))

    # Display white's time at the top and black's time at the bottom
    screen.blit(white_text, (WIDTH - 140, HEIGHT - 40))
    screen.blit(black_text, (WIDTH - 140, 20))


def format_time(total_seconds):
    hours = int(total_seconds / 3600)
    minutes = int((total_seconds % 3600) / 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# draw main game board
def draw_board():
    for i in range(64):
        column = i % 8
        row = i // 8
        if row % 2 == 0:
            if column % 2 == 0:
                pygame.draw.rect(screen, 'dark green', [700 - (column * 100), row * 100, 100, 100])
            else:
                pygame.draw.rect(screen, 'white', [700 - (column * 100), row * 100, 100, 100])
        else:
            if column % 2 == 0:
                pygame.draw.rect(screen, 'white', [700 - (column * 100), row * 100, 100, 100])
            else:
                pygame.draw.rect(screen, 'dark green', [700 - (column * 100), row * 100, 100, 100])

# draw pieces on board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 5, white_locations[i][1] * 100 + 10))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 5, white_locations[i][1] * 100 + 5))

        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100, white_locations[i][1] * 100, 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100+5, black_locations[i][1] * 100+10))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100+5, black_locations[i][1] * 100+5))

        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100, black_locations[i][1] * 100, 100, 100],
                                 2)


# check and return an all moves list
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []

    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)

        all_moves_list.append(moves_list)

    return all_moves_list


# check function
def in_check(color):
    if color == 'white':
        king_position = white_locations[white_pieces.index('king')]
        enemies_options = black_options
        enemies_pieces = black_pieces
        enemies_locations = black_locations
    else:
        king_position = black_locations[black_pieces.index('king')]
        enemies_options = white_options
        enemies_pieces = white_pieces
        enemies_locations = white_locations

    attacking_piece = 0

    for i, moves in enumerate(enemies_options):
        if king_position in moves:
            attacking_piece = i

            # list of positions between attacking piece and king
            attacking_positions = []
            attacking_location = enemies_locations[attacking_piece]

            if enemies_pieces[attacking_piece] == 'bishop':
                if king_position[0] > attacking_location[0]:  # king to the right of bishop
                    if king_position[1] > attacking_location[1]:  # king is below bishop
                        x, y = attacking_location[0] + 1, attacking_location[1] + 1
                        while (x, y) != king_position:
                            attacking_positions.append((x, y))
                            x += 1
                            y += 1
                    else:  # king is above bishop
                        x, y = attacking_location[0] + 1, attacking_location[1] - 1
                        while (x, y) != king_position:
                            attacking_positions.append((x, y))
                            x += 1
                            y -= 1

                else:  # king to the left of bishop
                    if king_position[1] > attacking_location[1]:  # king is below bishop
                        x, y = attacking_location[0] - 1, attacking_location[1] + 1
                        while (x, y) != king_position:
                            attacking_positions.append((x, y))
                            x -= 1
                            y += 1
                    else:  # king is above bishop
                        x, y = attacking_location[0] - 1, attacking_location[1] - 1
                        while (x, y) != king_position:
                            attacking_positions.append((x, y))
                            x -= 1
                            y -= 1

            elif enemies_pieces[attacking_piece] == 'rook':
                if king_position[0] > attacking_location[0]:  # king is to the right of rook
                    x, y = attacking_location[0] + 1, attacking_location[1]
                    while (x, y) != king_position:
                        attacking_positions.append((x, y))
                        x += 1

                elif king_position[0] < attacking_location[0]:  # king is to the left of rook
                    x, y = attacking_location[0] - 1, attacking_location[1]
                    while (x, y) != king_position:
                        attacking_positions.append((x, y))
                        x -= 1

                elif king_position[1] > attacking_location[1]:  # king is below rook
                    x, y = attacking_location[0], attacking_location[1] + 1
                    while (x, y) != king_position:
                        attacking_positions.append((x, y))
                        y += 1

                else:  # king is above rook
                    x, y = attacking_location[0], attacking_location[1] - 1
                    while (x, y) != king_position:
                        attacking_positions.append((x, y))
                        y -= 1

            elif enemies_pieces[attacking_piece] == 'knight':
                attacking_positions.append(attacking_location)

            elif enemies_pieces[attacking_piece] == 'pawn':
                attacking_positions.append(attacking_location)

            elif enemies_pieces[attacking_piece] == 'queen':
                if king_position[0] > attacking_location[0]:  # king to the right of queen
                    if king_position[1] > attacking_location[1]:  # king is right/below queen
                        x, y = attacking_location[0] + 1, attacking_location[1] + 1
                        while (x, y) != king_position:
                            attacking_positions.append((x, y))
                            x += 1
                            y += 1
                    elif king_position[1] < attacking_location[1]:  # king is right/above queen
                        x, y = attacking_location[0] + 1, attacking_location[1] - 1
                        while (x, y) != king_position:
                            attacking_positions.append((x, y))
                            x += 1
                            y -= 1
                    else:  # king is directly right of queen
                        x, y = attacking_location[0] + 1, attacking_location[1]
                        while (x, y) != king_position:
                            attacking_positions.append((x, y))
                            x += 1


                elif king_position[0] < attacking_location[0]:  # king to the left of queen
                    if king_position[1] > attacking_location[1]:  # king is left/below queen
                        x, y = attacking_location[0] - 1, attacking_location[1] + 1
                        while (x, y) != king_position:
                            attacking_positions.append((x, y))
                            x -= 1
                            y += 1
                    elif king_position[1] < attacking_location[1]:  # king is left/above queen
                        x, y = attacking_location[0] - 1, attacking_location[1] - 1
                        while (x, y) != king_position:
                            attacking_positions.append((x, y))
                            x -= 1
                            y -= 1
                    else:  # king is directly left of queen
                        x, y = attacking_location[0] - 1, attacking_location[1]
                        while (x, y) != king_position:
                            attacking_positions.append((x, y))
                            x -= 1

                else:
                    if king_position[1] > attacking_location[1]:  # king is below queen
                        x, y = attacking_location[0], attacking_location[1] + 1
                        while (x, y) != king_position:
                            attacking_positions.append((x, y))
                            y += 1
                    else:  # king is above queen
                        x, y = attacking_location[0], attacking_location[1] - 1
                        while (x, y) != king_position:
                            attacking_positions.append((x, y))
                            y -= 1

            return [True, attacking_piece, attacking_positions]

    return [False, None]


# checkmate function
def in_checkmate(color):
    if in_check(color)[0] == True:
        if color == 'white':
            count = 0
            for piece in white_options:
                if len(piece) != 0:
                    count = 1
            if count == 0:
                return True
            else:
                return False
        else:
            count = 0
            for piece in black_options:
                if len(piece) != 0:
                    count = 1
            if count == 0:
                return True
            else:
                return False
    else:
        return False


# checks if the king is within one square of enemy king
def near_enemy_king(king_position, color):
    targets = [(0, 1), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1)]

    if color == 'white':
        enemy_king_location = black_locations[black_pieces.index('king')]
    else:
        enemy_king_location = white_locations[white_pieces.index('king')]

    for i in range(8):
        if (king_position[0] + targets[i][0], king_position[1] + targets[i][1]) == enemy_king_location:
            return True

    return False


# checks if king is about to moves into attacking pawn location
def near_enemy_pawn(king_position, color):
    if color == 'white':
        for i in range(len(black_pieces)):
            if black_pieces[i] == 'pawn':
                if king_position == (black_locations[i][0] + 1, black_locations[i][1] + 1) or \
                        king_position == (black_locations[i][0] - 1, black_locations[i][1] + 1):
                    return True

        return False
    else:
        for i in range(len(white_pieces)):
            if white_pieces[i] == 'pawn':
                if king_position == (white_locations[i][0] + 1, white_locations[i][1] - 1) or \
                        king_position == (white_locations[i][0] - 1, white_locations[i][1] - 1):
                    return True

        return False


# checks if the rook is protecting the checking piece
def near_enemy_rook(king_position, color):
    moves_list = []
    if color == 'white':
        allies_locations = white_locations
        enemies_locations = black_locations
        enemies_pieces = black_pieces

    else:
        allies_locations = black_locations
        enemies_locations = white_locations
        enemies_pieces = white_pieces

    for k in range(len(enemies_pieces)):
        if enemies_pieces[k] == 'rook':
            position = enemies_locations[k]
            for i in range(4):  # up, down, right, left
                if i == 0:  # up
                    for j in range(1, 8):
                        if (position[0], position[1] - j) not in allies_locations and (position[1] - j) > -1:
                            if (position[0], position[1] - j) not in enemies_locations:
                                moves_list.append((position[0], position[1] - j))
                            else:
                                moves_list.append((position[0], position[1] - j))
                                break
                        elif (position[0], position[1] - j) in allies_locations:
                            moves_list.append((position[0], position[1] - j))
                            break
                        else:
                            break
                elif i == 1:  # down
                    for j in range(1, 8):
                        if (position[0], position[1] + j) not in allies_locations and (position[1] + j) < 8:
                            if (position[0], position[1] + j) not in enemies_locations:
                                moves_list.append((position[0], position[1] + j))
                            else:
                                moves_list.append((position[0], position[1] + j))
                                break
                        elif (position[0], position[1] + j) in allies_locations:
                            moves_list.append((position[0], position[1] + j))
                            break
                        else:
                            break
                elif i == 2:  # right
                    for j in range(1, 8):
                        if (position[0] + j, position[1]) not in allies_locations and (position[0] + j) < 8:
                            if (position[0] + j, position[1]) not in enemies_locations:
                                moves_list.append((position[0] + j, position[1]))
                            else:
                                moves_list.append((position[0] + j, position[1]))
                                break
                        elif (position[0] + j, position[1]) in allies_locations:
                            moves_list.append((position[0] + j, position[1]))
                            break
                        else:
                            break
                else:  # left
                    for j in range(1, 8):
                        if (position[0] - j, position[1]) not in allies_locations and (position[0] - j) > -1:
                            if (position[0] - j, position[1]) not in enemies_locations:
                                moves_list.append((position[0] - j, position[1]))
                            else:
                                moves_list.append((position[0] - j, position[1]))
                                break
                        elif (position[0] - j, position[1]) in allies_locations:
                            moves_list.append((position[0] - j, position[1]))
                            break
                        else:
                            break
    if king_position in moves_list:
        return True
    else:
        return False


# checks if the bishop is protecting the checking piece
def near_enemy_bishop(king_position, color):
    moves_list = []
    if color == 'white':
        allies_locations = white_locations
        enemies_locations = black_locations
        enemies_pieces = black_pieces
    else:
        allies_locations = black_locations
        enemies_locations = white_locations
        enemies_pieces = white_pieces

    for k in range(len(enemies_pieces)):
        if enemies_pieces[k] == 'bishop':
            position = enemies_locations[k]
            for i in range(4):  # diagonals
                if i == 0:  # top-right
                    for j in range(1, 8):
                        if (position[0] + j, position[1] - j) not in allies_locations and \
                                (position[0] + j) < 8 and (position[1] - j) > -1:
                            if (position[0] + j, position[1] - j) not in enemies_locations:
                                moves_list.append((position[0] + j, position[1] - j))
                            else:
                                moves_list.append((position[0] + j, position[1] - j))
                                break
                        elif (position[0] + j, position[1] - j) in allies_locations:
                            moves_list.append((position[0] + j, position[1] - j))
                            break
                        else:
                            break
                if i == 1:  # top-left
                    for j in range(1, 8):
                        if (position[0] - j, position[1] - j) not in allies_locations and \
                                (position[0] - j) > -1 and (position[1] - j) > -1:
                            if (position[0] - j, position[1] - j) not in enemies_locations:
                                moves_list.append((position[0] - j, position[1] - j))
                            else:
                                moves_list.append((position[0] - j, position[1] - j))
                                break
                        elif (position[0] - j, position[1] - j) in allies_locations:
                            moves_list.append((position[0] - j, position[1] - j))
                            break
                        else:
                            break
                if i == 2:  # bottom-right
                    for j in range(1, 8):
                        if (position[0] + j, position[1] + j) not in allies_locations and \
                                (position[0] + j) < 8 and (position[1] + j) < 8:
                            if (position[0] + j, position[1] + j) not in enemies_locations:
                                moves_list.append((position[0] + j, position[1] + j))
                            else:
                                moves_list.append((position[0] + j, position[1] + j))
                                break
                        elif (position[0] + j, position[1] + j) in allies_locations:
                            moves_list.append((position[0] + j, position[1] + j))
                            break
                        else:
                            break
                else:  # bottom-left
                    for j in range(1, 8):
                        if (position[0] - j, position[1] + j) not in allies_locations and \
                                (position[0] - j) > -1 and (position[1] + j) < 8:
                            if (position[0] - j, position[1] + j) not in enemies_locations:
                                moves_list.append((position[0] - j, position[1] + j))
                            else:
                                moves_list.append((position[0] - j, position[1] + j))
                                break
                        elif (position[0] - j, position[1] + j) in allies_locations:
                            moves_list.append((position[0] - j, position[1] + j))
                            break
                        else:
                            break

    if king_position in moves_list:
        return True
    else:
        return False


# checks if the knight is protecting the checking piece
def near_enemy_knight(king_position, color):
    moves_list = []
    if color == 'white':
        allies_locations = white_locations
        enemies_locations = black_locations
        enemies_options = black_options
        enemies_pieces = black_pieces
    else:
        allies_locations = black_locations
        enemies_locations = white_locations
        enemies_options = white_options
        enemies_pieces = white_pieces

    for i in range(len(enemies_pieces)):
        if enemies_pieces[i] == 'knight':
            position = enemies_locations[i]

            # Top-right up
            if (position[0] + 1) < 8 and (position[1] - 2) > -1:
                moves_list.append((position[0] + 1, position[1] - 2))
            # Top-right down
            if (position[0] + 2) < 8 and (position[1] - 1) > -1:
                moves_list.append((position[0] + 2, position[1] - 1))
            # Bottom-right up
            if (position[0] + 2) < 8 and (position[1] + 1) < 8:
                moves_list.append((position[0] + 2, position[1] + 1))
            # Bottom-right down
            if (position[0] + 1) < 8 and (position[1] + 2) < 8:
                moves_list.append((position[0] + 1, position[1] + 2))
            # Top-left up
            if (position[0] - 1) > -1 and (position[1] - 2) > -1:
                moves_list.append((position[0] - 1, position[1] - 2))
            # Top-left down
            if (position[0] - 2) > -1 and (position[1] - 2) > -1:
                moves_list.append((position[0] - 2, position[1] - 1))
            # Bottom-left up
            if (position[0] - 2) > -1 and (position[1] + 1) < 8:
                moves_list.append((position[0] - 2, position[1] + 1))
            # Bottom-left down
            if (position[0] - 1) > -1 and (position[1] + 2) < 8:
                moves_list.append((position[0] - 1, position[1] + 2))

    if king_position in moves_list:
        return True
    else:
        return False


def near_enemy_queen(king_position, color):
    moves_list = []
    if color == 'white':
        enemies_pieces = black_pieces
        enemies_locations = black_locations
        allies_locations = white_locations
    else:
        enemies_pieces = white_pieces
        enemies_locations = white_locations
        allies_locations = black_locations

    for k in range(len(enemies_pieces)):
        if enemies_pieces[k] == 'queen':
            position = enemies_locations[k]
            for i in range(4):  # diagonals
                if i == 0:  # top-right
                    for j in range(1, 8):
                        if (position[0] + j, position[1] - j) not in allies_locations and \
                                (position[0] + j) < 8 and (position[1] - j) > -1:
                            if (position[0] + j, position[1] - j) not in enemies_locations:
                                moves_list.append((position[0] + j, position[1] - j))
                            else:
                                moves_list.append((position[0] + j, position[1] - j))
                                break
                        elif (position[0] + j, position[1] - j) in allies_locations:
                            moves_list.append((position[0] + j, position[1] - j))
                            break
                        else:
                            break
                if i == 1:  # top-left
                    for j in range(1, 8):
                        if (position[0] - j, position[1] - j) not in allies_locations and \
                                (position[0] - j) > -1 and (position[1] - j) > -1:
                            if (position[0] - j, position[1] - j) not in enemies_locations:
                                moves_list.append((position[0] - j, position[1] - j))
                            else:
                                moves_list.append((position[0] - j, position[1] - j))
                                break
                        elif (position[0] - j, position[1] - j) in allies_locations:
                            moves_list.append((position[0] - j, position[1] - j))
                            break
                        else:
                            break
                if i == 2:  # bottom-right
                    for j in range(1, 8):
                        if (position[0] + j, position[1] + j) not in allies_locations and \
                                (position[0] + j) < 8 and (position[1] + j) < 8:
                            if (position[0] + j, position[1] + j) not in enemies_locations:
                                moves_list.append((position[0] + j, position[1] + j))
                            else:
                                moves_list.append((position[0] + j, position[1] + j))
                                break
                        elif (position[0] + j, position[1] + j) in allies_locations:
                            moves_list.append((position[0] + j, position[1] + j))
                            break
                        else:
                            break
                else:  # bottom-left
                    for j in range(1, 8):
                        if (position[0] - j, position[1] + j) not in allies_locations and \
                                (position[0] - j) > -1 and (position[1] + j) < 8:
                            if (position[0] - j, position[1] + j) not in enemies_locations:
                                moves_list.append((position[0] - j, position[1] + j))
                            else:
                                moves_list.append((position[0] - j, position[1] + j))
                                break
                        elif (position[0] - j, position[1] + j) in allies_locations:
                            moves_list.append((position[0] - j, position[1] + j))
                            break
                        else:
                            break
            for i in range(4):  # up, down, right, left
                if i == 0:  # up
                    for j in range(1, 8):
                        if (position[0], position[1] - j) not in allies_locations and (position[1] - j) > -1:
                            if (position[0], position[1] - j) not in enemies_locations:
                                moves_list.append((position[0], position[1] - j))
                            else:
                                moves_list.append((position[0], position[1] - j))
                                break
                        elif (position[0], position[1] - j) in allies_locations:
                            moves_list.append((position[0], position[1] - j))
                            break
                        else:
                            break
                elif i == 1:  # down
                    for j in range(1, 8):
                        if (position[0], position[1] + j) not in allies_locations and (position[1] + j) < 8:
                            if (position[0], position[1] + j) not in enemies_locations:
                                moves_list.append((position[0], position[1] + j))
                            else:
                                moves_list.append((position[0], position[1] + j))
                                break
                        elif (position[0], position[1] + j) in allies_locations:
                            moves_list.append((position[0], position[1] + j))
                            break
                        else:
                            break
                elif i == 2:  # right
                    for j in range(1, 8):
                        if (position[0] + j, position[1]) not in allies_locations and (position[0] + j) < 8:
                            if (position[0] + j, position[1]) not in enemies_locations:
                                moves_list.append((position[0] + j, position[1]))
                            else:
                                moves_list.append((position[0] + j, position[1]))
                                break
                        elif (position[0] + j, position[1]) in allies_locations:
                            moves_list.append((position[0] + j, position[1]))
                            break
                        else:
                            break
                else:  # left
                    for j in range(1, 8):
                        if (position[0] - j, position[1]) not in allies_locations and (position[0] - j) > -1:
                            if (position[0] - j, position[1]) not in enemies_locations:
                                moves_list.append((position[0] - j, position[1]))
                            else:
                                moves_list.append((position[0] - j, position[1]))
                                break
                        elif (position[0] - j, position[1]) in allies_locations:
                            moves_list.append((position[0] - j, position[1]))
                            break
                        else:
                            break

    if king_position in moves_list:
        return True
    else:
        return False


# check king moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        allies_locations = white_locations
        enemies_options = black_options
        enemies_locations = black_locations
        enemies_pieces = black_pieces
    else:
        allies_locations = black_locations
        enemies_options = white_options
        enemies_locations = white_locations
        enemies_pieces = white_pieces

    targets = [(0, 1), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1)]
    for i in range(8):
        check = True
        for j, moves in enumerate(enemies_options):
            if enemies_pieces[j] == 'pawn':
                if (position[0] + targets[i][0], position[1] + targets[i][1]) not in allies_locations and \
                        (position[0] + targets[i][0], position[1] + targets[i][1]) in moves and \
                        near_enemy_king((position[0] + targets[i][0], position[1] + targets[i][1]), color) == False and \
                        near_enemy_pawn((position[0] + targets[i][0], position[1] + targets[i][1]), color) == False and \
                        near_enemy_rook((position[0] + targets[i][0], position[1] + targets[i][1]), color) == False and \
                        near_enemy_bishop((position[0] + targets[i][0], position[1] + targets[i][1]),
                                          color) == False and \
                        near_enemy_knight((position[0] + targets[i][0], position[1] + targets[i][1]),
                                          color) == False and \
                        near_enemy_queen((position[0] + targets[i][0], position[1] + targets[i][1]), color) == False and \
                        -1 < (position[0] + targets[i][0]) < 8 and -1 < (position[1] + targets[i][1]) < 8:
                    pass
                else:
                    check = False
                    break

            else:
                if (position[0] + targets[i][0], position[1] + targets[i][1]) not in allies_locations and \
                        (position[0] + targets[i][0], position[1] + targets[i][1]) not in moves and \
                        near_enemy_king((position[0] + targets[i][0], position[1] + targets[i][1]), color) == False and \
                        near_enemy_pawn((position[0] + targets[i][0], position[1] + targets[i][1]), color) == False and \
                        near_enemy_rook((position[0] + targets[i][0], position[1] + targets[i][1]), color) == False and \
                        near_enemy_bishop((position[0] + targets[i][0], position[1] + targets[i][1]),
                                          color) == False and \
                        near_enemy_knight((position[0] + targets[i][0], position[1] + targets[i][1]),
                                          color) == False and \
                        near_enemy_queen((position[0] + targets[i][0], position[1] + targets[i][1]), color) == False and \
                        -1 < (position[0] + targets[i][0]) < 8 and -1 < (position[1] + targets[i][1]) < 8:
                    pass
                else:
                    check = False
                    break

            if check == True:
                moves_list.append((position[0] + targets[i][0], position[1] + targets[i][1]))

    if color == "white":
        if MOVE1 == True:
            if (1, 7) not in allies_locations:
                if (2, 7) not in allies_locations:
                    if (3, 7) not in allies_locations:
                        if (1, 7) not in enemies_locations:
                            if (2, 7) not in enemies_locations:
                                if (3, 7) not in enemies_locations:
                                    moves_list.append((2, 7))

    if color == "white":
        if MOVE1 == True:
            if (5, 7) not in allies_locations:
                if (6, 7) not in allies_locations:
                    if (5, 7) not in enemies_locations:
                        if (6, 7) not in enemies_locations:
                            moves_list.append((6, 7))

    if color == "black":
        if MOVE2 == True:
            if (1, 0) not in allies_locations:
                if (2, 0) not in allies_locations:
                    if (3, 0) not in allies_locations:
                        if (1, 0) not in enemies_locations:
                            if (2, 0) not in enemies_locations:
                                if (3, 0) not in enemies_locations:
                                    moves_list.append((2, 0))

    if color == "black":
        if MOVE2 == True:
            if (5, 0) not in allies_locations:
                if (6, 0) not in allies_locations:
                    if (5, 0) not in enemies_locations:
                        if (6, 0) not in enemies_locations:
                            moves_list.append((6, 0))

    if in_check(color)[0] == True:
        in_check_moves_list = []
        for moves in moves_list:
            if moves not in in_check(color)[2] or moves == enemies_locations[in_check(color)[1]]:
                in_check_moves_list.append(moves)

        return in_check_moves_list
    else:
        return moves_list

    # check queen moves


def check_queen(position, color):
    moves_list = check_bishop(position, color)
    rook_list = check_rook(position, color)

    for i in range(len(rook_list)):
        moves_list.append(rook_list[i])

    return moves_list


# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        allies_locations = white_locations
        enemies_locations = black_locations
        enemies_options = black_options
    else:
        allies_locations = black_locations
        enemies_locations = white_locations
        enemies_options = white_options

    for i in range(4):  # diagonals
        if i == 0:  # top-right
            for j in range(1, 8):
                if (position[0] + j, position[1] - j) not in allies_locations and \
                        (position[0] + j) < 8 and (position[1] - j) > -1:
                    if (position[0] + j, position[1] - j) not in enemies_locations:
                        moves_list.append((position[0] + j, position[1] - j))
                    else:
                        moves_list.append((position[0] + j, position[1] - j))
                        break
                else:
                    break
        if i == 1:  # top-left
            for j in range(1, 8):
                if (position[0] - j, position[1] - j) not in allies_locations and \
                        (position[0] - j) > -1 and (position[1] - j) > -1:
                    if (position[0] - j, position[1] - j) not in enemies_locations:
                        moves_list.append((position[0] - j, position[1] - j))
                    else:
                        moves_list.append((position[0] - j, position[1] - j))
                        break
                else:
                    break
        if i == 2:  # bottom-right
            for j in range(1, 8):
                if (position[0] + j, position[1] + j) not in allies_locations and \
                        (position[0] + j) < 8 and (position[1] + j) < 8:
                    if (position[0] + j, position[1] + j) not in enemies_locations:
                        moves_list.append((position[0] + j, position[1] + j))
                    else:
                        moves_list.append((position[0] + j, position[1] + j))
                        break
                else:
                    break
        else:  # bottom-left
            for j in range(1, 8):
                if (position[0] - j, position[1] + j) not in allies_locations and \
                        (position[0] - j) > -1 and (position[1] + j) < 8:
                    if (position[0] - j, position[1] + j) not in enemies_locations:
                        moves_list.append((position[0] - j, position[1] + j))
                    else:
                        moves_list.append((position[0] - j, position[1] + j))
                        break
                else:
                    break

    if in_check(color)[0] == True:
        in_check_moves_list = []
        for moves in moves_list:
            if moves in in_check(color)[2] or moves == enemies_locations[in_check(color)[1]]:
                in_check_moves_list.append(moves)

        return in_check_moves_list
    else:
        return moves_list


# check knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        allies_locations = white_locations
        enemies_locations = black_locations
        enemies_options = black_options
    else:
        allies_locations = black_locations
        enemies_locations = white_locations
        enemies_options = white_options

    # Top-right up
    if (position[0] + 1, position[1] - 2) not in allies_locations and \
            (position[0] + 1) < 8 and (position[1] - 2) > -1:
        moves_list.append((position[0] + 1, position[1] - 2))
    # Top-right down
    if (position[0] + 2, position[1] - 1) not in allies_locations and \
            (position[0] + 2) < 8 and (position[1] - 1) > -1:
        moves_list.append((position[0] + 2, position[1] - 1))
    # Bottom-right up
    if (position[0] + 2, position[1] + 1) not in allies_locations and \
            (position[0] + 2) < 8 and (position[1] + 1) < 8:
        moves_list.append((position[0] + 2, position[1] + 1))
        # Bottom-right down
    if (position[0] + 1, position[1] + 2) not in allies_locations and \
            (position[0] + 1) < 8 and (position[1] + 2) < 8:
        moves_list.append((position[0] + 1, position[1] + 2))
        # Top-left up
    if (position[0] - 1, position[1] - 2) not in allies_locations and \
            (position[0] - 1) > -1 and (position[1] - 2) > -1:
        moves_list.append((position[0] - 1, position[1] - 2))
        # Top-left down
    if (position[0] - 2, position[1] - 1) not in allies_locations and \
            (position[0] - 2) > -1 and (position[1] - 2) > -1:
        moves_list.append((position[0] - 2, position[1] - 1))
    # Bottom-left up
    if (position[0] - 2, position[1] + 1) not in allies_locations and \
            (position[0] - 2) > -1 and (position[1] + 1) < 8:
        moves_list.append((position[0] - 2, position[1] + 1))
        # Bottom-left down
    if (position[0] - 1, position[1] + 2) not in allies_locations and \
            (position[0] - 1) > -1 and (position[1] + 2) < 8:
        moves_list.append((position[0] - 1, position[1] + 2))

    if in_check(color)[0] == True:
        in_check_moves_list = []
        for moves in moves_list:
            if moves in in_check(color)[2] or moves == enemies_locations[in_check(color)[1]]:
                in_check_moves_list.append(moves)

        return in_check_moves_list
    else:
        return moves_list

    # check rook moves


def check_rook(position, color):
    moves_list = []
    if color == 'white':
        allies_locations = white_locations
        enemies_locations = black_locations
        enemies_options = black_options

    else:
        allies_locations = black_locations
        enemies_locations = white_locations
        enemies_options = white_options

    for i in range(4):  # up, down, right, left
        if i == 0:  # up
            for j in range(1, 8):
                if (position[0], position[1] - j) not in allies_locations and (position[1] - j) > -1:
                    if (position[0], position[1] - j) not in enemies_locations:
                        moves_list.append((position[0], position[1] - j))
                    else:
                        moves_list.append((position[0], position[1] - j))
                        break
                else:
                    break
        elif i == 1:  # down
            for j in range(1, 8):
                if (position[0], position[1] + j) not in allies_locations and (position[1] + j) < 8:
                    if (position[0], position[1] + j) not in enemies_locations:
                        moves_list.append((position[0], position[1] + j))
                    else:
                        moves_list.append((position[0], position[1] + j))
                        break
                else:
                    break
        elif i == 2:  # right
            for j in range(1, 8):
                if (position[0] + j, position[1]) not in allies_locations and (position[0] + j) < 8:
                    if (position[0] + j, position[1]) not in enemies_locations:
                        moves_list.append((position[0] + j, position[1]))
                    else:
                        moves_list.append((position[0] + j, position[1]))
                        break
                else:
                    break
        else:  # left
            for j in range(1, 8):
                if (position[0] - j, position[1]) not in allies_locations and (position[0] - j) > -1:
                    if (position[0] - j, position[1]) not in enemies_locations:
                        moves_list.append((position[0] - j, position[1]))
                    else:
                        moves_list.append((position[0] - j, position[1]))
                        break
                else:
                    break

    if in_check(color)[0] == True:
        in_check_moves_list = []
        for moves in moves_list:
            if moves in in_check(color)[2] or moves == enemies_locations[in_check(color)[1]]:
                in_check_moves_list.append(moves)

        return in_check_moves_list
    else:
        return moves_list

    # check pawn moves and en passant


def en_passant(old_coords, new_coords):
    if turn_step < 2:
        index = white_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] + 1)
        piece = white_pieces[index]
    else:
        index = black_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] - 1)
        piece = black_pieces[index]
    if piece == "pawn" and abs(old_coords[1] - new_coords[1]) > 1:
        pass
    else:
        ep_coords = (100, 100)
    return ep_coords


def check_pawn(position, color):
    moves_list = []
    if color == "white":
        enemies_locations = black_locations
        enemies_options = black_options
        # forward moves
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] != 0:
            moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and \
                    position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        # diagonal moves
        if (position[0] - 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        if (position[0] + 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        # en passant
        if (position[0] - 1, position[1] - 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
        if (position[0] + 1, position[1] - 1) == black_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
    else:
        enemies_locations = white_locations
        enemies_options = white_options
        # forward moves
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] != 7:
            moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and \
                    position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        # diagonal moves
        if (position[0] - 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        if (position[0] + 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        # en passant
        if (position[0] - 1, position[1] + 1) == white_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
        if (position[0] + 1, position[1] + 1) == white_ep:
            moves_list.append((position[0] + 1, position[1] + 1))

    if in_check(color)[0] == True:
        in_check_moves_list = []
        for moves in moves_list:
            if moves in in_check(color)[2] or moves == enemies_locations[in_check(color)[1]]:
                in_check_moves_list.append(moves)

        return in_check_moves_list
    else:
        return moves_list

# handling promotion
def check_promotion():
    pawn_indexes = []
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index = 100
    for i in range(len(white_pieces)):
        if white_pieces[i] == "pawn":
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 0:
            white_promotion = True
            promote_index = pawn_indexes[i]
    pawn_indexes = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == "pawn":
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 7:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index

def draw_promotion():
    pygame.draw.rect(screen, "dark grey", [800, 0, 200, 420])
    if white_promote:
        color = "white"
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            index = piece_list.index(piece)
            screen.blit(white_images[index], (860, 100 + 100 * i))
    else:
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            index = piece_list.index(piece)
            screen.blit(black_images[index], (860, 100 + 100 * i))
    pygame.draw.rect(screen, color, [800, 100, 200, 420], 8)


def select_promotion():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 100
    y_pos = mouse_pos[1] // 100
    if white_promote and left_click and x_pos > 7 and y_pos < 5 and y_pos >= 1:
        white_pieces[promo_index] = white_promotions[y_pos - 1]
    if black_promote and left_click and x_pos > 7 and y_pos < 5 and y_pos >= 1:
        black_pieces[promo_index] = black_promotions[y_pos - 1]


# check for valid moves for selected pieces
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# draw valid moves on screen
def draw_valid(moves):
    for i in range(len(moves)):
        pygame.draw.circle(screen, "red", (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)


# main game loop
black_options = check_options(black_pieces, black_locations, "black")
white_options = check_options(white_pieces, white_locations, "white")
run = True
timer_running = False
white_promote, black_promote, promo_index = False, False, 100
draw = False
while run:
    timer.tick(fps)
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    # checking if the list of moves is empty for either white or black, if so it is a stalemate
    all_wempty = all(not sublist for sublist in white_options)
    all_bempty = all(not sublist for sublist in black_options)

    if all_wempty and in_check('white')[0] == False:
        draw = True
    elif all_bempty and in_check('black')[0] == False:
        draw = True

    if draw:
        screen.blit(font.render("Stalemate!", True, "black"), (840, 390))
        time.sleep(10)
        run = False

    white_promote, black_promote, promo_index = check_promotion()

    if white_promote or black_promote:
        draw_promotion()
        select_promotion()

    if timer_running and not draw:
        if turn_step in [0, 1]:  # White's turn
            white_time -= 1 / fps
        elif turn_step in [2, 3]:  # Black's turn
            black_time -= 1 / fps
        if white_time <= 0:
            screen.blit(font.render("Black Wins", True, "black"), (820, 600))
            screen.blit(font.render("on time!", True, "black"), (820, 630))
            time.sleep(10)
            break
        if black_time <= 0:
            screen.blit(font.render("White Wins", True, "black"), (820, 600))
            screen.blit(font.render("on time!", True, "black"), (820, 630))
            time.sleep(10)
            break

    # Update and display timer
    display_time(white_time, black_time)
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    if in_checkmate('white') == True:
        text = font.render("Black Wins!", True, (255, 255, 255))
        screen.blit(text, (840, 390))
        time.sleep(10)
        run = False

    if in_checkmate('black') == True:
        text = font.render("White Wins!", True, (255, 255, 255))
        screen.blit(text, (840, 390))
        time.sleep(10)
        run = False

        # event handling
    for event in pygame.event.get():
        # to check if red X at top of game window was clicked
        if event.type == pygame.QUIT:
            run = False

        all_wempty = all(not sublist for sublist in white_options)
        all_bempty = all(not sublist for sublist in black_options)

        if all_wempty and in_check('white')[0] == False:
            draw = True
        elif all_bempty and in_check('black')[0] == False:
            draw = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:  # if its white turn
                # if in_checkmate('white') == True:
                # text = font.render("Black Wins!", True, (255, 255, 255))
                # screen.blit(text, (840, 390))
                # run = False
                white_options = check_options(white_pieces, white_locations, "white")

                all_wempty = all(not sublist for sublist in white_options)

                if all_wempty and in_check('white')[0] == False:
                    draw = True
                    turn_step = 0

                if click_coords in white_locations:  # checks if we selected a white piece
                    # this will tell us what piece we just selected
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                        timer_running = True

                K = True
                if selection == 4 and white_locations[4] == (4, 7) \
                    and MOVE1 == True and click_coords in valid_moves and selection != 100 \
                    and click_coords == (2, 7) and A == True:
                    
                    white_ep = en_passant(white_locations[selection], click_coords)
                    white_locations[selection] = click_coords
                    white_locations[0] = (3, 7)
                    A = False
                    B = False
                    K = False
                    MOVE1 = False

                    turn_step = 2
                    selection = 100
                    valid_moves = []

                if selection == 4 and white_locations[4] == (4, 7) and MOVE1 == True \
                    and (5, 7) not in white_locations and click_coords in valid_moves \
                    and selection != 100 and click_coords == (6, 7) and B == True:
                    
                    white_ep = en_passant(white_locations[selection], click_coords)
                    white_locations[selection] = click_coords
                    white_locations[7] = (5, 7)
                    B = False
                    A = False
                    K = False                    
                    MOVE1 = False                                                            

                    turn_step = 2                    
                    selection = 100                    
                    valid_moves = []                                        

                if click_coords in valid_moves and selection != 100:
                    white_ep = en_passant(white_locations[selection], click_coords)
                    white_locations[selection] = click_coords
                    if click_coords in black_locations or click_coords == black_ep:
                        if click_coords == black_ep:
                            black_piece_num = black_locations.index((black_ep[0], black_ep[1] + 1))
                        elif click_coords in black_locations:
                            black_piece_num = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece_num])
                        black_pieces.pop(black_piece_num)
                        black_locations.pop(black_piece_num)

                    white_options = check_options(white_pieces, white_locations, "white")
                    black_options = check_options(black_pieces, black_locations, "black")

                    # checking for stalemate
                    all_bempty = all(not sublist for sublist in black_options)

                    if all_bempty and in_check('black')[0] == False:
                        draw = True

                    if selection == 0:
                        MOVE1 = False
                    if selection == 7:
                        MOVE1 = False
                    if selection == 4:
                        MOVE1 = False
                        # screen.blit(font.render("Stalemate!", True, "black"),(840, 390))
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            if turn_step > 1:
                # if in_checkmate('black') == True:
                # text = font.render("White Wins!", True, (255, 255, 255))
                # screen.blit(text, (840, 390))
                # run = False

                black_options = check_options(black_pieces, black_locations, "black")
                all_bempty = all(not sublist for sublist in black_options)

                if all_bempty and in_check('black')[0] == False:
                    draw = True
                    turn_step = 0

                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3

                if selection == 4 and black_locations[4] == (4,0) and MOVE2 == True \
                    and click_coords in valid_moves and selection != 100 \
                        and click_coords == (2,0) and click_coords == (2,0):
                                    
                    black_ep = en_passant(black_locations[selection], click_coords)
                    black_locations[selection] = click_coords
                    black_locations[0] = (3, 0)
                    C = False
                    D = False
                    K = False
                    MOVE2 = False

                    turn_step = 0
                    selection = 100
                    valid_moves = []


                if selection == 4 and black_locations[4] == (4, 0) and MOVE2 == True \
                    and (5,0) not in white_locations and click_coords in valid_moves and selection != 100 \
                        and click_coords == (6, 0) and D == True:
                    black_ep = en_passant(black_locations[selection], click_coords)
                    black_locations[selection] = click_coords
                    black_locations[7] = (5, 0)
                    D = False
                    C = False
                    K = False
                    MOVE2 = False

                    turn_step = 0
                    selection = 100
                    valid_moves = []

                if click_coords in valid_moves and selection != 100:
                    black_ep = en_passant(black_locations[selection], click_coords)
                    black_locations[selection] = click_coords
                    if click_coords in white_locations or click_coords == white_ep:
                        if click_coords == white_ep:
                            white_piece_num = white_locations.index((white_ep[0], white_ep[1] - 1))
                        elif click_coords in white_locations:
                            white_piece_num = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece_num])
                        white_pieces.pop(white_piece_num)
                        white_locations.pop(white_piece_num)

                    white_options = check_options(white_pieces, white_locations, "white")
                    black_options = check_options(black_pieces, black_locations, "black")

                    all_wempty = all(not sublist for sublist in white_options)

                    if all_wempty and in_check('white')[0] == False:
                        draw = True
                        # screen.blit(font.render("Stalemate!", True, "black"),(840, 390))

                    if selection == 0:
                        MOVE2 = False
                    if selection == 7:
                        MOVE2 = False
                    if selection == 4:
                        MOVE2 = False
                    turn_step = 0
                    selection = 100  # dummy variable
                    valid_moves = []
    pygame.display.flip()

pygame.quit()