import pygame
import os

from pieces import Pawn
from pieces import Knight
from pieces import Bishop
from pieces import Rook
from pieces import Queen
from pieces import King

from board import Chessboard
from checks import Checks
from pieces import Spritesheet

pygame.init()
pygame.display.set_caption('CHESS')

clock = pygame.time.Clock()

WIN_WIDTH = 1000
WIN_HEIGHT = 640
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Chess board setup
BOARD_SIZE = 640
BOARD_START_X = 0
BOARD_START_Y = WIN_HEIGHT - BOARD_SIZE

check_handler = Checks()

board = Chessboard("W", check_handler, BOARD_SIZE, BOARD_START_X, BOARD_START_Y)


# Creates and inserts pieces into the board
def load_up_board():
    all_pieces = [
        Rook(board, "B", piece_imgs[10], 0, 0),
        Knight(board, "B", piece_imgs[9], 0, 1),
        Bishop(board, "B", piece_imgs[8], 0, 2),
        Queen(board, "B", piece_imgs[7], 0, 3),
        King(board, "B", piece_imgs[6], 0, 4),
        Bishop(board, "B", piece_imgs[8], 0, 5),
        Knight(board, "B", piece_imgs[9], 0, 6),
        Rook(board, "B", piece_imgs[10], 0, 7),

        Pawn(board, "B", piece_imgs[11], 1, 0),
        Pawn(board, "B", piece_imgs[11], 1, 1),
        Pawn(board, "B", piece_imgs[11], 1, 2),
        Pawn(board, "B", piece_imgs[11], 1, 3),
        Pawn(board, "B", piece_imgs[11], 1, 4),
        Pawn(board, "B", piece_imgs[11], 1, 5),
        Pawn(board, "B", piece_imgs[11], 1, 6),
        Pawn(board, "B", piece_imgs[11], 1, 7),
        Pawn(board, "W", piece_imgs[5], 6, 0),
        Pawn(board, "W", piece_imgs[5], 6, 1),
        Pawn(board, "W", piece_imgs[5], 6, 2),
        Pawn(board, "W", piece_imgs[5], 6, 3),
        Pawn(board, "W", piece_imgs[5], 6, 4),
        Pawn(board, "W", piece_imgs[5], 6, 5),
        Pawn(board, "W", piece_imgs[5], 6, 6),
        Pawn(board, "W", piece_imgs[5], 6, 7),
        Rook(board, "W", piece_imgs[4], 7, 0),
        Knight(board, "W", piece_imgs[3], 7, 1),
        Bishop(board, "W", piece_imgs[2], 7, 2),
        Queen(board, "W", piece_imgs[1], 7, 3),
        King(board, "W", piece_imgs[0], 7, 4),
        Bishop(board, "W", piece_imgs[2], 7, 5),
        Knight(board, "W", piece_imgs[3], 7, 6),
        Rook(board, "W", piece_imgs[4], 7, 7)
    ]
    for piece in all_pieces:
        board.board_array[piece.row][piece.column] = piece

    del all_pieces


# Setting up sprite sheet and resizing it
spritesheet = Spritesheet(os.path.join("assets", "chesspieces.png"))
spritesheet.img = pygame.transform.smoothscale(spritesheet.img, (430, 143)).convert_alpha()


def create_piece_imgs(spritesheet):
    width, height = spritesheet.img.get_size()
    width = width / 6
    height = height / 2
    imgs = []

    y = 0
    for _ in range(2):
        x = 0
        for _ in range(6):
            imgs.append(spritesheet.get_sprite(x, y, width, height))
            x += width
        y += height

    return imgs


piece_imgs = create_piece_imgs(spritesheet)


# The main func that controls the game state and general logic
def run():
    run = True
    load_up_board()
    # some task which can not be done in the class constructor
    board.kings = [
        board.board_array[0][4],
        board.board_array[7][4]
    ]
    board.update_all_pieces()
    board.update_legal_moves()

    # print(board.board_array)

    while run:
        clock.tick(240)
        print(clock.get_fps())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                board.handle_piece_selection(event.pos)
                board.handle_piece_movement(event.pos)

            render(WIN)


GREY = (51, 50, 48, 255)


# Renders the screen
def render(win):
    win.fill(GREY)
    board.render(win)
    pygame.display.update()


if __name__ == '__main__':
    run()
