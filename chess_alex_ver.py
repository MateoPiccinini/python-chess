from __future__ import annotations
from typing import List, Set, Dict


class Tile:
    piece: object = None
    tiles: Dict[tuple, Tile] = {}

    def __init__(self, x_coordinate: str, y_coordinate: int, team: any, occupied: bool):
        self.coords = (x_coordinate, y_coordinate)
        self.team = team
        self.occupied = occupied
        Tile.tiles[self.coords] = self

    def __repr__(self) -> str:
        return f"[{self.coords}]" if self.piece is None else f"{self.piece}"


class Rook:
    def __init__(self, tile: any, team: str, number: int):
        self.tile = tile
        self.team = team
        self.number = number
        tile.occupied = True
        tile.team = team
        tile.piece = self

    def __repr__(self):
        if self.team == "white":
            return f"\033[2;30;47m[   ♖   ]\033[0;0m"
        else:
            return f"\033[2;37;40m[   ♖   ]\033[0;0m"

    def movement(self):
        moves=[]
        lateral_1=self.lateral_movement_1()
        lateral_2=self.lateral_movement_2()
        upwards=self.upwards_movement()
        downwards=self.downwards_movement()
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
        available_spaces=[]
        abc="abcdefgh"
        x,y=self.tile.coords
        i=True
        wanted_x=abc.index(x)+1
        if wanted_x == 8:
            i=False
        while i:
            new_tile=Tile.tiles[abc[wanted_x],y]
            if new_tile.occupied:
                if new_tile.team==self.team:
                    i=False
                else:
                    available_spaces.append(new_tile)
                    i=False
            else:
                available_spaces.append(new_tile)
                wanted_x+=1
            if wanted_x > 8:
                i = False
        return available_spaces
    def lateral_movement_2(self):
        available_spaces=[]
        abc="abcdefgh"
        x,y=self.tile.coords
        i=True
        wanted_x=abc.index(x)-1
        if wanted_x == -1:
            i = False
        while i:
            new_tile=Tile.tiles[abc[wanted_x],y]
            if new_tile.occupied:
                if new_tile.team==self.team:
                    i=False
                else:
                    available_spaces.append(new_tile)
                    i=False
            else:
                available_spaces.append(new_tile)
                wanted_x-=1
            if wanted_x < 0:
                i = False
        return available_spaces
    def upwards_movement(self):
        available_spaces = []
        x, y = self.tile.coords
        i = True
        wanted_y= y+1
        if wanted_y == 9:
            i = False
        while i:
            new_tile = Tile.tiles[x, wanted_y]
            if new_tile.occupied:
                if new_tile.team == self.team:
                    i = False
                else:
                    available_spaces.append(new_tile)
                    i = False
            elif new_tile.occupied==False:
                available_spaces.append(new_tile)
                wanted_y += 1
            if wanted_y > 8:
                i=False
        return available_spaces
    def downwards_movement(self):
        available_spaces = []
        x, y = self.tile.coords
        i = True
        wanted_y= y-1
        if wanted_y == 0:
            i = False
        while i:
            new_tile = Tile.tiles[x, wanted_y]
            if new_tile.occupied:
                if new_tile.team == self.team:
                    i = False
                else:
                    available_spaces.append(new_tile)
                    i = False
            elif new_tile.occupied==False:
                available_spaces.append(new_tile)
                wanted_y -= 1
                if wanted_y < 1:
                    i = False
        return available_spaces



class Knight:
    def __init__(self, tile: any, team: str, number: int):
        self.tile = tile
        self.team = team
        self.number = number
        tile.occupied = True
        tile.team = team
        tile.piece = self

    def __repr__(self):
        if self.team == "white":
            return f"\033[2;30;47m[   ♘   ]\033[0;0m"
        else:
            return f"\033[2;37;40m[   ♘   ]\033[0;0m"

    def movement_uncleansed(self):
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

    def movement(self):
        available_space = self.movement_uncleansed()
        actually_available_space = self.movement_uncleansed()
        for tile in available_space:
            if tile.occupied and tile.team == self.team:
                actually_available_space.remove(tile)
        return actually_available_space


