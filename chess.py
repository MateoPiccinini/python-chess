from __future__ import annotations
from typing import List, Set, Dict


class Tile:
    piece: object = None
    tiles: Dict[tuple, Tile] = {}
    tag: str = None

    def __init__(self, x_coordinate: str, y_coordinate: int, team: any, occupied: bool):
        self.coords = (x_coordinate, y_coordinate)
        self.team = team
        self.occupied = occupied
        Tile.tiles[self.coords] = self

    def __repr__(self) -> str:
        return f"[{self.coords}]" if self.piece is None else f"{self.piece}"


class Rook:
    available_moves = []

    def __init__(self, tile: any, team: str, number: int):
        self.tile = tile
        self.team = team
        self.number = number
        tile.occupied = True
        tile.team = team
        tile.piece = self
        self.tag = f"r{number}"
        tile.tag = self.tag

    def __repr__(self):
        if self.team == "white":
            return f"\033[2;30;47m[   ♖   ]\033[0;0m"
        else:
            return f"\033[2;37;40m[   ♖   ]\033[0;0m"

    def threatened_spaces(self) -> list:
        moves = []
        for i in self.lateral_movement_1():
            moves.append(i)
        for i in self.lateral_movement_2():
            moves.append(i)
        for i in self.upwards_movement():
            moves.append(i)
        for i in self.downwards_movement():
            moves.append(i)
        return moves

    def movement(self) -> list:
        return [x for x in self.threatened_spaces() if x.team != self.team]

    def eat_or_move(self, new_tile):
        self.movement()
        print(self.available_moves)
        if new_tile in self.movement():
            self.tile.team = None
            self.tile.occupied = False
            self.tile.piece = None
            self.tile.tag = None
            if new_tile.piece is not None:
                new_tile.piece.tile = None
            new_tile.piece = self
            new_tile.team = self.team
            new_tile.occupied = True
            new_tile.tag = self.tag
            self.tile = new_tile
        else:
            print(f"{self.tag} can't move towards {new_tile.coords} tile")

    def lateral_movement_1(self) -> list:

        available_spaces = []
        abc = "abcdefgh"
        x, y = self.tile.coords
        i = True
        wanted_x = abc.index(x) + 1
        if wanted_x == 8:
            i = False
        while i:
            new_tile = Tile.tiles[abc[wanted_x], y]
            if new_tile.occupied:
                available_spaces.append(new_tile)
                i = False
            else:
                available_spaces.append(new_tile)
                wanted_x += 1
            if wanted_x > 8:
                i = False
        return available_spaces

    def lateral_movement_2(self) -> list:
        available_spaces = []
        abc = "abcdefgh"
        x, y = self.tile.coords
        i = True
        wanted_x = abc.index(x) - 1
        if wanted_x == -1:
            i = False
        while i:
            new_tile = Tile.tiles[abc[wanted_x], y]
            if new_tile.occupied:
                available_spaces.append(new_tile)
                i = False
            else:
                available_spaces.append(new_tile)
                wanted_x -= 1
            if wanted_x < 0:
                i = False
        return available_spaces

    def upwards_movement(self) -> list:
        available_spaces = []
        x, y = self.tile.coords
        i = True
        wanted_y = y + 1
        if wanted_y == 9:
            i = False
        while i:
            new_tile = Tile.tiles[x, wanted_y]
            if new_tile.occupied:
                available_spaces.append(new_tile)
                i = False
            elif not new_tile.occupied:
                available_spaces.append(new_tile)
                wanted_y += 1
            if wanted_y > 8:
                i = False
        return available_spaces

    def downwards_movement(self) -> list:
        available_spaces = []
        x, y = self.tile.coords
        i = True
        wanted_y = y - 1
        if wanted_y == 0:
            i = False
        while i:
            new_tile = Tile.tiles[x, wanted_y]
            if new_tile.occupied:
                available_spaces.append(new_tile)
                i = False
            elif not new_tile.occupied:
                available_spaces.append(new_tile)
                wanted_y -= 1
                if wanted_y < 1:
                    i = False
        return available_spaces


