from pulp import LpProblem, LpVariable, lpSum, LpStatus, value, LpMaximize
import numpy as np
from typing import List

def generar_tablero(y: List[int], pi: List[int], pj: List[int], o: List[int]) -> np.ndarray:
    n = len(y)
    m = len(y[0])
    tablero = np.zeros((n, m))
    for k in range(len(y)):
        if y[k]:
            if o[k]:
                tablero[pi[k]:pi[k]+barcos[k], pj[k]] = 1
            else:
                tablero[pi[k], pj[k]:pj[k]+barcos[k]] = 1
    return tablero

def batalla_naval_pl(barcos: List[int], demanda_filas: List[int], demanda_columnas: List[int]): 
    n = len(demanda_filas)
    m = len(demanda_columnas)
    o = []
    z = []
    y = []
    
    for k in range(len(barcos)):
        y.append(LpVariable(f"y_{k}", cat="Binary"))
        z.append([LpVariable(f"z_{i}_{j}", cat="Binary") for j in range(m)] for i in range(n))
        o.append(LpVariable(f"o_{k}", cat="Binary"))
    
    problem = pulp.LpProblem("battleship", pulp.LpMaximize)
    
    x = [LpVariable("z_{i}_{j}", cat="Binary") for j in range(m)] for i in range(n)
    
    
    
    # Restricciones
    
    # Restricción 1: Cada barco puede estar o no estar. Solo queremos que quede la posicion de inicio.
    for k, len_barco in enumerate(barcos):
        problem += lpSum(z[k][i][j] for i in range(n) for j in range(m)) == len_barco * y[k]
        
    # Restricción 2: Los barcos deben poder entrar en el tablero segun longitud y orientación
    for k, len_barco in enumerate(barcos):
        for r in range(n):
            for c in range(m):
                
                problem += y[k] * z[k][r][c] * (r + (len_barco - 1) * (1 - o[k])) <= n - 1 
                problem += y[k] * z[k][r][c] * (c + (len_barco - 1) * o[k]) <= m - 1
                
    # Restricción 3: No superposición de barcos
    for k, len_barco in enumerate(barcos):
        for k_aux, len_barco_aux in enumerate(barcos):
            if k != k_aux:
                for r in range(n):
                    for c in range(m):
                        problem += z[k][r][c] + z[k_aux][r][c] <= 1 # No pueden comenzar en la misma celda
                        

    for k, len_barco in enumerate(barcos):
        pos_i, pos_j = 0, 0
        for r in range(n):
            for c in range(m):
                if z[k][r][c] == 1:
                    pos_i, pos_j = r, c
                    break
            
        for k_aux, len_barco_aux in enumerate(barcos):
            if k != k_aux:
                for r in range(n):
                    for c in range(m):
                        if c + len_barco <= m:
                            problem += z[k][r][c+len_barco] * o[k]
                            
                            
                         

    for r in range(n):
            for c in range(m):
                problem += pulp.lpSum(z[i][r][c] for i in range(len(barcos))) <= 1, f"No_superposicion_celda_{r}_{c}"
        
        # Restricción 4: Demanda de filas
        for r in range(n):
            problem += pulp.lpSum(z[i][r][c] for i in range(len(barcos)) for c in range(m)) >= demanda_filas[r], f"Demanda_fila_{r}"
        
        # Restricción 5: Demanda de columnas
        for c in range(m):
            problem += pulp.lpSum(z[i][r][c] for i in range(len(barcos)) for r in range(n)) >= demanda_columnas[c], f"Demanda_columna_{c}"

    # Restricciones de no adyacencia (prohibir cercanía entre barcos)
    for i in range(R):
        for j in range(C):
            if X[i][j] == 1:
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if 0 <= i + di < R and 0 <= j + dj < C:
                            problem += X[i + di][j + dj] <= 1, f"No_adyacente_{i}_{j}"

    # Restricciones de demanda (cumplimiento de filas y columnas)
    for i in range(R):
        problem += lpSum(X[i][j] for j in range(C)) + incumplida_filas[i] == demanda_filas[i], f"Demanda_fila_{i}"

    for j in range(C):
        problem += lpSum(X[i][j] for i in range(R)) + incumplida_columnas[j] == demanda_columnas[j], f"Demanda_columna_{j}"

    problem += lpSum(x)  # Objetivo
    problem.solve()
        
    return generar_tablero(value(y), value(pi), value(pj), value(o))



if __name__ == "__main__":
    barcos = [2, 3, 4]
    demanda_filas = [2, 3, 4]
    demanda_columnas = [2, 3, 4]
    tablero = batalla_naval_pl(barcos, demanda_filas, demanda_columnas)
    print(tablero)