class Pawn:

    def __init__(self, tile: object, team: str, number: int):
        self.tile = tile
        self.team = team
        self.number = number
        tile.occupied = True
        tile.team = team
        tile.piece = self

    def __repr__(self) -> str:
        if self.team == "white":
            return f"\033[2;30;47m[   ♙   ]\033[0;0m"
        else:
            return f"\033[2;37;40m[   ♙   ]\033[0;0m"

    def movement(self) -> Set:
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
                    if pawn_y == 2 and pawn_x == x and y == 4 and tile.team is None:  # w initial move
                        available_spaces.add(tile)
                    if pawn_x == x and y == pawn_y + 1 and tile.team is None:  # w Regular move
                        available_spaces.add(tile)

                # BLACK PAWN MOVEMENTS

                elif self.team == "black":
                    if tile.occupied == True and (abc.index(x) == abc.index(
                            pawn_x) + 1 and y == pawn_y - 1) and tile.team == "white":  # b right diagonal take
                        available_spaces.add(tile)
                    if tile.occupied == True and (abc.index(x) == abc.index(
                            pawn_x) - 1 and y == pawn_y - 1) and tile.team == "white":  # b left diagonal take
                        available_spaces.add(tile)
                    if pawn_y == 7 and pawn_x == x and y == 5 and tile.team is None:  # b initial move
                        available_spaces.add(tile)
                    if pawn_x == x and y == pawn_y - 1 and tile.team is None:  # b Regular move
                        available_spaces.add(tile)

        return available_spaces if available_spaces != set() else "No available spaces"


class Bishop:

    def __init__(self, tile: object, team: str, number: int):
        self.tile = tile
        self.team = team
        self.number = number
        tile.occupied = True
        tile.team = team
        tile.piece = self

    def __repr__(self) -> str:
        if self.team == "white":
            return f"\033[2;30;47m[   ♗   ]\033[0;0m"
        else:
            return f"\033[2;37;40m[   ♗   ]\033[0;0m"

    def movement(self) -> list:
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

    def l_top_axis(self, x: int, y: int, available_spaces: list = []) -> list:  # Spaces in top left axis
        abc = "0abcdefgh"
        if x == 0 or y == 9:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.l_top_axis(x - 1, y + 1, available_spaces)

    def l_bot_axis(self, x: int, y: int, available_spaces: list = []) -> list:  # Spaces in top left axis
        abc = "0abcdefgh"
        if x == 0 or y == 0:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.l_bot_axis(x - 1, y - 1, available_spaces)

    def r_top_axis(self, x: int, y: int, available_spaces: list = []) -> list:
        abc = "0abcdefgh"
        if x > 8 or y > 8:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.r_top_axis(x + 1, y + 1, available_spaces)

    def r_bot_axis(self, x: int, y: int, available_spaces: list = []) -> list:
        abc = "0abcdefgh"
        if x > 8 or y == 0:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.r_bot_axis(x + 1, y - 1, available_spaces)