class Knight:
    available_moves = []

    def __init__(self, tile: any, team: str, number: int) -> object:
        self.tile = tile
        self.team = team
        self.number = number
        tile.occupied = True
        tile.team = team
        tile.piece = self
        self.tag = f"n{number}"
        tile.tag = self.tag

    def __repr__(self):
        if self.team == "white":
            return f"\033[2;30;47m[   ♘   ]\033[0;0m"
        else:
            return f"\033[2;37;40m[   ♘   ]\033[0;0m"

    def threatened_spaces(self) -> list:
        x_knight, y_knight = self.tile.coords
        available_space = []
        abc = "abcdefgh"
        for row in Board.board:
            for tile in row:
                x, y = tile.coords
                if (abc.index(x) == abc.index(x_knight) + 2 or abc.index(x) == abc.index(x_knight) - 2) and (
                        y == y_knight + 1 or y == y_knight - 1):  # movimiento lateral
                    available_space.append(tile)
                elif (y == y_knight + 2 or y == y_knight - 2) and (
                        abc.index(x) == abc.index(x_knight) + 1 or abc.index(x) == abc.index(
                    x_knight) - 1):  # movimiento vertical
                    available_space.append(tile)
        return available_space

    def movement(self) -> list:
        available_space = self.threatened_spaces()
        actually_available_space = self.threatened_spaces()
        for tile in available_space:
            if tile.occupied and tile.team == self.team:
                actually_available_space.remove(tile)
        return actually_available_space

    def eat_or_move(self, new_tile):
        self.movement()
        print(self.movement())
        if new_tile in self.movement():
            self.tile.team = None
            self.tile.occupied = False
            self.tile.piece = None
            self.tile.tag = None
            if new_tile.piece is not None:
                new_tile.piece.tile = None
            new_tile.piece = self
            new_tile.team = self.team
            new_tile.occupied = True
            new_tile.tag = self.tag
            self.tile = new_tile
        else:

            print(f"{self.tag} can't move towards {new_tile.coords} tile")


class Pawn:
    available_moves = []

    def __init__(self, tile: object, team: str, number: int):
        self.tile = tile
        self.team = team
        self.number = number
        tile.occupied = True
        tile.team = team
        tile.piece = self
        self.tag = f"p{number}"
        tile.tag = self.tag

    def __repr__(self) -> str:
        if self.team == "white":
            return f"\033[2;30;47m[   ♙   ]\033[0;0m"
        else:
            return f"\033[2;37;40m[   ♙   ]\033[0;0m"

    def movement(self):
        movement = []
        for space in self.threatened_spaces():
            if type(space) == str:
                pass
            elif space.team is None or space.team != self.team:
                movement.append(space)
        self.available_moves = movement
        return movement

    def threatened_spaces(self) -> Set:
        abc = "abcdefgh"
        available_spaces = set()
        pawn_x, pawn_y = self.tile.coords
        for row in Board.board:
            for tile in row:
                x, y = tile.coords

                # WHITE PAWN MOVEMENTS

                if self.team == "white":
                    if tile.occupied == True and (abc.index(x) == abc.index(
                            pawn_x) + 1 and y == pawn_y + 1) and tile.team == "black":  # w right diagonal take
                        available_spaces.add(tile)
                    if tile.occupied == True and (abc.index(x) == abc.index(
                            pawn_x) - 1 and y == pawn_y + 1) and tile.team == "black":  # w left diagonal take
                        available_spaces.add(tile)
                    if pawn_y == 2 and pawn_x == x and y == 4 and (
                            tile.team is None or tile.team == "white"):  # w initial move
                        available_spaces.add(tile)
                    if pawn_x == x and y == pawn_y + 1 and (
                            tile.team is None or tile.team == "white"):  # w Regular move
                        available_spaces.add(tile)

                # BLACK PAWN MOVEMENTS

                elif self.team == "black":
                    if tile.occupied == True and (abc.index(x) == abc.index(
                            pawn_x) + 1 and y == pawn_y - 1) and tile.team == "white":  # b right diagonal take
                        available_spaces.add(tile)
                    if tile.occupied == True and (abc.index(x) == abc.index(
                            pawn_x) - 1 and y == pawn_y - 1) and tile.team == "white":  # b left diagonal take
                        available_spaces.add(tile)
                    if pawn_y == 7 and pawn_x == x and y == 5 and (
                            tile.team is None or tile.team == "black"):  # b initial move
                        available_spaces.add(tile)
                    if pawn_x == x and y == pawn_y - 1 and (
                            tile.team is None or tile.team == "black"):  # b Regular move
                        available_spaces.add(tile)
        return available_spaces if available_spaces != set() else "No available spaces"

    def eat_or_move(self, new_tile):
        self.movement()
        print(self.movement())
        if new_tile in self.movement():
            self.tile.team = None
            self.tile.occupied = False
            self.tile.piece = None
            self.tile.tag = None
            if new_tile.piece is not None:
                new_tile.piece.tile = None
            new_tile.piece = self
            new_tile.team = self.team
            new_tile.occupied = True
            new_tile.tag = self.tag
            self.tile = new_tile
        else:
            print(f"{self.tag} can't move towards {new_tile.coords} tile")


