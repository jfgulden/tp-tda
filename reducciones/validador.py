
'''
Requisitos:
- No se pueden poner los barcos de forma adyacente.
- Los barcos tienen un ancho de una celda.
- Se deben cumplir con las restricciones para filas y columnas.
- Se deben colocar todos los barcos.
'''
from typing import List

def validate_restrictions(board: List[List[bool]], boats: List[int], res_rows: List[int], res_cols: List[int]):

    # Verificar restricciones de filas
    for i in range(len(board)):
        if sum(board[i]) != res_rows[i]:
            return False  

    # Verificar restricciones de columnas
    for j in range(len(board[0])):
        occupied_col = sum(board[i][j] for i in range(len(board)))
        if occupied_col != res_cols[j]:
            return False  

    return True

def validate_boat(board: List[List[bool]], boats, i: int, j: int):
    boat_size = 1
    board[i][j] = False
    if j+1 < len(board[0]) and board[i][j+1]:
        row_index = i   # Para verificar si hay barcos adyacentes
        for k in range(j+1, len(board[0])):
            if not board[i][k]:
                break
            board[i][k] = False
            boat_size += 1

            if row_index+1 < len(board) and board[row_index+1][k]:
                return False

            if row_index+1 < len(board) and k+1 < len(board[0]) and board[row_index+1][k+1]:
                return False

            row_index += 1

    if i+1 < len(board) and board[i+1][j]:
        col_index = j   # Para verificar si hay barcos adyacentes
        for k in range(i+1, len(board)):
            if not board[k][j]:
                break
            board[k][j] = False
            boat_size += 1

            if col_index+1 < len(board[0]) and board[k][col_index+1]:
                return False

            if k+1 < len(board) and col_index+1 < len(board[0]) and board[k+1][col_index+1]:
                return False
            
            col_index += 1

    if boat_size == 1:
        if i+1 < len(board) and j+1 < len(board[0]) and board[i+1][j+1]: # Diagonal derecha
            return False
    
    if boat_size in boats:
        boats.remove(boat_size)
        return True
    
    return False



    
def naval_battle_validator(board: List[List[bool]], boats: [int], res_rows: [int], res_cols: [int]):

    if not validate_restrictions(board, boats, res_rows, res_cols):
        return False

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]:
                if not validate_boat(board, boats, i, j):
                    return False

    return True
                

# Test cases
board = [
    [True, False, False, False, True],
    [False, True, False, False, True],
    [False, False, False, False, True],
    [False, True, True, False, True]
]
boats = [1, 2, 4, 1]
res_rows = [2,2,1,3]
res_cols = [1,2,1,0,4]
print(naval_battle_validator(board, boats, res_rows, res_cols)) # True

