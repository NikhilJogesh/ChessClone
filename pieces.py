import pygame


class Spritesheet:
    def __init__(self, columnname):
        self.columnname = columnname
        self.img = pygame.image.load(columnname).convert_alpha()

    def get_sprite(self, x, y, w, h):
        sprite = self.img.subsurface(x, y, w, h)
        return sprite


class Piece:
    def __init__(self, board, colour, img, row, column):
        self.board = board
        self.colour = colour
        self.img = img
        """
		self.row and self.column are not tho ones used in chess notations,
		they represent the pos of the move in the board_array
		"""
        self.row = row  # starts from 0
        self.column = column  # starts from 0
        self.width, self.height = self.img.get_size()

        self.legal_moves = []
        self.move_history = []

    def generate_axial_legal_moves(self, legal_moves, row_offset, column_offset):
        for i in range(1, 8):  # Numbers 1 to 7
            try:
                move_row = self.row + row_offset * i
                move_column = self.column + column_offset * i
                if move_row < 0 or move_column < 0:
                    continue
                move = self.board.board_array[move_row][move_column]
                if move == 0:
                    legal_moves.append([move_row, move_column])
                elif move.colour != self.colour:
                    legal_moves.append([move_row, move_column])
                    break
                else:
                    break
            except IndexError:
                break


class Pawn(Piece):
    def __init__(self, board, colour, img, row, column):
        super().__init__(board, colour, img, row, column)
        if self.colour == "W":
            self.enpassant_moves = [
                [-1, 1],
                [-1, -1]
            ]
        else:
            self.enpassant_moves = [
                [1, -1],
                [1, 1]
            ]

    def generate_legal_moves(self):
        legal_pawn_moves = []

        if self.colour == "W":  # White
            if self.row == 6:
                is_moved = False
            else:
                is_moved = True

            all_white_pawn_moves = [[-1, 0], [-1, -1], [-1, 1]]
            if not is_moved:
                all_white_pawn_moves.append([-2, 0])

            for white_pawn_move in all_white_pawn_moves:
                try:
                    move_row = white_pawn_move[0] + self.row
                    move_column = white_pawn_move[1] + self.column
                    piece = self.board.board_array[move_row][move_column]

                    if move_row < 0 or move_column < 0:
                        continue

                    if white_pawn_move[1] == 0:  # If the move is just a straight move
                        if piece == 0:
                            legal_pawn_moves.append([move_row, move_column])
                    elif piece != 0:
                        if piece.colour != self.colour:
                            legal_pawn_moves.append([move_row, move_column])

                except IndexError:
                    pass

        elif self.colour == "B":  # Black
            if self.row == 1:
                is_moved = False
            else:
                is_moved = True

            all_black_pawn_moves = [[1, 0], [1, -1], [1, 1]]
            if not is_moved:
                all_black_pawn_moves.append([2, 0])

            for black_pawn_move in all_black_pawn_moves:
                try:
                    move_row = black_pawn_move[0] + self.row
                    move_column = black_pawn_move[1] + self.column
                    piece = self.board.board_array[move_row][move_column]
                    if move_row < 0 or move_column < 0:
                        continue

                    if black_pawn_move[1] == 0:  # If the move is just a straight move
                        if piece == 0:
                            legal_pawn_moves.append([move_row, move_column])
                    elif piece != 0:
                        if piece.colour != self.colour:
                            legal_pawn_moves.append([move_row, move_column])
                except IndexError:
                    pass

        self.legal_moves = legal_pawn_moves

    def is_enpassant(self, move, board_move_history):
        if self.enpassant_moves.count(move) > 0:
            new_piece_row = self.row + move[0]
            new_piece_column = self.column + move[1]
            destination = self.board[new_piece_row][new_piece_column]
            enpassant_victim = self.board[self.row][move[1]]
            if destination == 0 and isinstance(enpassant_victim, Pawn):
                if len(enpassant_victim.move_history) == 1:
                    if board_move_history[-1].piece_moved == enpassant_victim:
                        return True
        return False