class Bishop:
    available_moves = []

    def __init__(self, tile: object, team: str, number: int):
        self.tile = tile
        self.team = team
        self.number = number
        tile.occupied = True
        tile.team = team
        tile.piece = self
        self.tag = f"b{number}"
        tile.tag = self.tag

    def __repr__(self) -> str:
        if self.team == "white":
            return f"\033[2;30;47m[   ♗   ]\033[0;0m"
        else:
            return f"\033[2;37;40m[   ♗   ]\033[0;0m"

    def movement(self) -> list:
        abc = "0abcdefgh"
        bishop_x, bishop_y = self.tile.coords
        available_spaces = []
        movement = []
        for row in Board.board:
            for tile in row:
                x, y = tile.coords
                if abc.index(x) == abc.index(bishop_x) - 1 and y == bishop_y + 1:  # Spaces in top left axis
                    for spaces in self.l_top_axis(abc.index(x), y):
                        available_spaces.append(spaces)
                if abc.index(x) == abc.index(bishop_x) - 1 and y == bishop_y - 1:  # Spaces in bottom left axis
                    for spaces in self.l_bot_axis(abc.index(x), y):
                        available_spaces.append(spaces)
                if abc.index(x) == abc.index(bishop_x) + 1 and y == bishop_y + 1:  # Spaces in top right axis
                    for spaces in self.r_top_axis(abc.index(x), y):
                        available_spaces.append(spaces)
                if abc.index(x) == abc.index(bishop_x) + 1 and y == bishop_y - 1:  # Spaces in bottom right axis
                    for spaces in self.r_bot_axis(abc.index(x), y):
                        available_spaces.append(spaces)
        for tile in available_spaces:
            if tile.team != self.team:
                movement.append(tile)
        return movement

    def threatened_spaces(self) -> list:
        abc = "0abcdefgh"
        bishop_x, bishop_y = self.tile.coords
        available_spaces = []
        for row in Board.board:
            for tile in row:
                x, y = tile.coords
                if abc.index(x) == abc.index(bishop_x) - 1 and y == bishop_y + 1:  # Spaces in top left axis
                    for spaces in self.l_top_axis(abc.index(x), y):
                        available_spaces.append(spaces)
                if abc.index(x) == abc.index(bishop_x) - 1 and y == bishop_y - 1:  # Spaces in bottom left axis
                    for spaces in self.l_bot_axis(abc.index(x), y):
                        available_spaces.append(spaces)
                if abc.index(x) == abc.index(bishop_x) + 1 and y == bishop_y + 1:  # Spaces in top right axis
                    for spaces in self.r_top_axis(abc.index(x), y):
                        available_spaces.append(spaces)
                if abc.index(x) == abc.index(bishop_x) + 1 and y == bishop_y - 1:  # Spaces in bottom right axis
                    for spaces in self.r_bot_axis(abc.index(x), y):
                        available_spaces.append(spaces)
        return available_spaces

    def l_top_axis(self, x: int, y: int, available_spaces=None) -> list:  # Spaces in top left axis
        if available_spaces is None:
            available_spaces = []
        abc = "0abcdefgh"
        if x == 0 or y == 9:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            available_spaces.append(tile)
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.l_top_axis(x - 1, y + 1, available_spaces)

    def l_bot_axis(self, x: int, y: int, available_spaces=None) -> list:  # Spaces in top left axis
        if available_spaces is None:
            available_spaces = []
        abc = "0abcdefgh"
        if x == 0 or y == 0:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            available_spaces.append(tile)
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.l_bot_axis(x - 1, y - 1, available_spaces)

    def r_top_axis(self, x: int, y: int, available_spaces=None) -> list:
        if available_spaces is None:
            available_spaces = []
        abc = "0abcdefgh"
        if x > 8 or y > 8:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            available_spaces.append(tile)
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.r_top_axis(x + 1, y + 1, available_spaces)

    def r_bot_axis(self, x: int, y: int, available_spaces=None) -> list:
        if available_spaces is None:
            available_spaces = []
        abc = "0abcdefgh"
        if x > 8 or y == 0:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            available_spaces.append(tile)
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.r_bot_axis(x + 1, y - 1, available_spaces)

    def eat_or_move(self, new_tile):
        self.movement()
        print(self.movement())
        if new_tile in self.movement():
            self.tile.team = None
            self.tile.occupied = False
            self.tile.piece = None
            self.tile.tag = None
            if new_tile.piece is not None:
                new_tile.piece.tile = None
            new_tile.piece = self
            new_tile.team = self.team
            new_tile.occupied = True
            new_tile.tag = self.tag
            self.tile = new_tile
        else:
            print(f"{self.tag} can't move towards {new_tile.coords} tile")


