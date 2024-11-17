from enum import Enum
import time
from typing import List
from backtracking import parsear_archivo


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
        self,
        n: int,
        m: int,
        demands_rows: List[int],
        demands_columns: List[int]
    ):
        self.n = n
        self.m = m
        self.demands_rows = demands_rows
        self.demands_columns = demands_columns
        self.ocuppied_boxes: set = set()

    def position_ship(self, ship: Ship, i: int, j: int):
        boxes = ship.get_boxes_to_occupy(i, j)
        for box in boxes:
            if box in self.ocuppied_boxes:
                return False
            if (box[0] < 0) or (box[0] >= self.n) or\
                    (box[1] < 0) or (box[1] >= self.m):
                return False
            if self.is_prohibited_by_neighbours(
                    ship.orientation, box[0], box[1]):
                return False
            if not self.is_available_on_demand(box[0], box[1]):
                return False
        orientation = ship.orientation
        if orientation == Orientation.Horizontal:
            if self.is_prohibited_by_neighbours_on_corners(
                Corner.Left, boxes[0][0], boxes[0][1]
            ):
                return False
            if self.is_prohibited_by_neighbours_on_corners(
                Corner.Right, boxes[-1][0], boxes[-1][1]
            ):
                return False
        else:
            if self.is_prohibited_by_neighbours_on_corners(
                Corner.Botton, boxes[0][0], boxes[0][1]
            ):
                return False
            if self.is_prohibited_by_neighbours_on_corners(
                Corner.Top, boxes[-1][0], boxes[-1][1]
            ):
                return False
        for box in boxes:
            self.ocuppied_boxes.add(box)
            self.demands_rows[box[0]] -= 1
            self.demands_columns[box[1]] -= 1
        return True

    def is_available_on_demand(self, i: int, j: int):
        return self.demands_rows[i] > 0 and self.demands_columns[j] > 0

    def is_prohibited_by_neighbours(self,
                                    orientation: Orientation,
                                    i: int,
                                    j: int):
        if orientation == Orientation.Horizontal:
            if ((i - 1, j) in self.ocuppied_boxes) or (
                ((i + 1, j) in self.ocuppied_boxes)
            ):
                return True
        else:
            if ((i, j - 1) in self.ocuppied_boxes) or (
                ((i, j + 1) in self.ocuppied_boxes)
            ):
                return True

    def is_prohibited_by_neighbours_on_corners(self,
                                               corner: Corner,
                                               i: int,
                                               j: int):
        if corner == Corner.Top:
            if (
                (self.n and (i + 1, j - 1) in self.ocuppied_boxes)
                or (self.m and (i + 1, j + 1) in self.ocuppied_boxes)
                or (self.n and (i + 1, j) in self.ocuppied_boxes)
            ):
                return True
        elif corner == Corner.Botton:
            if (
                (self.n and (i - 1, j - 1) in self.ocuppied_boxes)
                or (self.m and (i - 1, j + 1) in self.ocuppied_boxes)
                or (self.n and (i - 1, j) in self.ocuppied_boxes)
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
            self.demands_rows[box[0]] += 1
            self.demands_columns[box[1]] += 1

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

    def get_maximal_demand(self):
        return max(max(self.demands_rows), max(self.demands_columns))

    def get_available_demand(self):
        return sum(self.demands_rows) + sum(self.demands_columns)


class BestSolution:
    def __init__(self):
        self.ocuppied_boxes = set()
        self.remaining_demand = float('inf')

    def update_solution(self, board: Tablero):
        self.ocuppied_boxes = board.ocuppied_boxes.copy()
        self.remaining_demand = board.get_available_demand()

    def compare_solution(self, board: Tablero):
        if board.get_available_demand() < self.remaining_demand:
            self.ocuppied_boxes = board.ocuppied_boxes.copy()
            self.remaining_demand = board.get_available_demand()
            return True
        return False

    def __str__(self):
        ocuppied_boxes = f"Ocuppied boxes: {self.ocuppied_boxes}\n"
        remaining_demand = f"Remaining demand: {self.remaining_demand}\n"
        return ocuppied_boxes + remaining_demand


def batalla_naval(
    barcos: List[int], demands_rows: List[int], demands_columns: List[int]
):
    barcos = sorted(barcos, reverse=True)
    n = len(demands_rows)
    m = len(demands_columns)
    board = Tablero(n, m, demands_rows, demands_columns)
    best_solution = BestSolution()
    batalla_naval_BT(board, barcos, 0, best_solution)
    return best_solution


def batalla_naval_BT(
    board: Tablero,
    ships: List[int],
    current_ship: int,
    best_solution: BestSolution,
):
    n = board.n
    m = board.m

    if current_ship >= len(ships):
        if best_solution.compare_solution(board):
            print(board)
            print("\n\n")
        return

    ship = ships[current_ship]

    if board.get_maximal_demand() < ship:
        return batalla_naval_BT(board, ships, current_ship + 1, best_solution)

    remaining_ships = sum(ships[current_ship:])
    possible_demand = board.get_available_demand() - remaining_ships * 2
    if possible_demand > best_solution.remaining_demand:
        return

    for i in range(n):
        for j in range(m):
            for orientation in [Orientation.Horizontal, Orientation.Vertical]:
                # print(f"Ship: {ship}, i: {i}, j: {j}, orientation: {orientation}")
                ship_i_j = Ship(ship, orientation)
                if board.position_ship(ship_i_j, i, j):
                    batalla_naval_BT(board, ships, current_ship + 1, best_solution)
                    board.remove_ship(ship_i_j, i, j)
    batalla_naval_BT(board, ships, current_ship + 1, best_solution)


if __name__ == "__main__":
    # barcos = [1, 1, 1, 1, 2, 2, 2,3, 3, 4]
    # demands_rows = [0, 3, 2, 1, 1, 2, 4, 2, 2, 3]
    # demands_columns = [0, 5, 1, 3, 2, 2, 3, 1, 2, 1]
    # start_time = time.time()
    # result = batalla_naval(barcos, demands_rows[::-1], demands_columns)
    # end_time = time.time()
    # print(f"Execution time: {end_time - start_time}")
    # print(result)

    # for box in result:
    #     print(box)

    # barcos = [1, 1, 1, 1]
    # demands_rows = [2, 0, 2]
    # demands_columns = [2, 0, 2]
    # result = batalla_naval(barcos, demands_rows[::-1], demands_columns[::-1])
    # # # for box in result:
    # #     print(box)

    # barcos = [5, 5, 5]
    # demands_rows = [5, 5, 5, 5, 5]
    # demands_columns = [5, 5, 5, 5, 5]
    # result = batalla_naval(barcos, demands_rows[::-1], demands_columns[::-1])
    # for box in result:
    #     print(box)

    # barcos = [1, 2]
    # demands_rows = [1, 1]
    # demands_columns = [1, 1]
    # result = batalla_naval(barcos, demands_rows[::-1], demands_columns[::-1])
    # for box in result:
    #     print(box)

    tablero, barcos, demands_rows, demands_columns = parsear_archivo("./30_25_25.txt")
    start_time = time.time()
    result = batalla_naval(barcos, demands_rows[::-1], demands_columns)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time}")
    print(result)