class Rook(Piece):
    def generate_legal_moves(self):
        legal_rook_moves = []

        # Straight up column in the perspective of the "White" player
        # Straight down column in the perspective of the "Black" player
        self.generate_axial_legal_moves(legal_rook_moves, -1, 0)

        # Straight down column in the perspective of the "White" player
        # Straight up column in the perspective of the "Black" player
        self.generate_axial_legal_moves(legal_rook_moves, 1, 0)

        # Right row in the perspective of the "White" player
        # Left row in the perspective of the "Black" player
        self.generate_axial_legal_moves(legal_rook_moves, 0, 1)

        # Left row in the perspective of the "White" player
        # Right row in the perspective of the "Black" player
        self.generate_axial_legal_moves(legal_rook_moves, 0, -1)

        self.legal_moves = legal_rook_moves


class King(Piece):
    def __init__(self, board, colour, img, row, column):
        super().__init__(board, colour, img, row, column)
        if self.colour == "W":
            self.castle_moves = [
                [7, 2],
                [7, 6]
            ]
        else:
            self.castle_moves = [
                [0, 2],
                [0, 6]
            ]

    def generate_legal_moves(self):
        all_king_moves = [[1, 0], [-1, 0], [0, 1], [0, -1],
                          [-1, -1], [-1, 1], [1, -1], [1, 1]]

        legal_king_moves = []

        for king_move in all_king_moves:
            try:
                move_row = king_move[0] + self.row
                move_column = king_move[1] + self.column
                move = self.board.board_array[move_row][move_column]
                if move_row < 0 or move_column < 0:
                    continue

                if move == 0:
                    legal_king_moves.append([move_row, move_column])
                elif move.colour != self.colour:
                    legal_king_moves.append([move_row, move_column])

            except IndexError:
                pass

            self.legal_moves = legal_king_moves
            # This function add the castling move to the legal moves list
            self.handle_castling()

    def handle_castling(self):
        if len(self.move_history) == 0 and not \
                self.board.check_handler.is_check(self.board.board_array, self.board.kings)[0]:
            if self.colour == 'W':
                # Warning : Do not change the order of the element in the lists
                rooks = [
                    self.board.board_array[7][0],
                    self.board.board_array[7][7]
                ]

                to_be_empty_squares = [
                    [
                        self.board.board_array[7][1],
                        self.board.board_array[7][2],
                        self.board.board_array[7][3]
                    ],
                    [
                        self.board.board_array[7][5],
                        self.board.board_array[7][6]
                    ]
                ]

                to_be_check_free_square = [
                    [7, 3],
                    [7, 5]
                ]

            else:
                # Warning : Do not change the order of the element in the lists

                rooks = [
                    self.board.board_array[0][0],
                    self.board.board_array[0][7]
                ]

                to_be_empty_squares = [
                    [
                        self.board.board_array[0][1],
                        self.board.board_array[0][2],
                        self.board.board_array[0][3]
                    ],
                    [
                        self.board.board_array[0][5],
                        self.board.board_array[0][6]
                    ]
                ]

                to_be_check_free_square = [
                    [0, 3],
                    [0, 5]
                ]

            for i, rook in enumerate(rooks):
                if isinstance(rook, Rook):
                    # checks if the rook has ever moved
                    if len(rook.move_history) > 0:
                        continue

                    # Checks if the squares are empty for the king to castle
                    is_empty = []
                    for square in to_be_empty_squares[i]:
                        if square == 0:
                            is_empty.append(True)
                        else:
                            is_empty.append(False)

                    # skips to the other side if the squares are not empty
                    if not all(is_empty):
                        continue

                    # Look for check on the way to castling
                    # as the king cannot castle if it goes through a "check"
                    square_row = to_be_check_free_square[i][0]
                    square_column = to_be_check_free_square[i][1]

                    original_piece_row = self.row
                    original_piece_column = self.column

                    self.board.board_array[square_row][square_column] = self.board.board_array[self.row][self.column]
                    self.board.board_array[self.row][self.column] = 0

                    self.row = square_row
                    self.column = square_column

                    is_check, king_in_check = self.board.check_handler.is_check(self.board.board_array,
                                                                                self.board.kings)

                    self.board.board_array[original_piece_row][original_piece_column] = \
                        self.board.board_array[square_row][square_column]
                    self.board.board_array[square_row][square_column] = 0
                    self.row = original_piece_row
                    self.column = original_piece_column

                    if is_check and king_in_check.colour == self.colour:
                        break
                    else:
                        self.legal_moves.append(self.castle_moves[i])

    def perform_castling(self, castle_move):
        new_king_row = castle_move[0]
        new_king_column = castle_move[1]
        self.board.board_array[new_king_row][new_king_column] = self.board.board_array[self.row][self.column]
        self.board.board_array[self.row][self.column] = 0
        self.row = new_king_row
        self.column = new_king_column

        if self.column == 2:
            rook_column = 0
            new_rook_column = 3
        else:
            rook_column = 7
            new_rook_column = 5

        rook_row = self.row
        new_rook_row = self.row

        self.board.board_array[new_rook_row][new_rook_column] = self.board.board_array[rook_row][rook_column]
        self.board.board_array[new_rook_row][new_rook_column].row = new_rook_row
        self.board.board_array[new_rook_row][new_rook_column].column = new_rook_column
        self.board.board_array[rook_row][rook_column] = 0


