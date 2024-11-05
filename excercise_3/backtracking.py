
from typing import List


def restricciones_validas(board: List[List[bool]], boats: List[int], res_rows: List[int], res_cols: List[int], curr_row: int, curr_col: int):

    for i in range(curr_row + 1):
        res_row = sum(board[i])
        if i < curr_row and res_row != res_rows[i]:
            return False  
    
        if curr_col == len(board[0]) - 1:
            if res_row < res_rows[i]:
                return False


    for j in range(len(boards[0])):
        occupied_col = sum(board[i][j] (for i in range(curr_row + 1) if j < curr_col else for i in range(curr_row)))
        if occupied_col > res_cols[j]:
            return False  

        if curr_row == len(board) - 1 and j <= curr_col and occupied_col < res_cols[j]:
            return False  

    return True

def validate_diagonal(board: List[List[bool]], i: int, j: int):
    if i+1 < len(board) and j+1 < len(board[0]):
        if board[i+1][j+1]:
            return False

    return True

def validate_adjacency_right(board: List[List[bool]], i: int, j: int):
    
    if i+1 < len(board):
        if board[i+1][j]:
            return False

    return validate_diagonal(board, i, j)

def validate_adjacency_down(board: List[List[bool]], i: int, j: int):
    
    if j+1 < len(board[0]):
        if board[i][j+1]:
            return False

    return validate_diagonal(board, i, j)


def search_boat_to_right(board: List[List[bool]], i: int, j: int, boat_size: List[int]):
    row_index = i   # Para verificar si hay barcos adyacentes
    for k in range(j, len(board[0])):
        if not board[i][k]:
            break
        board[i][k] = 0
        boat_size[0] += 1
        
        if not validate_adjacency_right(board, row_index, k):
            return False
        row_index += 1

    return True

def search_boat_to_bottom(board: List[List[bool]], i: int, j: int, boat_size: List[int]):
    col_index = j   # Para verificar si hay barcos adyacentes
    for k in range(i, len(board)):
        if not board[k][j]:
            break
        board[k][j] = 0
        boat_size[0] += 1

        if not validate_adjacency_down(board, k, col_index):
            return False
        col_index += 1

    return True


def validate_boat(board: List[List[bool]], boats, i: int, j: int):
    boat_size = [1]
    board[i][j] = 0
    if j+1 < len(board[0]) and board[i][j+1]:
        if not search_boat_to_right(board, i, j+1, boat_size):
            return False

    if i+1 < len(board) and board[i+1][j]:
        if not search_boat_to_bottom(board, i+1, j, boat_size):
            return False

    if boat_size == 1:
        if not validate_diagonal(board, i, j):
            return False
    
    if boat_size[0] in boats:
        boats.remove(boat_size[0])
        return True
    
    return False

def es_compatible(tablero: List[List[int]], boats: List[int], res_rows: List[int], res_cols: List[int], curr_row: int, curr_col: int):
    if not restricciones_validas(tablero, boats, res_rows, res_cols, curr_row, curr_col):
        return False

    for i in range(curr_row + 1):
        if i < curr_row:
            for j in range(len(board[i])):
                if board[i][j]:
                    if not validate_boat(board, boats, i, j):
                        return False
        else:
            for j in range(curr_col + 1):
                if board[i][j]:
                    if not validate_boat(board, boats, i, j):
                        return False


def colocar_barco_horizontalmente(tablero: List[List[int]], boat: int, i: int, j: int):
    if j + boat >= len(tablero[0]):
        return False

    for k in range(boat):
        tablero[i][j+k] == 1

    return True

def colocar_barco_verticalmente(tablero: List[List[int]], boat: int, i: int, j: int):
    if i + boat >= len(tablero):
        return False

    for k in range(boat):
        tablero[i+k][j] == 1

    return True

def batalla_naval_BT(tablero: List[List[int]], boats: List[int], res_rows: List[int], res_cols: List[int], i: int, j: int):
    if not es_compatible(tablero, boats, res_rows, res_cols, i, j):
        return False
    if len(boats) == 0:
        return True

    ## Probar con cada uno de los barcos disponibles
    ## Por cada barco: Probar colocarlo horizontalmente o verticalmente
    for b in boats:
        boats.remove(b)
        if colocar_barco_horizontalmente(tablero, b, i, j):
            j += b
            if batalla_naval_BT(tablero, boats, res_rows, res_cols, i, j):
                return True

        if colocar_barco_verticalmente(tablero, b, i, j):
            i += b
            if batalla_naval_BT(tablero, boats, res_rows, res_cols, i, j):
                return True
        
        boats.append(b)

    return False


def batalla_naval(tablero: List[List[int]], boats: List[int], res_rows: List[int], res_cols: List[int]):

    return batalla_naval_BT(tablero, boats, res_rows, res_cols, 0, 0)

tablero = [[0] * n for _ in range(n)]