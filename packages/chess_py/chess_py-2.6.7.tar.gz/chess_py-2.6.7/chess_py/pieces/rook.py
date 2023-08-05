# -*- coding: utf-8 -*-

"""
Class stores Rook on the board

| rank
| 7 8 ║♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
| 6 7 ║♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
| 5 6 ║… … … … … … … …
| 4 5 ║… … … … … … … …
| 3 4 ║… … … … … … … …
| 2 3 ║… … … … … … … …
| 1 2 ║♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
| 0 1 ║♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
| ----╚═══════════════
| ——---a b c d e f g h
| -----0 1 2 3 4 5 6 7
| ------file

| Copyright © 2016 Aubhro Sengupta. All rights reserved.
"""

import itertools

from .piece import Piece
from ..core.algebraic import notation_const
from ..core.algebraic.location import Location
from ..core.algebraic.move import Move


class Rook(Piece):
    def __init__(self, input_color, location):
        """
        Initializes a rook that is capable of being compared to another rook,
        and returning a list of possible moves.

        :type: input_color: Color
        :type: location: Location
        """
        super(Rook, self).__init__(input_color, location, "♜", "♖")
        self.has_moved = False

    def __str__(self):
        return "R"

    def direction_moves(self, direction, position):
        """
        Finds moves in a given direction

        :type: direction: lambda
        :type: position: Board
        :rtype: list
        """
        current = direction(self.location)

        def side_move(status):
            return self.create_move(current, status)

        assert isinstance(current, Location)
        while current.on_board() and \
                position.is_square_empty(current):
            yield side_move(notation_const.MOVEMENT)
            current = direction(current)

        if current.on_board() and \
                self.contains_opposite_color_piece(current, position):
            yield side_move(notation_const.CAPTURE)

    def possible_moves(self, position):
        """
        Returns all possible rook moves.

        :type: position: Board
        :rtype: list
        """
        for move in itertools.chain(*[self.direction_moves(fn, position) for fn in self.cross_fn]):
            yield move
