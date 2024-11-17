from enum import Enum
from typing import List


class Orientation(Enum):
    Horizontal = 1
    Vertical = 2


class Corner(Enum):
    Top = 1
    Botton = 2
    Left = 3
    Right = 4


class Ship:
    def __init__(self, tamano: int, orientation: Orientation):
        self.tamano = tamano
        self.orientation = orientation

    def change_orientation(self):
        if self.orientation == Orientation.Horizontal:
            self.orientation = Orientation.Vertical
        else:
            self.orientation = Orientation.Horizontal

    def get_boxes_to_occupy(self, i: int, j: int):
        if self.orientation == Orientation.Horizontal:
            return [(i, j + k) for k in range(self.tamano)]
        else:
            return [(i + k, j) for k in range(self.tamano)]


class Tablero:
    def __init__(
        self, n: int, m: int, demandas_filas: List[int], demandas_columnas: List[int]
    ):
        self.n = n
        self.m = m
        self.demandas_filas = demandas_filas
        self.demandas_columnas = demandas_columnas
        self.ocuppied_boxes: set = set()

    def position_ship(self, ship: Ship, i: int, j: int):
        boxes = ship.get_boxes_to_occupy(i, j)
        for box in boxes:
            if box in self.ocuppied_boxes:
                return False
            if (box[0] < 0) or (box[0] >= self.n) or (box[1] < 0) or (box[1] >= self.m):
                return False
            if self.is_prohibited_by_neighbours(ship.orientation, box[0], box[1]):
                return False
            if not self.is_available_on_demand(box[0], box[1]):
                return False
        orientation = ship.orientation
        if orientation == Orientation.Horizontal:
            if self.is_prohibited_by_neighbours_on_corners(Corner.Left, boxes[0][0], boxes[0][1]):
                return False
            if self.is_prohibited_by_neighbours_on_corners(Corner.Right, boxes[-1][0], boxes[-1][1]):
                return False
        else:
            if self.is_prohibited_by_neighbours_on_corners(Corner.Botton, boxes[0][0], boxes[0][1]):
                return False
            if self.is_prohibited_by_neighbours_on_corners(Corner.Top, boxes[-1][0], boxes[-1][1]):
                return False
        for box in boxes:
            self.ocuppied_boxes.add(box)
            self.demandas_filas[box[0]] -= 1
            self.demandas_columnas[box[1]] -= 1
        return True

    def is_available_on_demand(self, i: int, j: int):
        return self.demandas_filas[i] > 0 and self.demandas_columnas[j] > 0

    def is_prohibited_by_neighbours(self, orientation: Orientation, i: int, j: int):
        if orientation == Orientation.Horizontal:
            if (i - 1 >= 0 and (i - 1, j) in self.ocuppied_boxes) or (
                i + 1 < self.n and (i + 1, j) in self.ocuppied_boxes
            ):
                return True
        else:
            if (j - 1 >= 0 and (i, j - 1) in self.ocuppied_boxes) or (
                j + 1 < self.m and (i, j + 1) in self.ocuppied_boxes
            ):
                return True

    def is_prohibited_by_neighbours_on_corners(self, corner: Corner, i: int, j: int):
        if corner == Corner.Top:
            if (
                (self.n and (i - 1, j - 1) in self.ocuppied_boxes)
                or (self.m and (i - 1, j + 1) in self.ocuppied_boxes)
                or (self.n and (i - 1, j) in self.ocuppied_boxes)
            ):
                return True
        elif corner == Corner.Botton:
            if (
                (self.n and (i + 1, j - 1) in self.ocuppied_boxes)
                or (self.m and (i + 1, j + 1) in self.ocuppied_boxes)
                or (self.n and (i + 1, j) in self.ocuppied_boxes)
            ):
                return True
        elif corner == Corner.Left:
            if (
                (self.n and (i - 1, j - 1) in self.ocuppied_boxes)
                or (self.m and (i + 1, j - 1) in self.ocuppied_boxes)
                or (self.m and (i, j - 1) in self.ocuppied_boxes)
            ):
                return True
        elif corner == Corner.Right:
            if (
                (self.n and (i - 1, j + 1) in self.ocuppied_boxes)
                or (self.m and (i + 1, j + 1) in self.ocuppied_boxes)
                or (self.m and (i, j + 1) in self.ocuppied_boxes)
            ):
                return True
        return False

    def remove_ship(self, ship: Ship, i: int, j: int):
        boxes = ship.get_boxes_to_occupy(i, j)
        for box in boxes:
            self.ocuppied_boxes.remove(box)
            self.demandas_filas[box[0]] += 1
            self.demandas_columnas[box[1]] += 1

    def __str__(self):
        board_str = ""
        for i in range(self.n):
            for j in range(self.m):
                if (i, j) in self.ocuppied_boxes:
                    board_str += "X "
                else:
                    board_str += "O "
            board_str += "\n"
        return board_str


def batalla_naval(
    barcos: List[int], demandas_filas: List[int], demandas_columnas: List[int]
):
    barcos = sorted(barcos, reverse=True)
    n = len(demandas_filas)
    m = len(demandas_columnas)
    board = Tablero(n, m, demandas_filas, demandas_columnas)
    best_solution: list = []
    batalla_naval_BT(board, barcos, 0, best_solution)
    return best_solution


def batalla_naval_BT(
    board: Tablero,
    ships: List[int],
    current_ship: int = 0,
    best_solution: List = [],
):
    n = board.n
    m = board.m

    if current_ship >= len(ships):
        best_solution.append(board.ocuppied_boxes.copy())
        print(board)
        return

    ship = ships[current_ship]

    for i in range(n):
        for j in range(m):
            for orientation in [Orientation.Horizontal, Orientation.Vertical]:
                # print(f"Ship: {ship}, i: {i}, j: {j}, orientation: {orientation}")
                ship_i_j = Ship(ship, orientation)
                if board.position_ship(ship_i_j, i, j):
                    batalla_naval_BT(board, ships, current_ship + 1, best_solution)
                    board.remove_ship(ship_i_j, i, j)


if __name__ == "__main__":
    barcos = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    demandas_filas = [0, 3, 2, 1, 1, 2, 4, 2, 2, 3]
    demandas_columnas = [0, 5, 1, 3, 2, 2, 3, 1, 2, 1]
    result = batalla_naval(barcos, demandas_filas[::-1], demandas_columnas)
    for box in result:
        print(box)

    # barcos = [1, 1, 1, 1]
    # demandas_filas = [2, 0, 2]
    # demandas_columnas = [2, 0, 2]
    # result = batalla_naval(barcos, demandas_filas[::-1], demandas_columnas[::-1])
    # # for box in result:
    #     print(box)

    # barcos = [5, 5, 5]
    # demandas_filas = [5, 5, 5, 5, 5]
    # demandas_columnas = [5, 5, 5, 5, 5]
    # result = batalla_naval(barcos, demandas_filas[::-1], demandas_columnas[::-1])
    # for box in result:
    #     print(box)

    # barcos = [2]
    # demandas_filas = [1, 1]
    # demandas_columnas = [1, 1]
    # result = batalla_naval(barcos, demandas_filas[::-1], demandas_columnas[::-1])
    # for box in result:
    #     print(box)