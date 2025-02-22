import sys
from enum import Enum
from typing import List
import sys
import time


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
        self.placed_positions = {}
        self.occupied_boxes = set()

    def position_ship(self, ship: Ship, i: int, j: int, ship_pos: int):
        boxes = ship.get_boxes_to_occupy(i, j)
        if ship.orientation == Orientation.Horizontal:
            if len(boxes) > self.demands_rows[i]:
                return False
        else:
            if len(boxes) > self.demands_columns[j]:
                return False

        for box in boxes:
            if box in self.occupied_boxes:
                return False
            x = box[0]
            y = box[1]
            if (x < 0) or (x >= self.n) or (y < 0) or (y >= self.m):
                return False
            if self.is_prohibited_by_neighbours(ship.orientation, x, y):
                return False
            if not self.is_available_on_demand(x, y):
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
            
        if ship_pos not in self.placed_positions:
            self.placed_positions[ship_pos] = set()
            
        for box in boxes:
            self.placed_positions[ship_pos].add(box)
            self.occupied_boxes.add(box)
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
            if ((i - 1, j) in self.occupied_boxes) or (
                ((i + 1, j) in self.occupied_boxes)
            ):
                return True
        else:
            if ((i, j - 1) in self.occupied_boxes) or (
                ((i, j + 1) in self.occupied_boxes)
            ):
                return True

    def is_prohibited_by_neighbours_on_corners(self,
                                               corner: Corner,
                                               i: int,
                                               j: int):
        if corner == Corner.Top:
            if (
                (self.n and (i + 1, j - 1) in self.occupied_boxes)
                or (self.m and (i + 1, j + 1) in self.occupied_boxes)
                or (self.n and (i + 1, j) in self.occupied_boxes)
            ):
                return True
        elif corner == Corner.Botton:
            if (
                (self.n and (i - 1, j - 1) in self.occupied_boxes)
                or (self.m and (i - 1, j + 1) in self.occupied_boxes)
                or (self.n and (i - 1, j) in self.occupied_boxes)
            ):
                return True
        elif corner == Corner.Left:
            if (
                (self.n and (i - 1, j - 1) in self.occupied_boxes)
                or (self.m and (i + 1, j - 1) in self.occupied_boxes)
                or (self.m and (i, j - 1) in self.occupied_boxes)
            ):
                return True
        elif corner == Corner.Right:
            if (
                (self.n and (i - 1, j + 1) in self.occupied_boxes)
                or (self.m and (i + 1, j + 1) in self.occupied_boxes)
                or (self.m and (i, j + 1) in self.occupied_boxes)
            ):
                return True
        return False

    def remove_ship(self, ship: Ship, i: int, j: int, ship_pos: int):
        boxes = ship.get_boxes_to_occupy(i, j)
        self.placed_positions.pop(ship_pos)
        for box in boxes:
            self.occupied_boxes.remove(box)
            self.demands_rows[box[0]] += 1
            self.demands_columns[box[1]] += 1

    def __str__(self):
        board_str = ""
        for i in range(self.n):
            board_str += f"{self.demands_rows[i]}| "
            for j in range(self.m):
                if (i, j) in self.occupied_boxes:
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
        self.placed_positions = {}
        self.occupied_boxes = set()
        self.remaining_demand = float("inf")

    def update_solution(self, board: Tablero):
        self.occupied_boxes = board.occupied_boxes.copy()
        self.remaining_demand = board.get_available_demand()
        self.placed_positions = board.placed_positions.copy()

    def compare_solution(self, board: Tablero):
        if board.get_available_demand() < self.remaining_demand:
            self.occupied_boxes = board.occupied_boxes.copy()
            self.remaining_demand = board.get_available_demand()
            self.placed_positions = board.placed_positions.copy()
            return True
        return False

    def __str__(self):
        occupied_boxes = f"occupied boxes: {self.occupied_boxes}\n"
        remaining_demand = f"Remaining demand: {self.remaining_demand}"
        return occupied_boxes + remaining_demand


def is_better_solution_possible(board, ships, current_ship, best_solution):
    remaining_ships = sum(ships[current_ship:])
    best_atteinable_solution = board.get_available_demand() - remaining_ships * 2
    if (
        len(best_solution.occupied_boxes) > 0
        and best_atteinable_solution >= best_solution.remaining_demand
    ):
        return False
    max_demand = board.get_maximal_demand()
    valid_ships = [value for value in ships[current_ship:] if value <= max_demand]
    best_atteinable_solution = (
            board.get_available_demand() - sum(valid_ships) * 2
        )
    if (
        len(best_solution.occupied_boxes) > 0
        and best_atteinable_solution >= best_solution.remaining_demand
    ):
        return False
    return True
