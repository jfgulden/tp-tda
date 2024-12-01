import numpy as np

def is_valid_placement(board, row, col, length, horizontal):

    n, m = board.shape
    if horizontal:
       
        if col + length > m or np.any(board[row, col:col + length]):
            return False
        
        for i in range(max(0, row - 1), min(n, row + 2)):
            for j in range(max(0, col - 1), min(m, col + length + 1)):
                if board[i, j] == 1:
                    return False
    else:
        
        if row + length > n or np.any(board[row:row + length, col]):
            return False
        
        for i in range(max(0, row - 1), min(n, row + length + 1)):
            for j in range(max(0, col - 1), min(m, col + 2)):
                if board[i, j] == 1:
                    return False
    return True

def place_ship(board, row, col, length, horizontal):
    
    if horizontal:
        board[row, col:col + length] = 1
    else:
        board[row:row + length, col] = 1

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
    print(result_board, end="\n\n")
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/5_5_6.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board, end="\n\n")
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/8_7_10.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board, end="\n\n")
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/10_3_3.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board, end="\n\n")
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/10_10_10.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board, end="\n\n")
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/12_12_21.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board, end="\n\n")
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/15_10_15.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board, end="\n\n")
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/20_20_20.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board,end="\n\n")
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/20_25_30.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board,end="\n\n")
    
    demands_rows, demands_cols, ships = read_file("excercise_3/archivos_pruebas/TP3/30_25_25.txt")
    result_board = naval_approximation(demands_rows,demands_cols,ships)
    print(result_board,end="\n\n")
    

