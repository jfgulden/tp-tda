from typing import List
from typing import Tuple
import numpy as np


def validar_diagonal(board: List[List[int]], i: int, j: int):
    if i+1 < len(board) and j+1 < len(board[0]):
        if board[i+1][j+1]:
            return False

    if i-1 >= 0 and j+1 < len(board[0]):
        if board[i-1][j+1]:
            return False

    if i-1 >= 0 and j-1 >= 0:
        if board[i-1][j-1]:
            return False

    if i+1 < len(board) and j-1 >= 0:
        if board[i+1][j-1]:
            return False


    return True



def puede_colocar_barco(board: List[List[int]], len_barco: int, demandas_filas: List[int], demandas_columnas: List[int], i: int, j: int, orientacion: str):
    n = len(board)
    m = len(board[0])
    if board[i][j]:
        return False

    if orientacion == "Horizontal":
        if j + len_barco >= m:
            return False

        if demandas_filas[i] < len_barco:
            return False

        if j-1 >= 0 and board[i][j-1]: # Valido que no haya ningun barco en la posicion anterior
            return False
        for k in range(j, j + len_barco):
            if demandas_columnas[k] < 1:
                return False

            if not validar_diagonal(board, i, k):
                return False

            if i+1 < n and board[i+1][k]:
                return False
            if i-1 >= 0 and board[i-1][k]:
                return False

        if j + len_barco < m and board[i][j + len_barco]: # Valido que no haya ningun barco en la posicion siguiente
            return False

    if orientacion == "Vertical":
        if i + len_barco >= n:
            return False

        if demandas_columnas[j] < len_barco:
            return False

        if i-1 >= 0 and board[i-1][j]: # Valido que no haya ningun barco en la posicion anterior
            return False
        for k in range(i, i + len_barco):
            if demandas_filas[k] < 1:
                return False

            if not validar_diagonal(board, k, j):
                return False

            if j+1 < m and board[k][j+1]:
                return False

            if j-1 >= 0 and board[k][j-1]:
                return False

        if i+len_barco < n and board[i+len_barco][j]: # Valido que no haya ningun barco en la posicion siguiente
            return False

    return True
            

def colocar_barco(board: List[List[int]], len_barco: int, i: int, j: int, orientacion: str):

    if orientacion == "Horizontal":
        for k in range(j, j + len_barco):
            board[i][k] = 1

    if orientacion == "Vertical":
        for k in range(i, i + len_barco):
            board[k][j] = 1
            
def remover_barco(board: List[List[int]], len_barco: int, i: int, j: int, orientacion: str):

    if orientacion == "Horizontal":
        for k in range(j, j + len_barco):
            board[i][k] = 0

    if orientacion == "Vertical":
        for k in range(i, i + len_barco):
            board[k][j] = 0
            
def actualizar_demandas(len_barco: int, i: int, j: int, orientacion: str, demandas_filas: List[int], demandas_columnas: List[int]):
    n = len(demandas_filas)
    m = len(demandas_columnas)
    
    demandas_filas = demandas_filas.copy()
    demandas_columnas = demandas_columnas.copy()
    
    if orientacion == "Horizontal":
        for k in range(j, j + len_barco):
            demandas_filas[i] -= 1
            demandas_columnas[k] -= 1

    if orientacion == "Vertical":
        for k in range(i, i + len_barco):
            demandas_filas[k] -= 1
            demandas_columnas[j] -= 1
    
    return demandas_filas, demandas_columnas

    
def batalla_naval_BT(board: List[List[int]], boats: List[int], demandas_filas: List[int], demandas_columnas: List[int], mejor_solucion: List[Tuple[List[List[int]], int]], barco_actual: int = 0):
    n = len(demandas_filas)
    m = len(demandas_columnas)
    demanda_incumplida = sum(demandas_filas) + sum(demandas_columnas)

    if mejor_solucion[0] is None or demanda_incumplida < mejor_solucion[0][1]:
        mejor_solucion[0] = (board.copy(), demanda_incumplida)
    
    if not boats or barco_actual >= len(boats):
        return

    barco = boats[barco_actual]
    barco_largo = barco
    
    for orientacion in ['Horizontal', 'Vertical']:
        for i in range(n):
            for j in range(m):
                if puede_colocar_barco(board, barco_largo, demandas_filas, demandas_columnas, i, j, orientacion):
                    colocar_barco(board, barco_largo, i, j, orientacion)
                    nueva_demanda_filas, nueva_demanda_columnas = actualizar_demandas(barco_largo, i, j, orientacion, demandas_filas, demandas_columnas)
                    batalla_naval_BT(board, boats, nueva_demanda_filas, nueva_demanda_columnas, mejor_solucion, barco_actual+1)
                    remover_barco(board, barco_largo, i, j, orientacion)
    
    # Intentar omitir el barco actual
    batalla_naval_BT(board, boats, demandas_filas, demandas_columnas, mejor_solucion, barco_actual+1)

def batalla_naval(board: List[List[int]], boats: List[int], demandas_filas: List[int], demandas_columnas: List[int]):
    mejor_solucion = [None]
    batalla_naval_BT(board, boats, demandas_filas, demandas_columnas, mejor_solucion)
    return mejor_solucion[0]


def generar_tablero(n, m, boats, demandas_filas, demandas_columnas):
    # Tablero vacío
    board = np.zeros((n, m), dtype=int)
    # Encontrar la mejor solución
    mejor_solucion = batalla_naval(board, boats, demandas_filas, demandas_columnas)
    if not mejor_solucion:
        return None, None
    return mejor_solucion[0], mejor_solucion[1]

n, m = 5, 5  # Dimensiones del tablero
boats = [4, 3, 2, 2, 1]  # Longitudes de los boats
demandas_filas = [6, 6, 6, 6, 6]  # Demanda de cada fila
demandas_columnas = [6, 6, 6, 6, 6]  # Demanda de cada columna

mejor_tablero, demanda_minima = generar_tablero(n, m, boats, demandas_filas, demandas_columnas)
print("Mejor disposición de boats:")
print(mejor_tablero)
print("Demanda incumplida mínima:", demanda_minima)