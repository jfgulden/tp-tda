# Validador eficiente para demostrar que el problema es NP
'''
Requisitos:
- No puede haber barcos adyacentes entre si.
- Los barcos tienen un ancho de una celda.
- Se debe cumplir con las restricciones para filas y columnas.
- Se deben colocar todos los barcos.
'''

from typing import List

def validate_diagonals(board: List[List[bool]], i: int, j: int):
    if i+1 < len(board) and j+1 < len(board[0]):
        if board[i+1][j+1]:
            return False

    if i+1 < len(board) and j-1 >= 0:
        if board[i+1][j-1]:
            return False
        
    if i-1 >= 0 and j+1 < len(board[0]):
        if board[i-1][j+1]:
            return False
    
    if i-1 >= 0 and j-1 >= 0:
        if board[i-1][j-1]:
            return False

    return True

def is_vertical(board: List[List[bool]], i: int, j: int):
    if i+1 < len(board):
        if board[i+1][j]:
            return True
    
    if i-1 >= 0:
        if board[i-1][j]:
            return True
    return False

def is_horizontal(board: List[List[bool]], i: int, j: int):
    if j+1 < len(board[0]):
        if board[i][j+1]:
            return True
    
    if j-1 >= 0:
        if board[i][j-1]:
            return True
    return False

def validate_restrictions(board: List[List[bool]], boats: List[int], res_rows: List[int], res_cols: List[int]):
    """
    Complejidad: O(m x n) + O(m x n) + O(m x n) = O(m x n)
    """
    
    # Verificar restricciones de filas
    for i in range(len(board)): # O(n)
        if sum(board[i]) != res_rows[i]:    # O(m)
            print('Fila ' + str(i) + ' no cumple con la restricción')
            return False  

    # Verificar restricciones de columnas
    for j in range(len(board[0])):  # O(m)
        occupied_col = sum(board[i][j] for i in range(len(board)))  # O(n)
        if occupied_col != res_cols[j]:
            print('Columna ' + str(j) + ' no cumple con la restricción') 
            return False 

    #verificar que hay cantidad correcta de casilleros ocupados
    occupied_cells = sum(sum(row) for row in board) # O(m x n)
    if occupied_cells != sum(boats):
        print('Cantidad de casilleros ocupados incorrecta')
        return False

    return True


def validate_diagonal(board: List[List[bool]], i: int, j: int):
    """
    Complejidad: O(1)
    """

    if i+1 < len(board) and j+1 < len(board[0]):
        if board[i+1][j+1]:
            return False

    if i+1 < len(board) and j-1 >= 0:
        if board[i+1][j-1]:
            return False

    if i-1 >= 0 and j+1 < len(board[0]):
        if board[i-1][j+1]:
            return False
        
    if i-1 >= 0 and j-1 >= 0:
        if board[i-1][j-1]:
            return False

    return True

def validate_adjacency_right(board: List[List[bool]], i: int, j: int):
    """
    Complejidad: O(1)
    """
    
    if i+1 < len(board) and board[i+1][j]:
        return False
    
    if i-1 >= 0 and board[i-1][j]:
        return False

    return validate_diagonal(board, i, j)

def validate_adjacency_down(board: List[List[bool]], i: int, j: int):
    """
    Complejidad: O(1)
    """
    
    if j+1 < len(board[0]) and board[i][j+1]:
        return False

    if j-1 >= 0 and board[i][j-1]:
        return False

    return validate_diagonal(board, i, j)


def search_boat_to_right(board: List[List[bool]], i: int, j: int, boat_size: List[int]):
    """
    Complejidad: O(m)
    """
    for k in range(j, len(board[0])):   # O(m)
        if not board[i][k]:
            break
        
        if not validate_adjacency_right(board, i, k):
            return False

        board[i][k] = 0
        boat_size[0] += 1

    return True

def search_boat_to_bottom(board: List[List[bool]], i: int, j: int, boat_size: List[int]):
    """
    Complejidad: O(n)
    """
    for k in range(i, len(board)):  # O(n)
        if not board[k][j]:
            break

        if not validate_adjacency_down(board, k, j):
            return False

        board[k][j] = 0
        boat_size[0] += 1

    return True


def validate_boat(board: List[List[bool]], boats, i: int, j: int):
    """
    Complejidad: O(max(m, n) + k), porque se puede llamar a search_boat_to_right o search_boat_to_bottom, pero no a ambos.
    """
    boat_size = [1]
    board[i][j] = 0
    if j+1 < len(board[0]) and board[i][j+1]:
        if not search_boat_to_right(board, i, j, boat_size):  # O(m)
            return False

    if i+1 < len(board) and board[i+1][j]:
        if not search_boat_to_bottom(board, i, j, boat_size): # O(n)
            return False

    if boat_size == 1:
        if not validate_diagonal(board, i, j):  # O(1)
            return False
    
    if boat_size[0] in boats:
        boats.remove(boat_size[0])  # O(k)
        return True
    
    
    return False

    
def naval_battle_validator(board: List[List[int]], boats: List[int], res_rows: List[int], res_cols: List[int]):
    """
    Complejidad: O(m x n) + O(m x n + n/2 x (m + k)) = O(m x n)
    """

    if len(board) == 0:
        return False

    if len(board[0]) == 0:
        return False

    if len(res_rows) == 0 or len(res_cols) == 0 or len(boats) == 0:
        return False

    if sum(boats) > len(board) * len(board[0]): # Si la dimension del tablero es menor que la cantidad de posiciones a ocupar, no es valido.
        return False

    if not validate_restrictions(board, boats, res_rows, res_cols): # O(m x n)
        return False

    for i in range(len(board)): # O(n)
        for j in range(len(board[i])):  # O(m)
            if board[i][j]:
                if not validate_boat(board, boats, i, j):   # O(max(m, n) + k)
                    return False

    if len(boats) > 0:  # Si no se colocaron todos los barcos
        return False

    return True

