from typing import List
from typing import Tuple
import numpy as np
from enum import Enum

class Orientacion(Enum):
    Horizontal = 1
    Vertical = 2


def validar_diagonal(tablero: List[List[int]], i: int, j: int) -> bool:
    if i+1 < len(tablero) and j+1 < len(tablero[0]):
        if tablero[i+1][j+1]:
            return False

    if i-1 >= 0 and j+1 < len(tablero[0]):
        if tablero[i-1][j+1]:
            return False

    if i-1 >= 0 and j-1 >= 0:
        if tablero[i-1][j-1]:
            return False

    if i+1 < len(tablero) and j-1 >= 0:
        if tablero[i+1][j-1]:
            return False


    return True


def puede_colocar_horizontalmente(tablero: List[List[int]], len_barco: int, demandas_filas: List[int], demandas_columnas: List[int], i: int, j: int) -> bool:
    n = len(tablero)
    m = len(tablero[0])

    if j + len_barco - 1 >= m or demandas_filas[i] < len_barco:
        return False

    if j - 1 >= 0 and tablero[i][j-1] or j + len_barco < m and tablero[i][j + len_barco]:
        return False

    for k in range(j, j + len_barco):
        if demandas_columnas[k] < 1:
            return False

        if not validar_diagonal(tablero, i, k):
            return False

        if i+1 < n and tablero[i+1][k] or i-1 >= 0 and tablero[i-1][k]:
            return False

    return True


def puede_colocar_verticalmente(tablero: List[List[int]], len_barco: int, demandas_filas: List[int], demandas_columnas: List[int], i: int, j: int) -> bool:
    n = len(tablero)
    m = len(tablero[0])

    if i + len_barco - 1 >= n or demandas_columnas[j] < len_barco:
        return False

    if i - 1 >= 0 and tablero[i-1][j] or i + len_barco < n and tablero[i+len_barco][j]:
        return False

    for k in range(i, i + len_barco):
        if demandas_filas[k] < 1:
            return False

        if not validar_diagonal(tablero, k, j):
            return False

        if j+1 < m and tablero[k][j+1] or j-1 >= 0 and tablero[k][j-1]:
            return False
        
    return True

def puede_colocar_barco(tablero: List[List[int]], len_barco: int, demandas_filas: List[int], demandas_columnas: List[int], i: int, j: int, orientacion: Orientacion) -> bool:
    if tablero[i][j]:
        return False

    if orientacion == Orientacion.Horizontal:
        return puede_colocar_horizontalmente(tablero, len_barco, demandas_filas, demandas_columnas, i, j)
        
    if orientacion == Orientacion.Vertical:
        return puede_colocar_verticalmente(tablero, len_barco, demandas_filas, demandas_columnas, i, j)
    
    return False
            

def colocar_barco(tablero: List[List[int]], len_barco: int, i: int, j: int, orientacion: Orientacion):

    if orientacion == Orientacion.Horizontal:
        for k in range(j, j + len_barco):
            tablero[i][k] = 1

    if orientacion == Orientacion.Vertical:
        for k in range(i, i + len_barco):
            tablero[k][j] = 1
            
def remover_barco(tablero: List[List[int]], len_barco: int, i: int, j: int, orientacion: Orientacion):

    if orientacion == Orientacion.Horizontal:
        for k in range(j, j + len_barco):
            tablero[i][k] = 0

    if orientacion == Orientacion.Vertical:
        for k in range(i, i + len_barco):
            tablero[k][j] = 0
            
def actualizar_demandas(len_barco: int, i: int, j: int, orientacion: str, demandas_filas: List[int], demandas_columnas: List[int]) -> Tuple[List[int], List[int]]:
    n = len(demandas_filas)
    m = len(demandas_columnas)
    
    demandas_filas = demandas_filas.copy()
    demandas_columnas = demandas_columnas.copy()
    
    if orientacion == Orientacion.Horizontal:
        for k in range(j, j + len_barco):
            demandas_filas[i] -= 1
            demandas_columnas[k] -= 1

    if orientacion == Orientacion.Vertical:
        for k in range(i, i + len_barco):
            demandas_filas[k] -= 1
            demandas_columnas[j] -= 1
    
    return demandas_filas, demandas_columnas

    
def batalla_naval_BT(tablero: List[List[int]], barcos: List[int], demandas_filas: List[int], demandas_columnas: List[int], mejor_solucion: List[Tuple[List[List[int]], int]], barco_actual: int = 0):
    n = len(demandas_filas)
    m = len(demandas_columnas)
    demanda_incumplida = sum(demandas_filas) + sum(demandas_columnas)

    if mejor_solucion[0] is None or demanda_incumplida < mejor_solucion[0][1]:
        mejor_solucion[0] = (tablero.copy(), demanda_incumplida)
    
    if not barcos or barco_actual >= len(barcos):
        return

    barco = barcos[barco_actual]
    
    for orientacion in Orientacion:
        for i in range(n):
            for j in range(m):
                if puede_colocar_barco(tablero, barco, demandas_filas, demandas_columnas, i, j, orientacion):
                    colocar_barco(tablero, barco, i, j, orientacion)
                    nueva_demanda_filas, nueva_demanda_columnas = actualizar_demandas(barco, i, j, orientacion, demandas_filas, demandas_columnas)
                    batalla_naval_BT(tablero, barcos, nueva_demanda_filas, nueva_demanda_columnas, mejor_solucion, barco_actual+1)
                    remover_barco(tablero, barco, i, j, orientacion)
    
    # Intentar omitir el barco actual
    batalla_naval_BT(tablero, barcos, demandas_filas, demandas_columnas, mejor_solucion, barco_actual+1)

def batalla_naval(tablero: List[List[int]], barcos: List[int], demandas_filas: List[int], demandas_columnas: List[int]) -> Tuple[List[List[int]], int]:
    mejor_solucion = [None]
    batalla_naval_BT(tablero, barcos, demandas_filas, demandas_columnas, mejor_solucion)
    return mejor_solucion[0]


# Ejemplo de uso
n, m = 5, 5  
barcos = [5, 5, 5, 5, 5] 
demandas_filas = [6, 6, 6, 6, 6]  
demandas_columnas = [6, 6, 6, 6, 6]
tablero = np.zeros((n, m), dtype=int)
mejor_tablero, demanda_minima = batalla_naval(tablero, barcos, demandas_filas, demandas_columnas)

print("Mejor disposición de barcos:")
print(mejor_tablero)
print("Demanda incumplida mínima:", demanda_minima)