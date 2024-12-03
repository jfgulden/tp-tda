import sys
import time
import numpy as np


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

    return board


def parsear_archivo(path):

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


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("La cantidad de argumentos es incorrecta")
        print("Uso: python3 aproximacion.py <archivo_prueba>")
        sys.exit()

    start_time = time.time()
    demandas_filas, demandas_columnas, barcos = parsear_archivo(sys.argv[1])
    print("Barcos:", barcos)
    print("Demandas filas:", demandas_filas)
    print("Demandas columnas:", demandas_columnas)
    demanda_inicial = np.sum(demandas_filas) + np.sum(demandas_columnas)
    result_board = naval_approximation(demandas_filas, demandas_columnas, barcos)
    demanda_insatisfecha = np.sum(demandas_filas) + np.sum(demandas_columnas)
    time_elapsed = time.time() - start_time

    print()
    print(f"Demanda insatisfecha: {demanda_insatisfecha}")
    print(f"Demanda cumplida: {demanda_inicial - demanda_insatisfecha}")
    print(f"Demanda inicial: {demanda_inicial}")
    print(f"Tiempo de ejecución: {time_elapsed:.6f} segundos")


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
