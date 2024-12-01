import numpy as np

def is_valid_placement(board, row, col, length, horizontal):
    """
    Verifica si se puede colocar un barco en una posición dada.
    :param board: Matriz del tablero actual.
    :param row: Fila inicial.
    :param col: Columna inicial.
    :param length: Longitud del barco.
    :param horizontal: Booleano, True si el barco es horizontal, False si es vertical.
    :return: True si es posible colocar el barco, False en caso contrario.
    """
    n, m = board.shape
    if horizontal:
        # Verificar que no se salga del tablero y no haya conflictos
        if col + length > m or np.any(board[row, col:col + length]):
            return False
        # Verificar que no haya barcos adyacentes (incluyendo diagonales)
        for i in range(max(0, row - 1), min(n, row + 2)):
            for j in range(max(0, col - 1), min(m, col + length + 1)):
                if board[i, j] == 1:
                    return False
    else:
        # Verificar que no se salga del tablero y no haya conflictos
        if row + length > n or np.any(board[row:row + length, col]):
            return False
        # Verificar que no haya barcos adyacentes (incluyendo diagonales)
        for i in range(max(0, row - 1), min(n, row + length + 1)):
            for j in range(max(0, col - 1), min(m, col + 2)):
                if board[i, j] == 1:
                    return False
    return True

def place_ship(board, row, col, length, horizontal):
    """
    Coloca un barco en el tablero.
    :param board: Matriz del tablero actual.
    :param row: Fila inicial.
    :param col: Columna inicial.
    :param length: Longitud del barco.
    :param horizontal: Booleano, True si el barco es horizontal, False si es vertical.
    """
    if horizontal:
        board[row, col:col + length] = 1
    else:
        board[row:row + length, col] = 1

def naval_approximation(demands_rows, demands_cols, ships):
    """
    Implementa el algoritmo de aproximación para La Batalla Naval.
    :param demands_rows: Lista con las demandas por fila.
    :param demands_cols: Lista con las demandas por columna.
    :param ships: Lista de longitudes de barcos.
    :return: Matriz del tablero con los barcos colocados.
    """
    n = len(demands_rows)
    m = len(demands_cols)
    board = np.zeros((n, m), dtype=int)
    ships = sorted(ships, reverse=True)  # Ordenar barcos de mayor a menor longitud
    
    while ships:
        max_row_demand = max((d, i) for i, d in enumerate(demands_rows) if d > 0)
        max_col_demand = max((d, i) for i, d in enumerate(demands_cols) if d > 0)
        
        # Determinar si trabajar con la fila o columna
        if max_row_demand[0] >= max_col_demand[0]:
            index = max_row_demand[1]
            is_row = True
        else:
            index = max_col_demand[1]
            is_row = False
        
        # Intentar colocar el barco más largo en esta fila/columna
        placed = False
        for ship in ships:
            if ship <= (demands_rows[index] if is_row else demands_cols[index]):
                # Buscar posición válida
                if is_row:
                    for col in range(m - ship + 1):
                        if is_valid_placement(board, index, col, ship, True):
                            place_ship(board, index, col, ship, True)
                            demands_rows[index] -= ship
                            for c in range(col, col + ship):
                                demands_cols[c] -= 1
                            ships.remove(ship)
                            placed = True
                            break
                else:
                    for row in range(n - ship + 1):
                        if is_valid_placement(board, row, index, ship, False):
                            place_ship(board, row, index, ship, False)
                            demands_cols[index] -= ship
                            for r in range(row, row + ship):
                                demands_rows[r] -= 1
                            ships.remove(ship)
                            placed = True
                            break
            if placed:
                break
        
        # Si no se puede colocar ningún barco en esta fila/columna, continuar
        if not placed:
            break
    
    return board
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

    return  demandas_filas, demandas_columnas,barcos
    

if __name__ == "__main__":
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/3_3_2.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board)
    print(demands_rows)
    
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/5_5_6.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board)
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/8_7_10.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board)
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/10_3_3.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board)
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/10_10_10.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board)
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/12_12_21.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board)
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/15_10_15.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board)
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/20_20_20.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board)
    

