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
        self.ocuppied_boxes: set = set()

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


def is_better_solution_possible(board, ships, current_ship, best_solution):
    remaining_ships = sum(ships[current_ship:])
    best_atteinable_solution = board.get_available_demand() - remaining_ships * 2
    if (
        len(best_solution.ocuppied_boxes) > 0
        and best_atteinable_solution >= best_solution.remaining_demand
    ):
        return False
    max_demand = board.get_maximal_demand()
    valid_ships = [value for value in ships[current_ship:] if value <= max_demand]
    best_atteinable_solution = (
            board.get_available_demand() - sum(valid_ships) * 2
        )
    if (
        len(best_solution.ocuppied_boxes) > 0
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
        range_j = range(j_start, m) if i == i_start else range(0, m)
        for j in range(0, m):
            if i == i_start and j < j_start:
                continue
            if board.demands_columns[j] == 0:
                continue
            for orientation in [Orientation.Horizontal, Orientation.Vertical]:
                ship_i_j = Ship(ship, orientation)
                if board.position_ship(ship_i_j, i, j):
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
                    board.remove_ship(ship_i_j, i, j)

    while current_ship < len(ships) and ships[current_ship] == ship:
        current_ship += 1
    naval_battle_BT(board, ships, current_ship, best_solution)
<<<<<<< Updated upstream


class GameTest:
    def __init__(self, file: str):
        self.file = file

    def run_naval_battle(self):
        try:
            barcos, demands_rows, demands_columns = self.parsear_archivo()
            result = naval_battle(barcos, demands_rows, demands_columns)
            demand_fullfilled = (
                sum(demands_rows) + sum(demands_columns) - result.remaining_demand
            )
            return demand_fullfilled
        except Exception as e:
            print(f"Ocurrió un error al ejecutar el algoritmo: {e}")
            sys.exit(1)

    def parsear_archivo(self) -> tuple[list[int], list[int], list[int]]:
        try:
            path: str = f"{self.file}"
            with open(path, "r") as file:
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
        except FileNotFoundError:
            print(f"El archivo {self.file} no fue encontrado.")
            sys.exit(1)
        except ValueError as e:
            print(f"Error al convertir datos en el archivo: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Por favor, proporciona el archivo como parámetro.")
        sys.exit(1)

    archivo = sys.argv[1]

    game_test = GameTest(archivo)

    resultado = game_test.run_naval_battle()
    print(f"Resultado del cumplimiento de la demanda: {resultado}")
=======
    
    
def parsear_archivo(filename: str) -> tuple[list[int], list[int], list[int]]:
    path: str = f"excercise_3/archivos_pruebas/TP3/{filename}"
    with open(path, "r") as file:
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
    print(f"Demanda total: {sum(demands_rows) + sum(demands_columns)}")
    print(f"Demanda cumplida: {demand_fullfilled}")
    print(f"Demanda incumplida: {resultado.remaining_demand}")
    print(f"Tiempo de ejecución: {end_time - start_time:.6f} segundos")
>>>>>>> Stashed changes
