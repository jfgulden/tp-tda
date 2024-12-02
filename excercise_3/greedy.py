import numpy as np
import math
from enum import Enum
from typing import List
import sys
import time

class Orientacion(Enum):
    Horizontal = 1
    Vertical = 2

# Esta clase la usamos para guardar la posición con menos demanda en la que se puede colocar el barco actual
class PosDemandaMin:
    def __init__(self, fila, col, orientacion: Orientacion = None):
        self.fila = fila
        self.col = col
        self.orientacion = orientacion
        
class Demandas:
    def __init__(self, demandas_filas: List[int], demandas_columnas: List[int]):
        self.filas = demandas_filas
        self.columnas = demandas_columnas
        

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

def puede_colocarse_verticalmente(tablero: List[List[int]], len_barco: int, demandas: Demandas, i: int, j: int) -> bool:
    n = len(demandas.filas)
    m = len(demandas.columnas)
    
    if i + len_barco - 1 >= n or demandas.columnas[j] < len_barco:
        return False

    if (i - 1 >= 0 and tablero[i-1][j]) or (i + len_barco < n and tablero[i+len_barco][j]):
        return False

    for k in range(i, i + len_barco):
        if demandas.filas[k] < 1:
            return False

        if not diagonales_estan_libres(tablero, k, j):
            return False

        if (j+1 < m and tablero[k][j+1]) or (j-1 >= 0 and tablero[k][j-1]):
            return False
        
    return True

def puede_colocarse_horizontalmente(tablero: List[List[int]], len_barco: int, demandas: Demandas, i: int, j: int) -> bool:
    n = len(demandas.filas)
    m = len(demandas.columnas)
    
    if j + len_barco - 1 >= m or demandas.filas[i] < len_barco:  #Chequeo que entre el barco
        return False

    if (j - 1 >= 0 and tablero[i][j-1]) or (j + len_barco < m and tablero[i][j + len_barco]):   #Chequeo de los extremos
        return False

    for k in range(j, j + len_barco):
        if demandas.columnas[k] < 1:
            return False

        if not diagonales_estan_libres(tablero, i, k):
            return False

        if (i+1 < n and tablero[i+1][k]) or (i-1 >= 0 and tablero[i-1][k]): # Chequeo arriba y abajo
            return False

    return True

def puede_colocarse(tablero: List[List[int]], barco: int, demandas: Demandas, i: int, j: int, orientacion: Orientacion) -> bool:
    if orientacion == Orientacion.Vertical:
        return puede_colocarse_verticalmente(tablero, barco, demandas, i, j)
    
    if orientacion == Orientacion.Horizontal:
        return puede_colocarse_horizontalmente(tablero, barco, demandas, i, j)
    
    return False

def obtener_demanda_pos_demanda_min(barco: int, pos_demanda_min: PosDemandaMin, demandas: Demandas) -> int:
    demanda_filas, demanda_columnas = 0, 0
    if pos_demanda_min.orientacion == Orientacion.Vertical:
        demanda_filas = sum(demandas.filas[k] for k in range(pos_demanda_min.fila, pos_demanda_min.fila + barco))
        demanda_columnas = demandas.columnas[pos_demanda_min.col]
      
    if pos_demanda_min.orientacion == Orientacion.Horizontal:
        demanda_columnas = sum(demandas.columnas[k] for k in range(pos_demanda_min.col, pos_demanda_min.col + barco))
        demanda_filas = demandas.filas[pos_demanda_min.fila]

    return demanda_filas + demanda_columnas
    
def obtener_demanda_actual(i: int, j: int, orientacion: Orientacion, barco: int, demandas: Demandas):
    demanda_filas, demanda_columnas = 0, 0
    if orientacion == Orientacion.Vertical:
        demanda_filas = sum(demandas.filas[k] for k in range(i, i + barco))
        demanda_columnas = demandas.columnas[j]
    
    if orientacion == Orientacion.Horizontal:
        demanda_columnas = sum(demandas.columnas[k] for k in range(j, j + barco))
        demanda_filas = demandas.filas[i]
        
    return demanda_filas + demanda_columnas
    
        
