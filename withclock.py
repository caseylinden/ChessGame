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

captured_pieces_white = []
captured_pieces_black = []
# 0 - whites turn, no selection: 1 - whites turn, piece selected: 2 - black turn, no selection: 3 - black turn, piece selected
turn_step = 0
selection = 100
valid_moves = []
# load in game piece images (queen, king, rook, bishop, knight, pawn)
black_queen = pygame.image.load('black_queen.png')
black_queen = pygame.transform.scale(black_queen, (90, 90))

black_king = pygame.image.load('black_king.png')
black_king = pygame.transform.scale(black_king, (90, 90))

black_knight = pygame.image.load('black_knight.png')
black_knight = pygame.transform.scale(black_knight, (90, 90))

black_bishop = pygame.image.load('black_bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (90, 90))

black_rook = pygame.image.load('black_rook.png')
black_rook = pygame.transform.scale(black_rook, (90, 90))

black_pawn = pygame.image.load('black_pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (90, 90))

white_queen = pygame.image.load('white_queen.png')
white_queen = pygame.transform.scale(white_queen, (90, 90))

white_king = pygame.image.load('white_king.png')
white_king = pygame.transform.scale(white_king, (90, 90))

white_knight = pygame.image.load('white_knight.png')
white_knight = pygame.transform.scale(white_knight, (90, 90))

white_bishop = pygame.image.load('white_bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (90, 90))

white_rook = pygame.image.load('white_rook.png')
white_rook = pygame.transform.scale(white_rook, (90, 90))

white_pawn = pygame.image.load('white_pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (90, 90))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]

black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]

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
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 5, black_locations[i][1] * 100 + 5))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 5, black_locations[i][1] * 100 + 5))

        if turn_step > 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [black_locations[i][0] * 100, black_locations[i][1] * 100, 100, 100], 2)

    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 5, white_locations[i][1] * 100 + 5))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 5, white_locations[i][1] * 100 + 5))

        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100, white_locations[i][1] * 100, 100, 100], 2)


# check pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == "white":
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] != 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and (
        position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] - 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        if (position[0] + 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
    else:
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] != 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and (
        position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] - 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        if (position[0] + 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
    return moves_list


# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == "white":
        enemies_position = black_locations
        allies_position = white_locations
    else:
        allies_position = black_locations
        enemies_position = white_locations

    return moves_list


# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == "pawn":
            moves_list = check_pawn(location, turn)
        '''elif piece == "rook":
      moves_list = check_rook(location, turn)
  elif piece == "knight":
      moves_list = check_knight(location, turn)
  elif piece == "bishop":
      moves_list = check_bishop(location, turn)
  elif piece == "king":
      moves_list = check_king(location, turn)
  elif piece == "queen":
      moves_list = check_queen(location, turn)'''
        all_moves_list.append(moves_list)
    return all_moves_list


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
while run:
    timer.tick(fps)
    screen.fill('grey')
    draw_board()
    draw_pieces()
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
            click_coord = (x_coord, y_coord)
            if turn_step < 2:
                if click_coord in white_locations:
                    selection = white_locations.index(click_coord)
                    if turn_step == 0:
                        turn_step = 1
                        timer_running = True
                if click_coord in valid_moves and selection != 100:
                    white_locations[selection] = click_coord
                    if click_coord in black_locations:
                        black_piece_num = black_locations.index(click_coord)
                        captured_pieces_white.append(black_pieces[black_piece_num])
                        black_pieces.pop(black_piece_num)
                        black_locations.pop(black_piece_num)
                    white_options = check_options(white_pieces, white_locations, "white")
                    black_options = check_options(black_pieces, black_locations, "black")
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            if turn_step >= 2:
                if click_coord in black_locations:
                    selection = black_locations.index(click_coord)
                    if turn_step == 2:
                        turn_step = 3
                if click_coord in valid_moves and selection != 100:
                    black_locations[selection] = click_coord
                    if click_coord in white_locations:
                        white_piece_num = white_locations.index(click_coord)
                        captured_pieces_black.append(white_pieces[white_piece_num])
                        white_pieces.pop(white_piece_num)
                        white_locations.pop(white_piece_num)
                    white_options = check_options(white_pieces, white_locations, "white")
                    black_options = check_options(black_pieces, black_locations, "black")
                    turn_step = 0
                    selection = 100
                    valid_moves = []

    pygame.display.flip()

pygame.quit()