class Knight(Piece):
    def generate_legal_moves(self):
        all_knight_moves = [[1, 2], [2, 1], [1, -2], [2, -1],
                            [-1, 2], [-2, 1], [-1, -2], [-2, -1]]
        legal_knight_moves = []
        for knight_move in all_knight_moves:
            try:
                move_row = knight_move[0] + self.row
                move_column = knight_move[1] + self.column
                move = self.board.board_array[move_row][move_column]
                if move_row < 0 or move_column < 0:
                    continue

                if move == 0:
                    legal_knight_moves.append([move_row, move_column])
                elif move.colour != self.colour:
                    legal_knight_moves.append([move_row, move_column])

            except IndexError:
                pass

        self.legal_moves = legal_knight_moves


class Queen(Piece):
    def generate_legal_moves(self):
        legal_queen_moves = []

        # Top-Left Diagonal in the perspective of the "White" player
        # Bottom-Right Diagonal in the perspective of the "White" player
        self.generate_axial_legal_moves(legal_queen_moves, -1, -1)

        # Top-Right Diagonal in the perspective of the "White" player
        # Bottom-Left Diagonal in the perspective of the "White" player
        self.generate_axial_legal_moves(legal_queen_moves, -1, 1)

        # Bottom-Right Diagonal in the perspective of the "White" player
        # Top-Left Diagonal in the perspective of the "White" player
        self.generate_axial_legal_moves(legal_queen_moves, 1, 1)

        # Bottom-Left Diagonal in the perspective of the "White" player
        # Top-Right Diagonal in the perspective of the "White" player
        self.generate_axial_legal_moves(legal_queen_moves, 1, -1)

        # Straight up column in the perspective of the "White" player
        # Straight down column in the perspective of the "Black" player
        self.generate_axial_legal_moves(legal_queen_moves, -1, 0)

        # Straight down column in the perspective of the "White" player
        # Straight up column in the perspective of the "Black" player
        self.generate_axial_legal_moves(legal_queen_moves, 1, 0)

        # Right row in the perspective of the "White" player
        # Left row in the perspective of the "Black" player
        self.generate_axial_legal_moves(legal_queen_moves, 0, 1)

        # Left row in the perspective of the "White" player
        # Right row in the perspective of the "Black" player
        self.generate_axial_legal_moves(legal_queen_moves, 0, -1)

        self.legal_moves = legal_queen_moves


class Bishop(Piece):
    def generate_legal_moves(self):
        legal_bishop_moves = []

        # Top-Left Diagonal in the perspective of the "White" player
        # Bottom-Right Diagonal in the perspective of the "White" player
        self.generate_axial_legal_moves(legal_bishop_moves, -1, -1)

        # Top-Right Diagonal in the perspective of the "White" player
        # Bottom-Left Diagonal in the perspective of the "White" player
        self.generate_axial_legal_moves(legal_bishop_moves, -1, 1)

        # Bottom-Right Diagonal in the perspective of the "White" player
        # Top-Left Diagonal in the perspective of the "White" player
        self.generate_axial_legal_moves(legal_bishop_moves, 1, 1)

        # Bottom-Left Diagonal in the perspective of the "White" player
        # Top-Right Diagonal in the perspective of the "White" player
        self.generate_axial_legal_moves(legal_bishop_moves, 1, -1)

        self.legal_moves = legal_bishop_moves