class Queen:
    available_moves = []

    def __init__(self, tile: object, team: str, number: int):
        self.tile = tile
        self.team = team
        self.number = number
        tile.occupied = True
        tile.team = team
        tile.piece = self
        self.tag = f"q "
        tile.tag = self.tag

    def __repr__(self):
        if self.team == "white":
            return f"\033[2;30;47m[   ♕   ]\033[0;0m"
        else:
            return f"\033[2;37;40m[   ♕   ]\033[0;0m"

    def straight_movement(self):
        moves = []
        lateral_1 = self.lateral_movement_1()
        lateral_2 = self.lateral_movement_2()
        upwards = self.upwards_movement()
        downwards = self.downwards_movement()
        for i in lateral_1:
            moves.append(i)
        for i in lateral_2:
            moves.append(i)
        for i in upwards:
            moves.append(i)
        for i in downwards:
            moves.append(i)
        return moves

    def lateral_movement_1(self):
        available_spaces = []
        abc = "abcdefgh"
        x, y = self.tile.coords
        i = True
        wanted_x = abc.index(x) + 1
        if wanted_x == 8:
            i = False
        while i:
            new_tile = Tile.tiles[abc[wanted_x], y]
            if new_tile.occupied:
                if new_tile.team == self.team:
                    available_spaces.append(new_tile)
                    i = False
                else:
                    available_spaces.append(new_tile)
                    i = False
            else:
                available_spaces.append(new_tile)
                wanted_x += 1
            if wanted_x > 8:
                i = False
        return available_spaces

    def lateral_movement_2(self):
        available_spaces = []
        abc = "abcdefgh"
        x, y = self.tile.coords
        i = True
        wanted_x = abc.index(x) - 1
        if wanted_x == -1:
            i = False
        while i:
            new_tile = Tile.tiles[abc[wanted_x], y]
            if new_tile.occupied:
                if new_tile.team == self.team:
                    available_spaces.append(new_tile)
                    i = False
                else:
                    available_spaces.append(new_tile)
                    i = False
            else:
                available_spaces.append(new_tile)
                wanted_x -= 1
            if wanted_x < 0:
                i = False
        return available_spaces

    def upwards_movement(self):
        available_spaces = []
        x, y = self.tile.coords
        i = True
        wanted_y = y + 1
        if wanted_y == 9:
            i = False
        while i:
            new_tile = Tile.tiles[x, wanted_y]
            if new_tile.occupied:
                if new_tile.team == self.team:
                    available_spaces.append(new_tile)
                    i = False
                else:
                    available_spaces.append(new_tile)
                    i = False
            elif not new_tile.occupied:
                available_spaces.append(new_tile)
                wanted_y += 1
            if wanted_y > 8:
                i = False
        return available_spaces

    def downwards_movement(self):
        available_spaces = []
        x, y = self.tile.coords
        i = True
        wanted_y = y - 1
        if wanted_y == 0:
            i = False
        while i:
            new_tile = Tile.tiles[x, wanted_y]
            if new_tile.occupied:
                if new_tile.team == self.team:
                    available_spaces.append(new_tile)
                    i = False
                else:
                    available_spaces.append(new_tile)
                    i = False
            elif not new_tile.occupied:
                available_spaces.append(new_tile)
                wanted_y -= 1
                if wanted_y < 1:
                    i = False
        return available_spaces

    def diagonal_movement(self):
        abc = "0abcdefgh"
        Queen_x, Queen_y = self.tile.coords
        available_spaces = []
        for row in Board.board:
            for tile in row:
                x, y = tile.coords
                if abc.index(x) == abc.index(Queen_x) - 1 and y == Queen_y + 1:  # Spaces in top left axis
                    for spaces in self.l_top_axis(abc.index(x), y):
                        available_spaces.append(spaces)
                if abc.index(x) == abc.index(Queen_x) - 1 and y == Queen_y - 1:  # Spaces in bottom left axis
                    for spaces in self.l_bot_axis(abc.index(x), y):
                        available_spaces.append(spaces)
                if abc.index(x) == abc.index(Queen_x) + 1 and y == Queen_y + 1:  # Spaces in top right axis
                    for spaces in self.r_top_axis(abc.index(x), y):
                        available_spaces.append(spaces)
                if abc.index(x) == abc.index(Queen_x) + 1 and y == Queen_y - 1:  # Spaces in bottom right axis
                    for spaces in self.r_bot_axis(abc.index(x), y):
                        available_spaces.append(spaces)
        return available_spaces

    def l_top_axis(self, x: int, y: int, available_spaces=None) -> list:  # Spaces in top left axis
        if available_spaces is None:
            available_spaces = []
        abc = "0abcdefgh"
        if x == 0 or y == 9:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            available_spaces.append(tile)
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.l_top_axis(x - 1, y + 1, available_spaces)

    def l_bot_axis(self, x: int, y: int, available_spaces=None) -> list:  # Spaces in top left axis
        if available_spaces is None:
            available_spaces = []
        abc = "0abcdefgh"
        if x == 0 or y == 0:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            available_spaces.append(tile)
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.l_bot_axis(x - 1, y - 1, available_spaces)

    def r_top_axis(self, x: int, y: int, available_spaces=None) -> list:
        if available_spaces is None:
            available_spaces = []
        abc = "0abcdefgh"
        if x > 8 or y > 8:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            available_spaces.append(tile)
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.r_top_axis(x + 1, y + 1, available_spaces)

    def r_bot_axis(self, x: int, y: int, available_spaces=None) -> list:
        if available_spaces is None:
            available_spaces = []
        abc = "0abcdefgh"
        if x > 8 or y == 0:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            available_spaces.append(tile)
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.r_bot_axis(x + 1, y - 1, available_spaces)

    def threatened_spaces(self):
        threatened = []
        diagonal_spaces = self.diagonal_movement()
        straight_spaces = self.straight_movement()
        for i in diagonal_spaces:
            threatened.append(i)
        for i in straight_spaces:
            threatened.append(i)
        return threatened

    def movement(self):
        return [x for x in self.threatened_spaces() if x.team != self.team]

    def eat_or_move(self, new_tile):
        self.movement()
        print(self.movement())
        if new_tile in self.movement():
            self.tile.team = None
            self.tile.occupied = False
            self.tile.piece = None
            self.tile.tag = None
            if new_tile.piece is not None:
                new_tile.piece.tile = None
            new_tile.piece = self
            new_tile.team = self.team
            new_tile.occupied = True
            new_tile.tag = self.tag
            self.tile = new_tile
        else:
            print(f"{self.tag} can't move towards {new_tile.coords} tile")


