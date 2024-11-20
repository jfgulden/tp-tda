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


def get_better_order_to_iterate(demad: list):
    return [
        indice
        for valor, indice in sorted(
            (valor, indice) for indice, valor in enumerate(demad)
        )
    ]


class Tablero:
    def __init__(
        self, n: int, m: int, demands_rows: List[int], demands_columns: List[int]
    ):
        self.n = n
        self.m = m
        self.demands_rows = demands_rows
        self.demands_columns = demands_columns
        self.ocuppied_boxes: set = set()
        # self.order_to_iterate_rows = get_better_order_to_iterate(demands_rows)[::-1]
        # self.order_to_iterate_columns = get_better_order_to_iterate(demands_columns)[::-1]
        self.order_to_iterate_rows = list(range(n))
        self.order_to_iterate_columns = list(range(m))

    def position_ship(self, ship: Ship, i: int, j: int):
        boxes = ship.get_boxes_to_occupy(i, j)
        if ship.orientation == Orientation.Horizontal:
            if len(boxes) > self.demands_rows[i]:
                return False
        else:
            if len(boxes) > self.demands_columns[j]:
                return False

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

    def is_prohibited_by_neighbours(self, orientation: Orientation, i: int, j: int):
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

    def is_prohibited_by_neighbours_on_corners(self, corner: Corner, i: int, j: int):
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

    # def __str__(self):
    #     board_str = ""
    #     for i in range(self.n):
    #         for j in range(self.m):
    #             if (i, j) in self.ocuppied_boxes:
    #                 board_str += "X "
    #             else:
    #                 board_str += "O "
    #         board_str += "\n"
    #     return board_str

    # A un costado pondre la demanda de las filas y arriba la demanda de las columnas
    def __str__(self):
        board_str = ""
        for i in range(self.n):
            board_str += f"{self.demands_rows[i]}| "
            for j in range(self.m):
                if (i, j) in self.ocuppied_boxes:
                    board_str += "X "
                else:
                    board_str += "O "
            board_str += "\n"
        board_str += "  "
        for j in range(self.m):
            board_str += f"{self.demands_columns[j]} "
        return board_str

    def get_maximal_demand(self):
        return max(max(self.demands_rows), max(self.demands_columns))

    def get_available_demand(self):
        return sum(self.demands_rows) + sum(self.demands_columns)


class BestSolution:
    def __init__(self):
        self.ocuppied_boxes = set()
        self.remaining_demand = float("inf")

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
        remaining_demand = f"Remaining demand: {self.remaining_demand}"
        return ocuppied_boxes + remaining_demand


# []


def is_better_solution_possible(board, ships, current_ship, best_solution):
    remaining_ships = sum(ships[current_ship:])
    best_atteinable_solution = board.get_available_demand() - remaining_ships * 2
    if (
        len(best_solution.ocuppied_boxes) > 0
        and best_atteinable_solution >= best_solution.remaining_demand
    ):
        return False  # Ojo
    max_demand = board.get_maximal_demand()
    valid_ships = [value for value in ships[current_ship:] if value <= max_demand]
    best_atteinable_solution = board.get_available_demand() - sum(valid_ships) * 2
    if (
        len(best_solution.ocuppied_boxes) > 0
        and best_atteinable_solution >= best_solution.remaining_demand
    ):
        return False


    # if (
    #     len(best_solution.ocuppied_boxes) > 0
    #     and best_atteinable_solution < 0
    # ):
    #     return False
    # if (
    #     len(best_solution.ocuppied_boxes) > 0
    #     and best_atteinable_solution == 0
    #     and board.get_maximal_demand() < ships[current_ship]
    # ):
    #     return False
    return True


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
    i_start: int = -1,
    j_start: int = -1,
):

    n = board.n
    m = board.m

    if current_ship >= len(ships):
        if best_solution.compare_solution(board):
            print("a")
            # print(board)
            # print("\n\n")
        return

    ship = ships[current_ship]

    if not is_better_solution_possible(board, ships, current_ship, best_solution):
        return

    if board.get_maximal_demand() < ship:
        return batalla_naval_BT(board, ships, current_ship + 1, best_solution)

    if i_start != -1:
        i_range = range(i_start, n)
    else:
        i_range = range(n)

    if j_start != -1:
        j_range = range(j_start, m)
    else:
        j_range = range(m)

    for i in i_range:
        if board.demands_rows[i] == 0:
            continue
        for j in j_range:
            if board.demands_columns[j] == 0:
                continue
            for orientation in [Orientation.Horizontal, Orientation.Vertical]:
                ship_i_j = Ship(ship, orientation)
                if board.position_ship(ship_i_j, i, j):
                    if len(ships) > current_ship + 1 and ships[current_ship + 1] == ship:
                        batalla_naval_BT(board, ships, current_ship + 1, best_solution, i, j)
                    else:
                        batalla_naval_BT(board, ships, current_ship + 1, best_solution)
                    board.remove_ship(ship_i_j, i, j)

    while current_ship < len(ships) and ships[current_ship] == ship:
        current_ship += 1
    batalla_naval_BT(board, ships, current_ship, best_solution)


