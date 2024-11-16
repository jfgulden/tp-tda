from typing import List
from typing import Tuple
import numpy as np
from enum import Enum

class Orientacion(Enum):
    Horizontal = 1
    Vertical = 2


def validar_diagonal(tablero: List[List[int]], i: int, j: int) -> bool:
    if i+1 < len(tablero) and j+1 < len(tablero[0]) and tablero[i+1][j+1]:
        return False

    if i-1 >= 0 and j+1 < len(tablero[0]) and tablero[i-1][j+1]:
        return False

    if i-1 >= 0 and j-1 >= 0 and tablero[i-1][j-1]:
        return False

    if i+1 < len(tablero) and j-1 >= 0 and tablero[i+1][j-1]:
        return False


    return True


def puede_colocar_horizontalmente(tablero: List[List[int]], len_barco: int, demandas_filas: List[int], demandas_columnas: List[int], i: int, j: int) -> bool:
    n = len(tablero)
    m = len(tablero[0])
   
    if j + len_barco - 1 >= m or demandas_filas[i] < len_barco:  #Chequeo que entre el barco
        return False

    if (j - 1 >= 0 and tablero[i][j-1]) or (j + len_barco < m and tablero[i][j + len_barco]):   #Chequeo de los extremos
        return False

    for k in range(j, j + len_barco):
        if demandas_columnas[k] < 1:
            return False

        if not validar_diagonal(tablero, i, k):
            return False

        if (i+1 < n and tablero[i+1][k]) or (i-1 >= 0 and tablero[i-1][k]): # Chequeo arriba y abajo
            return False

    return True


def puede_colocar_verticalmente(tablero: List[List[int]], len_barco: int, demandas_filas: List[int], demandas_columnas: List[int], i: int, j: int) -> bool:
    n = len(tablero)
    m = len(tablero[0])

    if i + len_barco - 1 >= n or demandas_columnas[j] < len_barco:
        return False

    if (i - 1 >= 0 and tablero[i-1][j]) or (i + len_barco < n and tablero[i+len_barco][j]):
        return False

    for k in range(i, i + len_barco):
        if demandas_filas[k] < 1:
            return False

        if not validar_diagonal(tablero, k, j):
            return False

        if (j+1 < m and tablero[k][j+1]) or (j-1 >= 0 and tablero[k][j-1]):
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
            
def actualizar_demandas(len_barco: int, i: int, j: int, orientacion: Orientacion, demandas_filas: List[int], demandas_columnas: List[int]) -> Tuple[List[int], List[int]]:
    
    demandas_filas_cp = demandas_filas.copy()
    demandas_columnas_cp = demandas_columnas.copy()
    
    
    if orientacion == Orientacion.Horizontal:
        demandas_filas_cp[i] -= len_barco
        for k in range(j, j + len_barco):
            demandas_columnas_cp[k] -= 1

    if orientacion == Orientacion.Vertical:
        demandas_columnas_cp[j] -= len_barco
        for k in range(i, i + len_barco):
            demandas_filas_cp[k] -= 1
    
    return demandas_filas_cp, demandas_columnas_cp

    
def batalla_naval_BT(tablero: List[List[int]], barcos: List[int], demandas_filas: List[int], demandas_columnas: List[int], mejor_solucion: List[Tuple[List[List[int]], int]], barco_actual: int = 0, not_repeat: bool = False):
    n = len(demandas_filas)
    m = len(demandas_columnas)

    if barco_actual >= len(barcos):
        return

    barco = barcos[barco_actual]

    if not_repeat and barco_actual >= 1 and barco == barcos[barco_actual-1]:
        batalla_naval_BT(tablero, barcos, demandas_filas, demandas_columnas, mejor_solucion, barco_actual+1, True)
        return
    

    demanda_incumplida = sum(demandas_filas) + sum(demandas_columnas)

    if mejor_solucion[0] is None or demanda_incumplida < mejor_solucion[0][1]:
        mejor_solucion[0] = (np.copy(tablero), demanda_incumplida)
        
    
    for i in range(n):
        if demandas_filas[i] == 0:
            continue
        for j in range(m):
            if demandas_filas[j] == 0:
                continue
            for orientacion in Orientacion:
                if puede_colocar_barco(tablero, barco, demandas_filas, demandas_columnas, i, j, orientacion):
                    colocar_barco(tablero, barco, i, j, orientacion)
                    nueva_demanda_filas, nueva_demanda_columnas = actualizar_demandas(barco, i, j, orientacion, demandas_filas, demandas_columnas)
                    batalla_naval_BT(tablero, barcos, nueva_demanda_filas, nueva_demanda_columnas, mejor_solucion, barco_actual+1)
                    remover_barco(tablero, barco, i, j, orientacion)
        
    # Intentar omitir el barco actual
    batalla_naval_BT(tablero, barcos, demandas_filas, demandas_columnas, mejor_solucion, barco_actual+1, True)

