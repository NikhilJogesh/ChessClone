
class Move:
    def __init__(self, move_type, piece_moved, original_position, new_position, piece_captured=None,
                 rook_moved_in_castle=None, rook_moved_in_castle_original_position=None,
                 rook_moved_in_castle_new_position=None):
        move_types = ["normal", "capture", "enpassant", "castle"]
        self.move_type = move_type
        self.piece_moved = piece_moved
        self.original_position = original_position
        self.new_position = new_position
        self.piece_captured = piece_captured
        self.rook_moved_in_castle = rook_moved_in_castle
        self.rook_moved_in_castle_original_position = rook_moved_in_castle_original_position
        self.rook_moved_in_castle_new_position = rook_moved_in_castle_new_position
