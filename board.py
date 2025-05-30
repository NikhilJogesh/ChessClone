import pygame

from move import Move
from pieces import King, Pawn


class Chessboard:
    # Colours
    BLUE = (0, 73, 115)
    WHITE = (240, 234, 214)
    GREY = (84, 84, 84)
    DARK_GREY = (51, 50, 48, 255)

    def __init__(
            self, player_colour, check_handler, board_size, start_x, start_y,
            colour1=BLUE, colour2=WHITE, notation_colour=GREY, move_marking_colour=DARK_GREY,
            circle_marking_radius=10, font_size=30):

        self.player_piece_colour = player_colour
        self.check_handler = check_handler
        self.board_size = board_size
        self.start_x = start_x
        self.start_y = start_y

        self.player_colours = ["W", "B"]
        self.square_size = board_size // 8
        self.colour1 = colour1
        self.colour2 = colour2
        self.move_marking_colour = move_marking_colour
        self.colour4 = (122, 120, 115)
        self.notation_colour = notation_colour
        self.font = pygame.font.SysFont("Roboto", font_size)
        self.kings = None

        self.circle_marking_radius = circle_marking_radius
        self.graphic_squares = self.create_graphical_board()
        self.graphic_notation = self.create_notations()
        self.board_array = [[0 for _ in range(8)] for _ in range(8)]
        self.all_pieces = []
        self.move_history = []

        self.to_play = self.player_colours[0]
        self.selected_square_pos = None
        self.tmp_is_selected = False
        self.tmp_is_moved = False
        self.in_check = None

    # Creates all the squares of the board graphically
    def create_graphical_board(self):
        x = self.start_x
        y = self.start_y
        board = []
        for _ in range(8):
            row = []
            for _ in range(8):
                cell = pygame.Rect(x, y, self.square_size, self.square_size)
                row.append(cell)
                x += self.square_size
            board.append(row)
            x = self.start_x
            y += self.square_size
        del x, y
        return board

    # Creates notations (index) for both row and column
    def create_notations(self):
        row_notation_x = self.start_x + 5
        row_notation_y = self.start_y + 5
        column_notation_x = self.start_x + self.square_size - 5 - 15
        column_notation_y = self.start_y + self.board_size - 5 - 15

        notations = []
        if self.player_piece_colour == self.player_colours[0]:  # White
            for i in range(8):
                text = self.font.render(str(8 - i), 1, self.notation_colour)
                notations.append([text, row_notation_x, row_notation_y])
                row_notation_y += self.square_size

                text = self.font.render(chr(97 + i), 1, self.notation_colour)
                notations.append([text, column_notation_x, column_notation_y])
                column_notation_x += self.square_size

        else:  # Black
            for i in range(8):
                text = self.font.render(str(i + 1), 1, self.notation_colour)
                notations.append([text, row_notation_x, row_notation_y])
                row_notation_y += self.square_size

                text = self.font.render(chr(97 + 8 - i - 1), 1, self.notation_colour)
                notations.append([text, column_notation_x, column_notation_y])
                column_notation_x += self.square_size

        del text
        return notations

    # updates the "self.all_pieces" array for efficiency
    def update_all_pieces(self):
        self.all_pieces = []
        for row in self.board_array:
            for piece in row:
                if piece != 0:
                    self.all_pieces.append(piece)

    # Updates legal moves for all pieces
    # This function is run every move
    def update_legal_moves(self):
        print("Generating Legal Moves")
        for piece in self.all_pieces:
            if piece.colour != self.to_play:
                piece.legal_moves = []
            else:
                piece.generate_legal_moves()
                self.check_handler.remove_pinned_moves(self.board_array, self.kings, piece)

    def is_checkmate(self):
        for piece in self.all_pieces:
            if len(piece.legal_moves) != 0:
                return False
        return True

    # Handles selection of pieces
    def handle_piece_selection(self, pos):
        self.tmp_is_moved = False
        self.tmp_is_selected = False
        x, y = pos
        row = (y - self.start_y) // self.square_size
        column = (x - self.start_x) // self.square_size
        piece = self.board_array[row][column]
        if piece != 0:
            print(piece.legal_moves)
            if piece.colour == self.to_play and not self.tmp_is_moved:
                if (row, column) == self.selected_square_pos:
                    self.selected_square_pos = None
                else:
                    self.selected_square_pos = row, column
                    self.tmp_is_selected = True

    # Handles movement of pieces
    def handle_piece_movement(self, pos):
        self.tmp_is_moved = False

        if self.selected_square_pos is not None and not self.tmp_is_selected:
            x, y = pos
            new_row = (y - self.start_y) // self.square_size
            new_column = (x - self.start_x) // self.square_size
            row, column = self.selected_square_pos

            if self.board_array[row][column].legal_moves.count([new_row, new_column]) > 0:
                is_legal_move = True
            else:
                is_legal_move = False

            if is_legal_move:
                piece = self.board_array[row][column]
                move = [new_row, new_column]
                # checks if it is a castling move
                if isinstance(piece, King) and piece.castle_moves.count(move) > 0:
                    piece.perform_castling(move)

                elif isinstance(piece, Pawn) and piece.is_enpassant(move, self.move_history):
                    piece.is_enpassant(move, self.move_history)

                else:
                    if self.board_array[new_row][new_column] == 0:
                        move_type = "normal"
                        self.move_history.append(
                            Move(move_type, piece, self.selected_square_pos, move)
                        )
                    else:
                        move_type = "capture"
                        self.move_history.append(
                            Move(move_type, piece, self.selected_square_pos, move,
                                 piece_captured=self.board_array[new_row][new_column])
                        )
                    # Moves the pieces into the new square
                    self.board_array[new_row][new_column] = self.board_array[row][column]
                    self.board_array[new_row][new_column].row = new_row
                    self.board_array[new_row][new_column].column = new_column
                    self.board_array[new_row][new_column].move_history.append([new_row, new_column])

                    # Resets the original position
                    self.board_array[row][column] = 0

                # Deselects the piece for the next move
                self.selected_square_pos = None
                self.tmp_is_moved = True
                if self.to_play == self.player_colours[0]:  # White to Black
                    self.to_play = self.player_colours[1]
                else:  # Black to White
                    self.to_play = self.player_colours[0]

                # Updates the all)pieces array to the new stata of the board array
                self.update_all_pieces()

                # Resets the legal_moves
                self.update_legal_moves()

                # Looks for check mate
                if self.is_checkmate():
                    print("Checkmate !!!")
                    quit()

        self.tmp_is_selected = False

    # TODO: separate this function into a new file
    # Renders the board, pieces and pieces
    def render(self, surface):
        column = 1
        colour = self.colour1

        for r, row in enumerate(self.graphic_squares):
            for c, square in enumerate(row):
                if column <= 8:
                    if colour == self.colour2:
                        colour = self.colour1
                    elif colour == self.colour1:
                        colour = self.colour2

                pygame.draw.rect(surface, colour, square)

                if self.selected_square_pos is not None:
                    if r == self.selected_square_pos[0] and c == self.selected_square_pos[1]:
                        pygame.draw.rect(surface, self.move_marking_colour, square)

                if column == 8:
                    if colour == self.colour2:
                        colour = self.colour1
                    elif colour == self.colour1:
                        colour = self.colour2
                    column = 0
                column += 1

                if self.board_array[r][c] != 0:
                    piece_img = self.board_array[r][c].img
                    piece_width, piece_height = piece_img.get_size()
                    piece_x = square.x + (square.width - piece_width) / 2
                    piece_y = square.y + (square.height - piece_height) / 2
                    surface.blit(piece_img, (piece_x, piece_y))

        del column

        for notation in self.graphic_notation:
            surface.blit(notation[0], (notation[1], notation[2]))

        if self.selected_square_pos is not None:
            selected_piece_row = self.selected_square_pos[0]
            selected_piece_column = self.selected_square_pos[1]
            selected_piece = self.board_array[selected_piece_row][selected_piece_column]
            # print(selected_piece.legal_moves)
            for legal_move in selected_piece.legal_moves:
                try:
                    circle_marking_x = self.start_x + legal_move[1] * self.square_size + self.square_size / 2
                    circle_marking_y = self.start_y + legal_move[0] * self.square_size + self.square_size / 2
                except TypeError:
                    # print(legal_move)
                    quit()
                pygame.draw.circle(surface, self.move_marking_colour, (circle_marking_x, circle_marking_y),
                                   self.circle_marking_radius)
