import numpy as np
import math
from enum import Enum
from typing import List

class Orientacion(Enum):
    Horizontal = 1
    Vertical = 2

# Esta clase la usamos para guardar la posición con menos demanda en la que se puede colocar el barco actual
class MenorPosValida:
    def __init__(self, fila, col, orientacion: Orientacion = None):
        self.fila = fila
        self.col = col
        self.orientacion = orientacion
        

def diagonales_estan_libres(tablero: List[List[int]], i: int, j: int) -> bool:
    if i+1 < len(tablero) and j+1 < len(tablero[0]) and tablero[i+1][j+1]:
        return False

    if i-1 >= 0 and j+1 < len(tablero[0]) and tablero[i-1][j+1]:
        return False

    if i-1 >= 0 and j-1 >= 0 and tablero[i-1][j-1]:
        return False

    if i+1 < len(tablero) and j-1 >= 0 and tablero[i+1][j-1]:
        return False


    return True  

def puede_colocarse_verticalmente(tablero: List[List[int]], len_barco: int, demandas_filas: List[int], demandas_columnas: List[int], i: int, j: int) -> bool:
    n = len(demandas_filas)
    m = len(demandas_columnas)
    
    if i + len_barco - 1 >= n or demandas_columnas[j] < len_barco:
        return False

    if (i - 1 >= 0 and tablero[i-1][j]) or (i + len_barco < n and tablero[i+len_barco][j]):
        return False

    for k in range(i, i + len_barco):
        if demandas_filas[k] < 1:
            return False

        if not diagonales_estan_libres(tablero, k, j):
            return False

        if (j+1 < m and tablero[k][j+1]) or (j-1 >= 0 and tablero[k][j-1]):
            return False
        
    return True

def puede_colocarse_horizontalmente(tablero: List[List[int]], len_barco: int, demandas_filas: List[int], demandas_columnas: List[int], i: int, j: int) -> bool:
    n = len(demandas_filas)
    m = len(demandas_columnas)
    
    if j + len_barco - 1 >= m or demandas_filas[i] < len_barco:  #Chequeo que entre el barco
        return False

    if (j - 1 >= 0 and tablero[i][j-1]) or (j + len_barco < m and tablero[i][j + len_barco]):   #Chequeo de los extremos
        return False

    for k in range(j, j + len_barco):
        if demandas_columnas[k] < 1:
            return False

        if not diagonales_estan_libres(tablero, i, k):
            return False

        if (i+1 < n and tablero[i+1][k]) or (i-1 >= 0 and tablero[i-1][k]): # Chequeo arriba y abajo
            return False

    return True

def puede_colocarse(tablero: List[List[int]], barco: int, demandas_filas: List[int], demandas_columnas: List[int], i: int, j: int, orientacion: Orientacion) -> bool:
    if orientacion == Orientacion.Vertical:
        return puede_colocarse_verticalmente(tablero, barco, demandas_filas, demandas_columnas, i, j)
    
    if orientacion == Orientacion.Horizontal:
        return puede_colocarse_horizontalmente(tablero, barco, demandas_filas, demandas_columnas, i, j)
    
    return False

def actualizar_mejor_posicion(demandas_filas, demandas_columnas, i, j, demanda_columna, demanda_fila, orientacion, mejor_pos):
    """
    Esta funcion recibe demanda_columna y demanda_fila que son las demandas de las filas y/o columnas de la mejor posicion actual.
    Si se prueba una orientación Vertical y la orientacion de la mejor posicion es Horizontal, demanda_fila sera la suma de las demandas de las columnas de la mejor posicion, y demanda_columna la demanda de las filas de la mejor posicion.
    Si se prueba una orientación Horizontal y la orientacion de la mejor posicion es Vertical, demanda_columna sera la suma de las demandas de las filas de la mejor posicion, y demanda_fila la demanda de las columnas de la mejor posicion.
    """
    if demandas_filas[i] < demanda_fila and demandas_columnas[j] < demanda_columna:
        mejor_pos.fila = i
        mejor_pos.col = j
        mejor_pos.orientacion = orientacion
        return
        
    if demandas_filas[i] < demanda_fila:
        dif_cols = demanda_columna - demandas_columnas[j]
        dif_filas = demandas_filas[i] - demanda_fila
        
        if dif_filas > dif_cols:
            mejor_pos.fila = i
            mejor_pos.col = j
            mejor_pos.orientacion = orientacion
            return
            
    if demandas_columnas[j] < demanda_columna:
        dif_filas = demandas_filas[i] - demanda_fila
        dif_cols = demanda_columna - demandas_columnas[j]
        if dif_cols > dif_filas:
            mejor_pos.fila = i
            mejor_pos.col = j
            mejor_pos.orientacion = orientacion            
    