class Queen:

    def __init__(self, tile: object, team: str, number: int):
        self.tile = tile
        self.team = team
        self.number = number
        tile.occupied = True
        tile.team = team
        tile.piece = self

    def __repr__(self):
        if self.team == "white":
            return f"\033[2;30;47m[   ♕   ]\033[0;0m"
        else:
            return f"\033[2;37;40m[   ♕   ]\033[0;0m"

    def straight_movement(self):
        moves=[]
        lateral_1=self.lateral_movement_1()
        lateral_2=self.lateral_movement_2()
        upwards=self.upwards_movement()
        downwards=self.downwards_movement()
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
        available_spaces=[]
        abc="abcdefgh"
        x,y=self.tile.coords
        i=True
        wanted_x=abc.index(x)+1
        if wanted_x == 8:
            i=False
        while i:
            new_tile=Tile.tiles[abc[wanted_x],y]
            if new_tile.occupied:
                if new_tile.team==self.team:
                    i=False
                else:
                    available_spaces.append(new_tile)
                    i=False
            else:
                available_spaces.append(new_tile)
                wanted_x+=1
            if wanted_x > 8:
                i = False
        return available_spaces
    def lateral_movement_2(self):
        available_spaces=[]
        abc="abcdefgh"
        x,y=self.tile.coords
        i=True
        wanted_x=abc.index(x)-1
        if wanted_x == -1:
            i = False
        while i:
            new_tile=Tile.tiles[abc[wanted_x],y]
            if new_tile.occupied:
                if new_tile.team==self.team:
                    i=False
                else:
                    available_spaces.append(new_tile)
                    i=False
            else:
                available_spaces.append(new_tile)
                wanted_x-=1
            if wanted_x < 0:
                i = False
        return available_spaces
    def upwards_movement(self):
        available_spaces = []
        x, y = self.tile.coords
        i = True
        wanted_y= y+1
        if wanted_y == 9:
            i = False
        while i:
            new_tile = Tile.tiles[x, wanted_y]
            if new_tile.occupied:
                if new_tile.team == self.team:
                    i = False
                else:
                    available_spaces.append(new_tile)
                    i = False
            elif new_tile.occupied==False:
                available_spaces.append(new_tile)
                wanted_y += 1
            if wanted_y > 8:
                i=False
        return available_spaces
    def downwards_movement(self):
        available_spaces = []
        x, y = self.tile.coords
        i = True
        wanted_y= y-1
        if wanted_y == 0:
            i = False
        while i:
            new_tile = Tile.tiles[x, wanted_y]
            if new_tile.occupied:
                if new_tile.team == self.team:
                    i = False
                else:
                    available_spaces.append(new_tile)
                    i = False
            elif new_tile.occupied==False:
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

    def l_top_axis(self, x: int, y: int, available_spaces: list = []) -> list:  # Spaces in top left axis
        abc = "0abcdefgh"
        if x == 0 or y == 9:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.l_top_axis(x - 1, y + 1, available_spaces)

    def l_bot_axis(self, x: int, y: int, available_spaces: list = []) -> list:  # Spaces in top left axis
        abc = "0abcdefgh"
        if x == 0 or y == 0:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.l_bot_axis(x - 1, y - 1, available_spaces)

    def r_top_axis(self, x: int, y: int, available_spaces: list = []) -> list:
        abc = "0abcdefgh"
        if x > 8 or y > 8:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.r_top_axis(x + 1, y + 1, available_spaces)

    def r_bot_axis(self, x: int, y: int, available_spaces: list = []) -> list:
        abc = "0abcdefgh"
        if x > 8 or y == 0:
            return available_spaces
        tile = Tile.tiles[(abc[x], y)]
        if tile.occupied == True and tile.team == self.team:
            return available_spaces
        elif tile.occupied == True and tile.team != self.team:
            available_spaces.append(tile)
            return available_spaces
        else:
            available_spaces.append(tile)
            return self.r_bot_axis(x + 1, y - 1, available_spaces)

    def movement(self):
        available_spaces = []
        diagonal_spaces = self.diagonal_movement()
        straight_spaces = self.straight_movement()
        for i in diagonal_spaces:
            available_spaces.append(i)
        for i in straight_spaces:
            available_spaces.append(i)
        return available_spaces


class King:

    def __init__(self, tile: object, team: str, number: int):
        self.tile = tile
        self.team = team
        self.number = number
        tile.occupied = True
        tile.team = team
        tile.piece = self

    def __repr__(self):
        return f"\033[2;30;47m[   K   ]\033[0;0m"
    def movement(self):
        King_x, King_y = self.tile.coords
        available_spaces = []
        spaces=set()
        color=self.team
        abc = "abcdefgh"
        x=abc.index(King_x)
        available_spaces.append(Tile.tiles[abc[x-1],King_y])
        available_spaces.append(Tile.tiles[abc[x - 1], King_y-1])
        available_spaces.append(Tile.tiles[abc[x - 1], King_y+1])
        available_spaces.append(Tile.tiles[abc[x], King_y+1])
        available_spaces.append(Tile.tiles[abc[x], King_y-1])
        available_spaces.append(Tile.tiles[abc[x + 1], King_y])
        available_spaces.append(Tile.tiles[abc[x + 1], King_y-1])
        available_spaces.append(Tile.tiles[abc[x + 1], King_y+1])
        for i in available_spaces:
            if i.occupied==False:
                spaces.add(i)
        not_available=Board.threatened_spaces(color)
        actually_available=spaces.difference(not_available)
        return actually_available