class King:
    available_moves = []

    def __init__(self, tile: object, team: str, number: int):
        self.tile = tile
        self.team = team
        self.number = number
        tile.occupied = True
        tile.team = team
        tile.piece = self
        self.check = False
        self.tag = "k"
        tile.tag = self.tag

    def __repr__(self):
        if self.team == "white":
            return f"\033[2;30;47m[   K   ]\033[0;0m"
        else:
            return f"\033[2;37;40m[   K   ]\033[0;0m"

    def threatened_spaces(self):
        King_x, King_y = self.tile.coords
        available_spaces = []
        spaces = []
        abc = "abcdefgh"
        for row in Board.board:
            for tile in row:
                x, y = tile.coords
                if x == King_x:
                    if y == King_y + 1 or y == King_y - 1:
                        available_spaces.append(tile)
                if abc.index(x) == abc.index(King_x) + 1:
                    if y == King_y or y == King_y + 1 or y == King_y - 1:
                        available_spaces.append(tile)
                if abc.index(x) == abc.index(King_x) - 1:
                    if y == King_y or y == King_y + 1 or y == King_y - 1:
                        available_spaces.append(tile)
        for i in available_spaces:
            spaces.append(i)
        return spaces

    def movement(self):
        not_team = set([x for x in self.threatened_spaces() if x.team != self.team])
        not_available = Board.threatened_space(self.team)
        actually_available = not_team.difference(not_available)
        return actually_available

    def check_checks(self):
        threatened = Board.threatened_space(self.team)
        if self.tile in threatened:
            self.check = True

    def eat_or_move(self, new_tile):
        self.movement()
        print(self.movement())
        if new_tile in self.movement():
            self.tile.team = None
            self.tile.occupied = False
            self.tile.piece = None
            self.tile.tag = None
            if new_tile.piece is not None:
                new_tile.piece.tile = None
            new_tile.piece = self
            new_tile.team = self.team
            new_tile.occupied = True
            new_tile.tag = self.tag
            self.tile = new_tile
        else:
            print(f"{self.tag} can't move towards {new_tile.coords} tile")