[1,0,1,0,1]
[0,0,0,0,0]
[1,0,1,0,1]
[0,0,0,0,0]
[1,0,1,0,1]


# Test cases
board = [
    [1, 0, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1]
]
boats = [1, 2, 4]
res_rows = [2,1,1,3]
res_cols = [1,1,1,0,4]
print("Test3: True, caso 5x5 con 3 barcos")
print(naval_battle_validator(board, boats, res_rows, res_cols)) # True
print()

# Test4: Caso 5x5 con 4 barcos
board = [
    [1, 0, 0, 0, 1],
    [0, 0, 1, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0]
]
boats = [1, 2, 4, 1]
res_rows = [2,2,1,3,0]
res_cols = [1,1,2,0,4]
print("Test4: True, caso 5x5 con 4 barcos")
print(naval_battle_validator(board, boats, res_rows, res_cols)) # True
print()

# Test5: Ejemplo consigna
board = [
    [0, 0, 0 , 0, 1, 1, 1, 0, 0, 0],
    [1, 0, 0 , 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1 , 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0 , 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 0 , 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0 , 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0 , 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0 , 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0 , 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 0 , 0, 0, 0, 0, 0, 0, 0],
]

boats = [3,1,1,2,4,2,1,3,1,2]
res_rows = [3,2,2,4,2,1,1,2,3,0]
res_cols = [1,2,1,3,2,2,3,1,5,0]

print("Test5: True, Ejemplo consigna")
print(naval_battle_validator(board, boats, res_rows, res_cols)) # True
print()

####################
# Casos negativos #
###################

## Por restricciones ##

# Test5: Caso 5x5 con 4 barcos, hay un barco de más (1,2)
board = [
    [1, 0, 0, 0, 1],
    [0, 1, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1]
]

boats = [1, 2, 4]
res_rows = [2,2,1,3]
res_cols = [1,1,2,0,4]

print("Test5: False. Hay un barco de más (1,2)")
print(naval_battle_validator(board, boats, res_rows, res_cols)) # False: hay un barco de más (1,2)
print()


# Test6: Caso 5x5 con 4 barcos, no se cumplen las restricciones de columnas
board = [
    [1, 0, 0, 0, 1],
    [0, 1, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1]
]

boats = [1, 2, 4, 1]
res_rows = [2,2,1,3]
res_cols = [1,2,1,0,5]

print("Test6: False, No se cumplen las restricciones de columnas")
print(naval_battle_validator(board, boats, res_rows, res_cols)) # False: No se cumplen las restricciones de columnas

board = [
    [1, 0, 0, 0, 1],
    [0, 1, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1]
]

boats = [1, 2, 4, 1]
res_rows = [2,1,1,3]
res_cols = [1,1,1,0,4]

print("Test7: False, No se colocaron todos los barcos")
print(naval_battle_validator(board, boats, res_rows, res_cols)) # False: Queda un barco sin poner
print()

## Por barcos adyacentes ##

# Test8: Hay un barco diagonal al 0,0
board = [
    [1, 0, 0, 0, 1],
    [0, 1, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1]
]

boats = [1, 2, 4]
res_rows = [2,2,1,4]
res_cols = [1,2,1,0,4]

print("Test8: False, No se cumplen las restricciones de filas")
print(naval_battle_validator(board, boats, res_rows, res_cols)) # False: No se cumplen las restricciones de filas
print()

# Test9: Hay un barco adyacente a la derecha
board = [
    [0, 0, 1],
    [1, 1, 1],
    [0, 0, 1]
]

boats = [2, 3]
res_rows = [1,3,1]
res_cols = [1,1,3]

print("Test9: False, Hay un barco adyacente a la derecha")
print(naval_battle_validator(board, boats, res_rows, res_cols)) # False: Hay un barco adyacente a la derecha
print()

# Test10: Hay un barco adyacente abajo
board = [
    [1, 1, 1],
    [0, 1, 0],
    [0, 1, 0]
]

boats = [2, 3]
res_rows = [3,1,1]
res_cols = [1,3,1]

print("Test10: False, Hay un barco adyacente abajo")
print(naval_battle_validator(board, boats, res_rows, res_cols)) # False: Hay un barco adyacente abajo
print()

# Test11: Hay dos barcos de tamaño incorrecto
# Las sumas dan bien. Solo los largos de cada uno estan mal
board = [
    [1, 0, 0, 0, 1],
    [0, 1, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1]
]

boats = [2, 2]
res_rows = [1,2,1]
res_cols = [3,0,1]

print("Test11: False, Hay dos barcos de tamaño incorrecto")
print(naval_battle_validator(board, boats, res_rows, res_cols)) # False: Hay dos barcos de tamaño incorrecto
print()

# Test12: Hay 2 barcos tamaño 1 adyacentes
board = [
    [1, 0, 0, 0, 1],
    [0, 0, 1, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0]
]

boats = [1, 1]
res_rows = [2,0,0]
res_cols = [1,1,0]

print("Test12: False, Hay 2 barcos tamaño 1 adyacentes")
print(naval_battle_validator(board, boats, res_rows, res_cols)) # False: Hay 2 barcos tamaño 1 adyacentes
print()