class Board:
    board: List[List[object]] = [[], [], [], [], [], [], [], []]
    x_coords = "abcdefgh"
    a = 9
    for row in board:
        a -= 1
        for i in range(8):
            row.append((Tile(x_coords[i], a, None, False)))

    def __init__(self):
        pass

    def __repr__(self):
        board = ""
        for row in Board.board:
            board = board + f"\n{row}"
        return board


    @staticmethod
    def threatened_spaces(color):
        threats=[]
        for row in Board.board:
            for tile in row:
                if tile.occupied:
                    if tile.team==color:
                        pass
                    else:
                        piece_threats=tile.piece.movement()
                        for i in piece_threats:
                            threats.append(i)
        empty_threats=[]
        for i in threats:
            if i.occupied==False:
                empty_threats.append(i)
        return set(empty_threats)



board1 = Board()
pawn1w = Pawn(Board.board[6][0], "white", 1)
pawn2w = Pawn(Board.board[6][1], "white", 1)
pawn3w = Pawn(Board.board[6][2], "white", 1)
pawn4w = Pawn(Board.board[6][3], "white", 1)
pawn5w = Pawn(Board.board[6][4], "white", 1)
pawn6w = Pawn(Board.board[6][5], "white", 1)
pawn7w = Pawn(Board.board[6][6], "white", 1)
pawn8w = Pawn(Board.board[6][7], "white", 1)
rook2w = Rook(Board.board[7][7], "white", 1)
knight1w = Knight(Board.board[7][1], "white", 1)
knight2w = Knight(Board.board[7][6], "white", 1)
bishop1w = Bishop(Board.board[3][5], "white", 1)
bishop2w = Bishop(Board.board[4][7], "white", 1)
queenw = Queen(Board.board[4][2], "white", 1)
pawn1b = Pawn(Board.board[1][0], "black", 1)
pawn2b = Pawn(Board.board[1][2], "black", 1)
pawn4b = Pawn(Board.board[1][3], "black", 1)
pawn6b = Pawn(Board.board[1][5], "black", 1)
pawn7b = Pawn(Board.board[1][6], "black", 1)
pawn8b = Pawn(Board.board[1][7], "black", 1)
rook1b = Rook(Board.board[0][0], "black", 1)
rook2b = Rook(Board.board[0][7], "black", 1)
knight1b = Knight(Board.board[0][1], "black", 1)
knight2b = Knight(Board.board[0][6], "black", 1)
bishop1b = Bishop(Board.board[4][6], "black", 1)
bishop2b = Bishop(Board.board[0][5], "black", 1)
kingb= King(Board.board[5][3],"white",1)
print(board1)
print(kingb.movement())
# print(bishop2b.available_spaces())
# pawn1 = Pawn(Board.board[5][4], "white", 1)
# pawn2 = Pawn(Board.board[6][2], "white", 1)
# pawn3 = Pawn(Board.board[5][3], "black", 1)
# pawn4 = Pawn(Board.board[4][2], "black", 1)
# rook1 = Rook(Board.board[4][4], "white", 1)
# pawn5 = Pawn(Board.board[4][7], "white", 1)
# rook2 = Rook(Board.board[2][4], "black", 1)
# knight1 = Knight(Board.board[1][2], "black", 1)
# bishop1 = Bishop(Board.board[4][6], "white", 1)
# print(pawn1.available_spaces())
# print(knight1.cleanse())
# print(pawn2.available_spaces())
# print(bishop1.available_spaces())