if __name__ == "__main__":
    tablero, barcos, demands_rows, demands_columns = parsear_archivo(
        "./archivos_pruebas/TP3/3_3_2.txt"
    )
    start_time = time.time()
    result = batalla_naval(barcos, demands_rows, demands_columns)
    end_time = time.time()
    print("Board: 3_3_2.txt")
    print(f"Execution time: {end_time - start_time}")
    print(
        f"Demand fullfilled: {sum(demands_rows) + sum(demands_columns) - result.remaining_demand}"
    )
    print(f"Result: {result}")
    print("\n\n")

    tablero, barcos, demands_rows, demands_columns = parsear_archivo(
        "./archivos_pruebas/TP3/5_5_6.txt"
    )
    print(barcos)
    start_time = time.time()
    result = batalla_naval(barcos, demands_rows, demands_columns)
    end_time = time.time()
    print("Board: 5_5_6.txt")
    print(f"Execution time: {end_time - start_time}")
    print(
        f"Demand fullfilled: {sum(demands_rows) + sum(demands_columns) - result.remaining_demand}"
    )
    print(f"Result: {result}")
    print("\n\n")

    tablero, barcos, demands_rows, demands_columns = parsear_archivo(
        "./archivos_pruebas/TP3/8_7_10.txt"
    )
    print(barcos)
    start_time = time.time()
    result = batalla_naval(barcos, demands_rows, demands_columns)
    end_time = time.time()
    print("Board: 8_7_10.txt")
    print(f"Execution time: {end_time - start_time}")
    print(
        f"Demand fullfilled: {sum(demands_rows) + sum(demands_columns) - result.remaining_demand}"
    )
    print(f"Result: {result}")
    print("\n\n")

    tablero, barcos, demands_rows, demands_columns = parsear_archivo(
        "./archivos_pruebas/TP3/10_3_3.txt"
    )
    print(barcos)
    start_time = time.time()
    result = batalla_naval(barcos, demands_rows, demands_columns)
    end_time = time.time()
    print("Board: 10_3_3.txt")
    print(f"Execution time: {end_time - start_time}")
    print(
        f"Demand fullfilled: {sum(demands_rows) + sum(demands_columns) - result.remaining_demand}"
    )
    print(f"Result: {result}")
    print("\n\n")

    tablero, barcos, demands_rows, demands_columns = parsear_archivo(
        "./archivos_pruebas/TP3/10_10_10.txt"
    )
    print(barcos)
    start_time = time.time()
    result = batalla_naval(barcos, demands_rows, demands_columns)
    end_time = time.time()
    print("Board: 10_10_10.txt")
    print(f"Execution time: {end_time - start_time}")
    print(
        f"Demand fullfilled: {sum(demands_rows) + sum(demands_columns) - result.remaining_demand}"
    )
    print(f"Result: {result}")
    print("\n\n")

    tablero, barcos, demands_rows, demands_columns = parsear_archivo(
        "./archivos_pruebas/TP3/12_12_21.txt"
    )
    print(barcos)
    start_time = time.time()
    result = batalla_naval(barcos, demands_rows, demands_columns)
    end_time = time.time()
    print("Board: 12_12_21.txt")
    print(f"Execution time: {end_time - start_time}")
    print(
        f"Demand fullfilled: {sum(demands_rows) + sum(demands_columns) - result.remaining_demand}"
    )
    print(f"Result: {result}")
    print("\n\n")

    tablero, barcos, demands_rows, demands_columns = parsear_archivo(
        "./archivos_pruebas/TP3/15_10_15.txt"
    )
    print(barcos)
    start_time = time.time()
    result = batalla_naval(barcos, demands_rows, demands_columns)
    end_time = time.time()
    print("Board: 15_10_15.txt")
    print(f"Execution time: {end_time - start_time}")
    print(
        f"Demand fullfilled: {sum(demands_rows) + sum(demands_columns) - result.remaining_demand}"
    )
    print(f"Result: {result}")
    print("\n\n")

    tablero, barcos, demands_rows, demands_columns = parsear_archivo(
        "./archivos_pruebas/TP3/20_20_20.txt"
    )
    print(barcos)
    start_time = time.time()
    result = batalla_naval(barcos, demands_rows, demands_columns)
    end_time = time.time()
    print("Board: 20_20_20.txt")
    print(f"Execution time: {end_time - start_time}")
    print(
        f"Demand fullfilled: {sum(demands_rows) + sum(demands_columns) - result.remaining_demand}"
    )
    print(f"Result: {result}")
    print("\n\n")

    tablero, barcos, demands_rows, demands_columns = parsear_archivo(
        "./archivos_pruebas/TP3/20_25_30.txt"
    )
    print(barcos)
    start_time = time.time()
    result = batalla_naval(barcos, demands_rows, demands_columns)
    end_time = time.time()
    print("Board: 20_25_30.txt")
    print(f"Execution time: {end_time - start_time}")
    print(
        f"Demand fullfilled: {sum(demands_rows) + sum(demands_columns) - result.remaining_demand}"
    )
    print(f"Result: {result}")
    print("\n\n")

    tablero, barcos, demands_rows, demands_columns = parsear_archivo(
        "./archivos_pruebas/TP3/30_25_25.txt"
    )
    print(barcos)
    start_time = time.time()
    result = batalla_naval(barcos, demands_rows, demands_columns)
    end_time = time.time()
    print("Board: 30_25_25.txt")
    print(f"Execution time: {end_time - start_time}")
    print(
        f"Demand fullfilled: {sum(demands_rows) + sum(demands_columns) - result.remaining_demand}"
    )
    print(f"Result: {result}")
    print("\n\n")