class Board:
    board: List[List[object]] = [[], [], [], [], [], [], [], []]
    x_coords = "abcdefgh"
    a = 9
    for row in board:
        a -= 1
        for i in range(8):
            row.append((Tile(x_coords[i], a, None, False)))
    white_king_check=False
    black_king_check=False

    def __init__(self):
        pass

    def __repr__(self):
        board = ""
        for row in Board.board:
            board = board + f"\n{row}"
        return board

    def play(self):
        color = "white"
        check_mate = False
        while not check_mate:
            letter, number, to, x, y = tuple(input(f"{color} move:"))
            place = Tile.tiles[(x, int(y))]
            for tile in Tile.tiles:
                this_tile = Tile.tiles[tile]
                piece = Tile.tiles[tile].piece
                if f"{letter}{number}" == this_tile.tag and this_tile.team == color:
                    piece.eat_or_move(place)
                    if not this_tile.occupied:
                        print(self)
                        if color == "white":
                            color = "black"
                        else:
                            color = "white"

    @staticmethod
    def threatened_space(color):
        threats = []
        for row in Board.board:
            for tile in row:
                if tile.occupied:
                    if tile.team != color:
                        piece_threats = tile.piece.threatened_spaces()
                        for i in piece_threats:
                            threats.append(i)
        return set(threats)

    def block_movement_while_in_check(self):
        for row in Board.board:
            for tile in row:
                if tile.occupied:
                    if tile.piece.tag=="k" and tile.piece.color=="black":
                        if tile.piece.check:
                            black_king_check=True
                    elif tile.piece.tag=="k" and tile.piece.color=="white":
                        if tile.piece.check
                            white_king_check=True