def actualizar_mejor_posicion_verticalmente(barco, demandas_filas, demandas_columnas, i, j, mejor_pos):
    demanda_columnas_mejor_pos, demanda_filas_mejor_pos = 0, 0
    
    if mejor_pos.orientacion == Orientacion.Horizontal:
        demanda_columnas_mejor_pos = sum(demandas_columnas[k] for k in range(mejor_pos.col, mejor_pos.col + barco))
        demanda_filas_mejor_pos = demandas_filas[mejor_pos.fila]
        return actualizar_mejor_posicion(demandas_filas, demandas_columnas, i, j, demanda_filas_mejor_pos, demanda_columnas_mejor_pos, Orientacion.Vertical, mejor_pos)
    
    if mejor_pos.orientacion == Orientacion.Vertical:
        demanda_filas_mejor_pos = sum(demandas_filas[k] for k in range(mejor_pos.fila, mejor_pos.fila + barco))
        demanda_columnas_mejor_pos = demandas_columnas[mejor_pos.col]
        return actualizar_mejor_posicion(demandas_filas, demandas_columnas, i, j, demanda_columnas_mejor_pos, demanda_filas_mejor_pos, Orientacion.Vertical, mejor_pos)
           
   

def actualizar_mejor_posicion_horizontalmente(barco, demandas_filas, demandas_columnas, i, j, mejor_pos):
    demanda_columnas_mejor_pos, demanda_filas_mejor_pos = 0, 0
        
    if mejor_pos.orientacion == Orientacion.Vertical:
        demanda_filas_mejor_pos = sum(demandas_filas[k] for k in range(mejor_pos.fila, mejor_pos.fila + barco))
        demanda_columnas_mejor_pos = demandas_columnas[mejor_pos.col]
        return actualizar_mejor_posicion(demandas_filas, demandas_columnas, i, j, demanda_filas_mejor_pos, demanda_columnas_mejor_pos, Orientacion.Horizontal, mejor_pos)
    
    if mejor_pos.orientacion == Orientacion.Horizontal:
        demanda_columnas_mejor_pos = sum(demandas_columnas[k] for k in range(mejor_pos.col, mejor_pos.col + barco))
        demanda_filas_mejor_pos = demandas_filas[mejor_pos.fila]
        return actualizar_mejor_posicion(demandas_filas, demandas_columnas, i, j, demanda_columnas_mejor_pos, demanda_filas_mejor_pos, Orientacion.Horizontal, mejor_pos)

def intentar_colocar_barco(tablero, barco, demandas_filas, demandas_columnas):
    n = len(demandas_filas)
    m = len(demandas_columnas)
    mejor_pos = None
    
    if barco > max(max(demandas_filas), max(demandas_columnas)):
        return demandas_filas, demandas_columnas
    
    for i in range(n):
        for j in range(m):
            for orientacion in Orientacion:
                if puede_colocarse(tablero, barco, demandas_filas, demandas_columnas, i, j, orientacion):
                    if not mejor_pos:
                        mejor_pos = MenorPosValida(i, j, orientacion)
                        continue
                    if orientacion == Orientacion.Vertical:
                        actualizar_mejor_posicion_verticalmente(barco, demandas_filas, demandas_columnas, i, j, mejor_pos)
                    if orientacion == Orientacion.Horizontal:
                        actualizar_mejor_posicion_horizontalmente(barco, demandas_filas, demandas_columnas, i, j, mejor_pos)
    
    if orientacion == Orientacion.Horizontal:
        actualizar_mejor_posicion_horizontalmente(barco, demandas_filas, demandas_columnas, i, j, mejor_pos)
                    
                    
    if not mejor_pos:
        return demandas_filas, demandas_columnas
        
    if mejor_pos.orientacion == Orientacion.Vertical:
        for i in range(mejor_pos.fila, mejor_pos.fila + barco):
            tablero[i][mejor_pos.col] = 1
            
        # Actualizo las demandas
        for i in range(mejor_pos.fila, mejor_pos.fila + barco):
            demandas_filas[i] -= 1
            
        demandas_columnas[mejor_pos.col] -= barco
            
    if mejor_pos.orientacion == Orientacion.Horizontal:
        for j in range(mejor_pos.col, mejor_pos.col + barco):
            tablero[mejor_pos.fila][j] = 1
            
        # Actualizo las demandas
        for j in range(mejor_pos.col, mejor_pos.col + barco):
            demandas_columnas[j] -= 1
        
        demandas_filas[mejor_pos.fila] -= barco
    
    
    return demandas_filas, demandas_columnas
        
    
def batalla_naval(
    barcos: List[int], demandas_filas: List[int], demandas_columnas: List[int]
):

    barcos = sorted(barcos, reverse=True)
    n = len(demandas_filas)
    m = len(demandas_columnas)
    
    tablero = np.zeros((n, m))
    
    for barco in barcos:
        demandas_filas, demandas_columnas = intentar_colocar_barco(tablero, barco, demandas_filas, demandas_columnas)
    
    print(demandas_filas, demandas_columnas)
    print(tablero)
    return sum(demandas_filas) + sum(demandas_columnas)

def parsear_archivo(filename: str) -> tuple[list[int], list[int], list[int]]:
    path: str = f"excercise_3/archivos_pruebas/TP3/{filename}"
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

    return barcos, demandas_filas, demandas_columnas

if __name__ == "__main__":
    barcos, demandas_filas, demandas_columnas = parsear_archivo("30_25_25.txt")
    print(batalla_naval(barcos, demandas_filas, demandas_columnas))
    
    
        
    
    




    