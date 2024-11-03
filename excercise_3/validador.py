
'''
Requisitos:
- No pueden haber barcos adyacentes.
- Los barcos tienen un ancho de una celda.
- Se debe cumplir con las restricciones para filas y columnas.
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
        board[i][k] = False
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
        board[k][j] = False
        boat_size[0] += 1

        if not validate_adjacency_down(board, k, col_index):
            return False
        col_index += 1

    return True


def validate_boat(board: List[List[bool]], boats, i: int, j: int):
    boat_size = [1]
    board[i][j] = False
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



    
def naval_battle_validator(board: List[List[bool]], boats: List[int], res_rows: List[int], res_cols: List[int]):

    if not validate_restrictions(board, boats, res_rows, res_cols):
        return False

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]:
                if not validate_boat(board, boats, i, j):
                    return False

    if len(boats) > 0:  # Si no se colocaron todos los barcos
        return False

    return True
                

# Test cases
board = [
    [True, False, False, False, True],
    [False, False, False, False, True],
    [False, False, False, False, True],
    [False, True, True, False, True]
]
boats = [1, 2, 4]
res_rows = [2,1,1,3]
res_cols = [1,1,1,0,4]
print(naval_battle_validator(board, boats, res_rows, res_cols)) # True

board = [
    [True, False, False, False, True],
    [False, True, False, False, True],
    [False, False, False, False, True],
    [False, True, True, False, True]
]
boats = [1, 2, 4]
res_rows = [2,2,1,3]
res_cols = [1,2,1,0,4]
print(naval_battle_validator(board, boats, res_rows, res_cols)) # False: Hay un barco en diagonal al [0,0]


board = [
    [True, False, False, False, True],
    [False, True, False, False, True],
    [False, False, False, False, True],
    [False, True, True, False, True]
]
boats = [1, 2, 4]
res_rows = [2,2,1,3]
res_cols = [1,2,1,0,5]
print(naval_battle_validator(board, boats, res_rows, res_cols)) # False: No se cumplen las restricciones de columnas

board = [
    [True, False, False, False, True],
    [False, True, False, False, True],
    [False, False, False, False, True],
    [False, True, True, False, True]
]
boats = [1, 2, 4]
res_rows = [2,2,1,4]
res_cols = [1,2,1,0,4]
print(naval_battle_validator(board, boats, res_rows, res_cols)) # False: No se cumplen las restricciones de filas


board = [
    [True, False, False, False, True],
    [False, True, False, False, True],
    [False, False, False, False, True],
    [False, True, True, False, True]
]
boats = [1, 2, 4, 1]
res_rows = [2,2,1,4]
res_cols = [1,2,1,0,4]
print(naval_battle_validator(board, boats, res_rows, res_cols)) # False: Queda un barco sin poner

board = [
    [True, False, False, False, True],
    [False, False, True, False, True],
    [False, False, False, False, True],
    [False, True, True, False, True],
    [False, False, False, False, False]
]
boats = [1, 2, 4, 1]
res_rows = [2,2,1,3,0]
res_cols = [1,1,2,0,4]
print(naval_battle_validator(board, boats, res_rows, res_cols)) # True

#TODO: Mejorar estos tests
#TODO: Analizar complejidad -> Explicar por que es polinomial 