def batalla_naval(tablero: List[List[int]], barcos: List[int], demandas_filas: List[int], demandas_columnas: List[int]) -> Tuple[List[List[int]], int]:
    mejor_solucion = [None]
    batalla_naval_BT(tablero, barcos, demandas_filas, demandas_columnas, mejor_solucion)
    return mejor_solucion[0]


def parsear_archivo(archivo: str) -> Tuple[List[List[int]], List[int], List[int], List[int]]:
    with open(archivo, "r") as file:
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
        
    print(f"demandas_filas: {demandas_filas}")
    print(f"demandas_columnas: {demandas_columnas}")
    tablero = np.zeros((len(demandas_filas), len(demandas_columnas)), dtype=int)
    return tablero, barcos, demandas_filas, demandas_columnas

if __name__ == "__main__":
    tablero, barcos, demandas_filas, demandas_columnas = parsear_archivo("./archivos_pruebas/10_10_10.txt")
    barcos.sort(reverse=True)
    mejor_tablero, demanda_incumplida = batalla_naval(tablero, barcos, demandas_filas, demandas_columnas)
    print(mejor_tablero, demanda_incumplida)

""" 
    tablero, barcos, demandas_filas, demandas_columnas = parsear_archivo("./archivos_pruebas/3_3_2.txt")
    mejor_tablero, demanda_incumplida = batalla_naval(tablero, barcos, demandas_filas, demandas_columnas)
    print(mejor_tablero, demanda_incumplida)

    tablero, barcos, demandas_filas, demandas_columnas = parsear_archivo("./archivos_pruebas/5_5_6.txt")
    mejor_tablero, demanda_incumplida = batalla_naval(tablero, barcos, demandas_filas, demandas_columnas)
    print(mejor_tablero, demanda_incumplida)

    tablero, barcos, demandas_filas, demandas_columnas = parsear_archivo("./archivos_pruebas/8_7_10.txt")
    mejor_tablero, demanda_incumplida = batalla_naval(tablero, barcos, demandas_filas, demandas_columnas)
    print(mejor_tablero, demanda_incumplida)


    tablero, barcos, demandas_filas, demandas_columnas = parsear_archivo("./archivos_pruebas/10_10_10.txt")
    mejor_tablero, demanda_incumplida = batalla_naval(tablero, barcos, demandas_filas, demandas_columnas)
    print(mejor_tablero, demanda_incumplida)

    tablero, barcos, demandas_filas, demandas_columnas = parsear_archivo("./archivos_pruebas/12_12_21.txt")
    mejor_tablero, demanda_incumplida = batalla_naval(tablero, barcos, demandas_filas, demandas_columnas)
    print(mejor_tablero, demanda_incumplida)

    tablero, barcos, demandas_filas, demandas_columnas = parsear_archivo("./archivos_pruebas/15_10_15.txt")
    mejor_tablero, demanda_incumplida = batalla_naval(tablero, barcos, demandas_filas, demandas_columnas)
    print(mejor_tablero, demanda_incumplida)

    tablero, barcos, demandas_filas, demandas_columnas = parsear_archivo("./archivos_pruebas/20_20_20.txt")
    mejor_tablero, demanda_incumplida = batalla_naval(tablero, barcos, demandas_filas, demandas_columnas)
    print(mejor_tablero, demanda_incumplida)

    tablero, barcos, demandas_filas, demandas_columnas = parsear_archivo("./archivos_pruebas/20_25_30.txt")
    mejor_tablero, demanda_incumplida = batalla_naval(tablero, barcos, demandas_filas, demandas_columnas)
    print(mejor_tablero, demanda_incumplida)

    tablero, barcos, demandas_filas, demandas_columnas = parsear_archivo("./archivos_pruebas/30_25_25.txt")
    mejor_tablero, demanda_incumplida = batalla_naval(tablero, barcos, demandas_filas, demandas_columnas)
    print(mejor_tablero, demanda_incumplida) """