import numpy as np
import sys
import time

def is_valid_placement(board, row, col, length, horizontal, demand_rows, demand_cols):

    n, m = board.shape
    if horizontal:

        if col + length > m or np.any(board[row, col : col + length]):
            return False

        for i in range(max(0, row - 1), min(n, row + 2)):
            for j in range(max(0, col - 1), min(m, col + length + 1)):
                if board[i, j] == 1:
                    return False

        for i in range(col, col + length):
            if demand_cols[i] < 1:
                return False

    else:

        if row + length > n or np.any(board[row : row + length, col]):
            return False

        for i in range(max(0, row - 1), min(n, row + length + 1)):
            for j in range(max(0, col - 1), min(m, col + 2)):
                if board[i, j] == 1:
                    return False

        for i in range(row, row + length):
            if demand_rows[i] < 1:
                return False

    return True


def place_ship(board, row, col, length, horizontal):

    if horizontal:
        board[row, col : col + length] = 1
    else:
        board[row : row + length, col] = 1


def naval_approximation(demands_rows, demands_cols, ships):

    n = len(demands_rows)
    m = len(demands_cols)
    board = np.zeros((n, m), dtype=int)
    ships = sorted(ships, reverse=True)

    while ships:
        max_row_demand = max((d, i) for i, d in enumerate(demands_rows) if d > 0)
        max_col_demand = max((d, i) for i, d in enumerate(demands_cols) if d > 0)

        if max_row_demand[0] >= max_col_demand[0]:
            index = max_row_demand[1]
            is_row = True
        else:
            index = max_col_demand[1]
            is_row = False

        placed = False
        for ship in ships:
            if ship <= (demands_rows[index] if is_row else demands_cols[index]):

                if is_row:
                    for col in range(m - ship + 1):
                        if is_valid_placement(
                            board, index, col, ship, True, demands_rows, demands_cols
                        ):
                            place_ship(board, index, col, ship, True)
                            demands_rows[index] -= ship
                            for c in range(col, col + ship):
                                demands_cols[c] -= 1
                            ships.remove(ship)
                            placed = True
                            break
                else:
                    for row in range(n - ship + 1):
                        if is_valid_placement(
                            board, row, index, ship, False, demands_rows, demands_cols
                        ):
                            place_ship(board, row, index, ship, False)
                            demands_cols[index] -= ship
                            for r in range(row, row + ship):
                                demands_rows[r] -= 1
                            ships.remove(ship)
                            placed = True
                            break
            if placed:
                break

        if not placed:
            break

    return sum(demands_rows) + sum(demands_cols)


def read_file(path):

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

    return demandas_filas, demandas_columnas, barcos

def calculate_demand(files):
    for file in files:
        file_name = file.split("/")[-1]
        print(f"File: {file_name}")
        demands_rows, demands_cols, ships = read_file(file)
        demanda_inicial = np.sum(demands_rows) + np.sum(demands_cols)
        result_board = naval_approximation(demands_rows, demands_cols, ships)
        demanda_insatisfecha = np.sum(demands_rows) + np.sum(demands_cols)
        print(f"\n{result_board}\n")
        print(f"Demanda insatisfecha: {demanda_insatisfecha}")
        print(f"Demanda cumplida: {demanda_inicial - demanda_insatisfecha}")
        print(f"Demanda inicial: {demanda_inicial}")
        print("======================================")

    

if __name__ == "__main__":

<<<<<<< HEAD
    files = [
        "excercise_3/archivos_pruebas/TP3/3_3_2.txt",
        "excercise_3/archivos_pruebas/TP3/5_5_6.txt",
        "excercise_3/archivos_pruebas/TP3/8_7_10.txt",
        "excercise_3/archivos_pruebas/TP3/10_3_3.txt",
        "excercise_3/archivos_pruebas/TP3/10_10_10.txt",
        "excercise_3/archivos_pruebas/TP3/12_12_21.txt",
        "excercise_3/archivos_pruebas/TP3/15_10_15.txt",
        "excercise_3/archivos_pruebas/TP3/20_20_20.txt",
        "excercise_3/archivos_pruebas/TP3/20_25_30.txt",
        "excercise_3/archivos_pruebas/TP3/30_25_25.txt",
    ]
    calculate_demand(files)
    
=======
    if len(sys.argv) != 2:
        print("La cantidad de argumentos es incorrecta")
        print("Uso: python3 backtracking.py <archivo_prueba>")
        sys.exit()
    
    start_time = time.time()
    barcos, demandas_filas, demandas_columnas = read_file(sys.argv[1])
    demanda_incumplida = naval_approximation(barcos, demandas_filas, demandas_columnas)
    demanda_cumplida = (
        sum(demandas_filas) + sum(demandas_columnas) - demanda_incumplida
    )
    end_time = time.time()
    print(f"Demanda total: {sum(demandas_filas) + sum(demandas_columnas)}")
    print(f"Demanda cumplida: {demanda_cumplida}")
    print(f"Demanda incumplida aproximada: {demanda_incumplida}")
    print(f"Tiempo de ejecución: {end_time - start_time:.6f} segundos")
>>>>>>> 6a311b4 (fix main aproximacion)

# Analisis complejidad
# El algoritmo de aproximación es una heurística que intenta colocar los barcos en las filas o columnas con mayor demanda,
# colocando el barco más largo que pueda en esa fila o columna. Luego, se intenta colocar los barcos más largos restantes
# en la fila o columna con la siguiente mayor demanda, y así sucesivamente. El algoritmo termina cuando no se pueden colocar
# más barcos o no hay más demanda en las filas o columnas.

# La complejidad de este algoritmo depende de la cantidad de barcos y la cantidad de filas y columnas del tablero. En el peor
# caso, el algoritmo intentará colocar cada barco en cada fila o columna, lo cual resulta en una complejidad de O(n * m * k),
# donde n y m son las dimensiones del tablero y k es la cantidad de barcos. En la práctica, la complejidad que se manifiesta
# es mucho menor, ya que el algoritmo no intentará colocar cada barco en cada fila o columna, sino que intentará colocar
# los barcos en las filas o columnas con mayor demanda. Por lo tanto, la complejidad real del algoritmo es mucho menor que
# O(n * m * k), pero no se puede determinar con exactitud.