def intentar_actualizar_pos_demanda_min(pos_demanda_min: PosDemandaMin, i: int, j: int, orientacion: Orientacion, barco: int, demandas: Demandas):
    demanda_pos_demanda_min = obtener_demanda_pos_demanda_min(barco, pos_demanda_min, demandas)
    demanda_actual = obtener_demanda_actual(i, j, orientacion, barco, demandas)
    
    if demanda_actual < demanda_pos_demanda_min:
        pos_demanda_min.col = j
        pos_demanda_min.fila = i
        pos_demanda_min.orientacion = orientacion

def colocar_barco(tablero: List[List[int]], barco: int, pos_demanda_min: PosDemandaMin, demandas: Demandas):
    if pos_demanda_min.orientacion == Orientacion.Vertical:
        for i in range(pos_demanda_min.fila, pos_demanda_min.fila + barco):
            tablero[i][pos_demanda_min.col] = 1
            
        # Actualizo las demandas
        for i in range(pos_demanda_min.fila, pos_demanda_min.fila + barco):
            demandas.filas[i] -= 1
            
        demandas.columnas[pos_demanda_min.col] -= barco
            
    if pos_demanda_min.orientacion == Orientacion.Horizontal:
        for j in range(pos_demanda_min.col, pos_demanda_min.col + barco):
            tablero[pos_demanda_min.fila][j] = 1
            
        # Actualizo las demandas
        for j in range(pos_demanda_min.col, pos_demanda_min.col + barco):
            demandas.columnas[j] -= 1
        
        demandas.filas[pos_demanda_min.fila] -= barco
    
def intentar_colocar_barco(tablero: List[List[int]], barco: int, demandas: Demandas) -> Demandas:
    n = len(demandas.filas)
    m = len(demandas.columnas)
    pos_demanda_min = None
    
    if barco > max(max(demandas.filas), max(demandas.columnas)):
        return demandas
    
    for i in range(n):
        for j in range(m):
            for orientacion in Orientacion:
                if puede_colocarse(tablero, barco, demandas, i, j, orientacion):
                    if not pos_demanda_min:
                        pos_demanda_min = PosDemandaMin(i, j, orientacion)
                        continue
                    
                    intentar_actualizar_pos_demanda_min(pos_demanda_min, i, j, orientacion, barco, demandas)

    if not pos_demanda_min:
        return demandas
    
    colocar_barco(tablero, barco, pos_demanda_min, demandas)
    
    return demandas
        
    
def batalla_naval(
    barcos: List[int], demandas_filas: List[int], demandas_columnas: List[int]
):

    barcos = sorted(barcos, reverse=True)
    tablero = np.zeros((len(demandas_filas), len(demandas_columnas)))
    demandas = Demandas(demandas_filas, demandas_columnas)
    
    for barco in barcos:
        demandas = intentar_colocar_barco(tablero, barco, demandas)

    return sum(demandas.filas) + sum(demandas.columnas)

def parsear_archivo(filepath: str) -> tuple[list[int], list[int], list[int]]:
    with open(filepath, "r") as file:
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
    if len(sys.argv) != 2:
        print("La cantidad de argumentos es incorrecta")
        print("Uso: python3 backtracking.py <archivo_prueba>")
        sys.exit()
    
    start_time = time.time()
    barcos, demandas_filas, demandas_columnas = parsear_archivo(sys.argv[1])
    demanda_incumplida = batalla_naval(barcos, demandas_filas, demandas_columnas)
    demanda_cumplida = (
        sum(demandas_filas) + sum(demandas_columnas) - demanda_incumplida
    )
    end_time = time.time()
    print(f"Demanda total: {sum(demandas_filas) + sum(demandas_columnas)}")
    print(f"Demanda cumplida: {demanda_cumplida}")
    print(f"Demanda incumplida aproximada: {demanda_incumplida}")
    print(f"Tiempo de ejecución: {end_time - start_time:.6f} segundos")


    
        
    
    




    