def naval_battle(
    barcos: List[int], demands_rows: List[int], demands_columns: List[int]
):

    barcos = sorted(barcos, reverse=True)
    n = len(demands_rows)
    m = len(demands_columns)
    board = Tablero(n, m, demands_rows, demands_columns)
    best_solution = BestSolution()
    naval_battle_BT(board, barcos, 0, best_solution)
    return best_solution


def naval_battle_BT(
    board: Tablero,
    ships: List[int],
    current_ship: int,
    best_solution: BestSolution,
    i_start: int = 0,
    j_start: int = 0,
):

    n = board.n
    m = board.m

    if current_ship >= len(ships):
        best_solution.compare_solution(board)
        return

    ship = ships[current_ship]

    if not is_better_solution_possible(
        board, ships, current_ship, best_solution
    ):
        return

    if board.get_maximal_demand() < ship:
        return naval_battle_BT(board, ships, current_ship + 1, best_solution)

    for i in range(i_start, n):
        if board.demands_rows[i] == 0:
            continue
        for j in range(0, m):
            if i == i_start and j < j_start:
                continue
            if board.demands_columns[j] == 0:
                continue
            for orientation in [Orientation.Horizontal, Orientation.Vertical]:
                ship_i_j = Ship(ship, orientation)
                if board.position_ship(ship_i_j, i, j, current_ship):
                    if (
                        len(ships) > current_ship + 1
                        and ships[current_ship + 1] == ship
                    ):
                        naval_battle_BT(
                            board, ships, current_ship + 1, best_solution, i, j
                        )
                    else:
                        naval_battle_BT(
                            board, ships, current_ship + 1, best_solution
                        )
                    board.remove_ship(ship_i_j, i, j, current_ship)

    while current_ship < len(ships) and ships[current_ship] == ship:
        current_ship += 1
    naval_battle_BT(board, ships, current_ship, best_solution)
    
def parsear_archivo(filepath: str) -> tuple[list[int], list[int], list[int]]:
    with open(filepath, "r") as file:
        i = 0
        demandas_filas = []
        demandas_columnas = []
        barcos = []

        for index, line in enumerate(file):
            if index < 2:
                continue
            if line.strip() == "":
                i += 1
                continue
            if i == 0:
                demandas_filas.append(int(line.strip()))
            elif i == 1:
                demandas_columnas.append(int(line.strip()))
            elif i == 2:
                barcos.append(int(line.strip()))

    return barcos, demandas_filas, demandas_columnas

def display_board(best_sol: BestSolution, ships: List[int], n: int, m: int):
    print()
    for i, ship in enumerate(ships):
        if i in best_sol.placed_positions:
            print(f"Barco {i} de tamaño {ship}: {best_sol.placed_positions[i]}")
        else:
            print(f"Barco {i} de tamaño {ship}: No fue colocado")
           
    print("\nDispoción de los barcos en el tablero:")
    print("\nX: casilla ocupada")
    print("O: casilla libre\n")
    board_str = "   " + " ".join(f"{i:2}" for i in range(m)) + "\n\n"

    for i in range(n):
        board_str += f"{i:2} "
        for j in range(m):
            X = f"{' X' if n <= 10 else ' X '}"
            O = f"{' O' if n <= 10 else ' O '}"
            board_str += X if (i, j) in best_sol.occupied_boxes else O
        board_str += "\n"
        
    print(board_str)

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("La cantidad de argumentos es incorrecta")
        print("Uso: python3 backtracking.py <archivo_prueba>")
        sys.exit()
    
    start_time = time.time()
    barcos, demands_rows, demands_columns = parsear_archivo(sys.argv[1])
    resultado = naval_battle(barcos, demands_rows, demands_columns)
    demand_fullfilled = (
        sum(demands_rows) + sum(demands_columns) - resultado.remaining_demand
    )
    end_time = time.time()  
    display_board(resultado, barcos, len(demands_rows), len(demands_columns))
    print(f"Demanda total: {sum(demands_rows) + sum(demands_columns)}")
    print(f"Demanda cumplida: {demand_fullfilled}")
    print(f"Demanda incumplida: {resultado.remaining_demand}")
    print(f"Tiempo de ejecución: {end_time - start_time:.6f} segundos")
