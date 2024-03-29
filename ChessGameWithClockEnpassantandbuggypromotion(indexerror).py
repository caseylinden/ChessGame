import pygame

pygame.init()
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Two Player Pygame Chess")
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60
# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

white_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
white_options =[]
black_options = []
captured_pieces_white = []
captured_pieces_black = []
white_ep = (100,100)
black_ep = (100,100)
# 0 - whites turn, no selection: 1 - whites turn, piece selected: 2 - black turn, no selection: 3 - black turn, piece selected
turn_step = 0
selection = 100
valid_moves = []
# load in game piece images (queen, king, rook, bishop, knight, pawn)
black_queen = pygame.image.load('black_queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))

black_king = pygame.image.load('black_king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))

black_knight = pygame.image.load('black_knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))

black_bishop = pygame.image.load('black_bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))

black_rook = pygame.image.load('black_rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))

black_pawn = pygame.image.load('black_pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (80, 80))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))

white_queen = pygame.image.load('white_queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))

white_king = pygame.image.load('white_king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))

white_knight = pygame.image.load('white_knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))

white_bishop = pygame.image.load('white_bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))

white_rook = pygame.image.load('white_rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))

white_pawn = pygame.image.load('white_pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (80, 80))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small, white_rook_small, white_bishop_small]

black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small, black_rook_small, black_bishop_small]

# this corresponds to the white_images/black_images indexes
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']


# check variables / flashing counter


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


#time settings
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



# draw pieces on board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 20))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))

        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100, white_locations[i][1] * 100, 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 20))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))

        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100, black_locations[i][1] * 100, 100, 100],2)


# check pawn moves
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
    else:
        king_position = black_locations[black_pieces.index('king')]
        enemies_options = white_options

    attacking_piece = 0

    for i, moves in enumerate(enemies_options):
        if king_position in moves:
            attacking_piece = i
            return True, attacking_piece

    return False, None


# check king moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        allies_locations = white_locations
        enemies_options = black_options
    else:
        allies_locations = black_locations
        enemies_options = white_options

    targets = [(0, 1), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1)]

    for i in range(8):
        check = True
        for moves in enemies_options:
            if (position[0] + targets[i][0], position[1] + targets[i][1]) not in allies_locations and \
                    (position[0] + targets[i][0], position[1] + targets[i][1]) not in moves and \
                    -1 < (position[0] + targets[i][0]) < 8 and -1 < (position[1] + targets[i][1]) < 8:
                pass
            else:
                check = False

        if check == True:
            moves_list.append((position[0] + targets[i][0], position[1] + targets[i][1]))

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
            if moves in enemies_options[in_check(color)[1]] or moves == enemies_locations[in_check(color)[1]]:
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
            if moves in enemies_options[in_check(color)[1]] or moves == enemies_locations[in_check(color)[1]]:
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
            if moves in enemies_options[in_check(color)[1]] or moves == enemies_locations[in_check(color)[1]]:
                in_check_moves_list.append(moves)

        return in_check_moves_list
    else:
        return moves_list

# check pawn moves and en passant
def en_passant(old_coords, new_coords):
    if turn_step < 2:
         index = white_locations.index(old_coords)
         ep_coords = (new_coords[0], new_coords[1]+1)
         piece = white_pieces[index]
    else:
         index = black_locations.index(old_coords)
         ep_coords = (new_coords[0], new_coords[1]-1)
         piece = black_pieces[index]
    if piece == "pawn" and abs(old_coords[1] - new_coords[1]) > 1:
        pass
    else:
        ep_coords = (100,100)
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
        #en passant
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
        #en passant
        if (position[0] - 1, position[1] + 1) == white_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
        if (position[0] + 1, position[1] + 1) == white_ep:
            moves_list.append((position[0] + 1, position[1] + 1))


    if in_check(color)[0] == True:
        in_check_moves_list = []
        for moves in moves_list:
            if moves in enemies_options[in_check(color)[1]] or moves == enemies_locations[in_check(color)[1]]:
                in_check_moves_list.append(moves)

        return in_check_moves_list
    else:
        return moves_list

#check for promotion
def check_promotion():
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
    pawn_index = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == "pawn":
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 7:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index

white_promotions = ["bishop", "knight", "rook", "queen"]
black_promotions = ["bishop", "knight", "rook", "queen"]

def draw_promotion():
    pygame.draw.rect(screen, "dark grey", [800, 0, 200, 420])
    if white_promote:
        color = "white"
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            index = piece_list.index(piece)
            screen.blit(white_images[index],(860, 100 + 100*i))
    else:
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            index = piece_list.index(piece)
            screen.blit(black_images[index],(860, 100 + 100*i))
    '''pygame.draw.rect(screen, color, [800,0,200,420],8)'''
def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 100
    y_pos = mouse_pos[1] // 100
    if white_promote and left_click and x_pos>7 and y_pos < 5:
        white_pieces[promo_index] = white_promotions[y_pos]
    if black_promote and left_click and x_pos>7 and y_pos < 5:
        black_pieces[promo_index] = black_promotions[y_pos]

# function to check all pieces valid options on board



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
while run:
    timer.tick(fps)
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    white_promote, black_promote, promo_index = check_promotion()
    if white_promote or black_promote:
        draw_promotion()
        check_promo_select()
    if timer_running:
        if turn_step in [0, 1]:  # White's turn
            white_time -= 1 / fps
        elif turn_step in [2, 3]:  # Black's turn
            black_time -= 1 / fps
        if white_time <= 0:
            print("White time's up! Black wins!")
            break
        if black_time <= 0:
            print("Black time's up! White wins!")
            break

    # Update and display timer
    display_time(white_time, black_time)
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    # event handling
    for event in pygame.event.get():
        # to check if red X at top of game window was clicked
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step <= 1: # if its white turn
                white_options = check_options(white_pieces, white_locations, "white")
                all_empty = all(not sublist for sublist in white_options)
                if all_empty:
                    run = False
                if click_coords in white_locations:  # checks if we selected a white piece

                    # this will tell us what piece we just selected
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                        timer_running = True
                if click_coords in valid_moves and selection != 100:
                    white_ep = en_passant(white_locations[selection], click_coords)
                    white_locations[selection] = click_coords
                    '''if click_coords[1] == 0 and white_pieces[selection] == "pawn":
                        draw_promotion("white")
                        white_pieces[selection] = "queen"'''
                    if click_coords in black_locations or click_coords == black_ep:
                        if click_coords == black_ep:
                            black_piece_num = black_locations.index((black_ep[0],black_ep[1]+1))
                        elif click_coords in black_locations:
                            black_piece_num = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece_num])
                        black_pieces.pop(black_piece_num)
                        black_locations.pop(black_piece_num)
                    white_options = check_options(white_pieces, white_locations, "white")
                    black_options = check_options(black_pieces, black_locations, "black")
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            if turn_step > 1:
                black_options = check_options(black_pieces, black_locations, "black")
                all_empty = all(not sublist for sublist in black_options)
                if all_empty:
                    run = False
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    black_ep = en_passant(black_locations[selection], click_coords)
                    black_locations[selection] = click_coords
                    '''if click_coords[1] == 7 and black_pieces[selection] == "pawn":
                        black_pieces[selection] = "queen"'''
                    if click_coords in white_locations or click_coords == white_ep:
                        if click_coords == white_ep:
                            white_piece_num = white_locations.index((white_ep[0],white_ep[1]-1))
                        elif click_coords in white_locations:
                            white_piece_num = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece_num])
                        white_pieces.pop(white_piece_num)
                        white_locations.pop(white_piece_num)
                    white_options = check_options(white_pieces, white_locations, "white")
                    black_options = check_options(black_pieces, black_locations, "black")
                    turn_step = 0
                    selection = 100 #dummy variable
                    valid_moves = []
    pygame.display.flip()

pygame.quit()