board1 = Board()
pawn1w = Pawn(Board.board[6][0], "white", 1)
pawn2w = Pawn(Board.board[6][1], "white", 2)
pawn3w = Pawn(Board.board[6][2], "white", 3)
pawn4w = Pawn(Board.board[6][3], "white", 4)
pawn5w = Pawn(Board.board[6][4], "white", 5)
pawn6w = Pawn(Board.board[6][5], "white", 6)
pawn7w = Pawn(Board.board[6][6], "white", 7)
pawn8w = Pawn(Board.board[6][7], "white", 8)
rook1w = Rook(Board.board[7][0], "white", 1)
rook2w = Rook(Board.board[7][7], "white", 2)
knight1w = Knight(Board.board[7][1], "white", 1)
knight2w = Knight(Board.board[7][6], "white", 2)
bishop1w = Bishop(Board.board[7][2], "white", 1)
bishop2w = Bishop(Board.board[7][5], "white", 2)
queenw = Queen(Board.board[7][3], "white", 1)
pawn1b = Pawn(Board.board[1][0], "black", 1)
pawn2b = Pawn(Board.board[1][1], "black", 2)
pawn3b = Pawn(Board.board[1][2], "black", 3)
pawn4b = Pawn(Board.board[1][3], "black", 4)
pawn5b = Pawn(Board.board[1][4], "black", 5)
pawn6b = Pawn(Board.board[1][5], "black", 6)
pawn7b = Pawn(Board.board[1][6], "black", 7)
pawn8b = Pawn(Board.board[1][7], "black", 8)
rook1b = Rook(Board.board[0][0], "black", 1)
rook2b = Rook(Board.board[0][7], "black", 2)
knight1b = Knight(Board.board[0][1], "black", 1)
knight2b = Knight(Board.board[0][6], "black", 2)
bishop1b = Bishop(Board.board[0][2], "black", 1)
bishop2b = Bishop(Board.board[0][5], "black", 2)

# print(board1)
# print(queenw.movement())

# KingW = King(Board.board[3][7], "white", 1)
# KingB = King(Board.board[0][4], "black", 1)
print(board1)
# print(Tile.tiles[("g", 5)].team)
# print(Tile.tiles[("g", 5)].occupied)
# print(Tile.tiles[("e", 5)].team)
# print(Tile.tiles[("e", 5)].occupied)
# print(rook1w.eat_or_move(Tile.tiles[("g", 5)]))
# print(board1)
# print(Tile.tiles[("g", 5)].team)
# print(Tile.tiles[("g", 5)].occupied)
# print(Tile.tiles[("e", 5)].team)
# print(Tile.tiles[("e", 5)].occupied)
# print(KingW.movement())
# Board.play()
# Board.play()
board1.play()
# print(KingW.movement())
# print(KingW.actual_movement())
