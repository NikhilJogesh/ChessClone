from pieces import Pawn
from pieces import Knight
from pieces import Bishop
from pieces import Rook
from pieces import Queen
from pieces import King


class Checks:
    def __init__(self):
        pass

    # Looks for checks made by enemy rook, bishop and queen
    def look_for_axial_checks(self, board_array, king, row_offset, column_offset):
        for i in range(1, 8):  # Numbers 1 to 7
            try:

                piece_row = king.row + row_offset * i
                piece_column = king.column + column_offset * i

                piece = board_array[piece_row][piece_column]

                if piece != 0:
                    if piece.colour != king.colour and piece_row > 0 and piece_column > 0:
                        if row_offset != 0 and column_offset != 0:
                            if isinstance(piece, (Bishop, Queen)):
                                return True
                            else:
                                return False
                        elif row_offset == 0 or column_offset == 0:
                            if isinstance(piece, (Rook, Queen)):
                                return True
                            else:
                                return False
                    else:
                        return False

            except IndexError:
                pass

        return False

    def look_for_pawn_checks(self, board_array, king):
        # White
        if king.colour == "W":
            king_pawn_attacks = [
                [-1, -1],
                [-1, 1]
            ]
        # Black
        else:
            king_pawn_attacks = [
                [1, -1],
                [1, 1]
            ]

        for row, column in king_pawn_attacks:
            try:
                piece_row = king.row + row
                piece_column = king.column + column
                piece = board_array[piece_row][piece_column]
                if piece != 0:
                    if piece_row > 0 and piece_column > 0:
                        if piece.colour != king.colour and isinstance(piece, Pawn):
                            return True

            except IndexError:
                pass

        return False

    def look_for_knight_checks(self, board_array, king):
        king_knight_attacks = [
            [-2, -1],
            [-2, 1],
            [-1, 2],
            [1, 2],
            [2, 1],
            [2, -1],
            [1, 2],
            [1, -2]
        ]

        try:
            for row, column in king_knight_attacks:
                piece_row = king.row + row
                piece_column = king.column + column
                piece = board_array[piece_row][piece_column]
                if piece != 0:
                    if piece_row > 0 and piece_column > 0:
                        if piece.colour != king.colour and isinstance(piece, Knight):
                            return True

        except IndexError:
            pass

        return False

    def look_for_king_checks(self, board_array, king):
        king_attacks = [
            [-1, -1],
            [-1, 0],
            [-1, 1],
            [0, 1],
            [1, 1],
            [1, 0],
            [1, -1],
            [0, -1]
        ]

        try:
            for row, column in king_attacks:
                piece_row = king.row + row
                piece_column = king.column + column
                piece = board_array[piece_row][piece_column]
                if piece != 0:
                    if piece_row < 0 and piece_column < 0:
                        if piece.colour != king.colour and isinstance(piece, King):
                            return True

        except IndexError:
            pass

        return False

    def is_check(self, board_array, kings):  # returns False if both the kings are not in check

        all_axial_offsets = [
            [1, 1], [-1, 1], [1, -1], [-1, -1],
            [0, 1], [0, -1], [1, 0], [-1, 0]
        ]

        for king in kings:
            all_check_verifications = []

            # Queen, Rook, Bishop checks
            for offset in all_axial_offsets:
                is_in_check = self.look_for_axial_checks(board_array, king, offset[0], offset[1])
                all_check_verifications.append(is_in_check)

            # Pawn
            is_in_pawn_check = self.look_for_pawn_checks(board_array, king)
            all_check_verifications.append(is_in_pawn_check)

            # Knight
            is_in_knight_check = self.look_for_knight_checks(board_array, king)
            all_check_verifications.append(is_in_knight_check)

            # King
            is_in_king_check = self.look_for_king_checks(board_array, king)
            all_check_verifications.append(is_in_king_check)

            if any(all_check_verifications):
                return True, king
                print(all_check_verifications)

        return False, None

    # Prevents illegals moves that keep or cause the king to be in check
    def remove_pinned_moves(self, board_array, kings, piece):
        pinned_moves = []
        for move in piece.legal_moves:
            move_row = move[0]
            move_column = move[1]
            piece_in_destination = board_array[move_row][move_column]
            original_piece_row = piece.row
            original_piece_column = piece.column
            board_array[original_piece_row][original_piece_column] = 0
            board_array[move_row][move_column] = piece
            piece.row = move_row
            piece.column = move_column

            is_check, king_in_check = self.is_check(board_array, kings)
            if is_check and king_in_check.colour == piece.colour:
                pinned_moves.append(move)

            board_array[original_piece_row][original_piece_column] = piece
            piece.row = original_piece_row
            piece.column = original_piece_column
            board_array[move_row][move_column] = piece_in_destination

        for pinned_move in pinned_moves:
            piece.legal_moves.remove(pinned_move)
