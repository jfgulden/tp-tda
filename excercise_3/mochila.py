from typing import List, Tuple

import numpy as np

from backtracking import generar_tablero


def probar_combinacion(board, boats, values, capacidad, index, current_value, best_value, best_combination):
    if index == len(boats):
        # Evaluar la combinación actual
        demandas_filas = [capacidad]  # Demanda total para la fila
        demandas_columnas = [1] * capacidad  # Demanda de 1 por cada columna
        tablero, _ = generar_tablero(1, capacidad, [sum(board)], demandas_filas, demandas_columnas)
        if np.sum(tablero) == sum(board):  # Si la combinación es válida
            if current_value > best_value[0]:
                best_value[0] = current_value
                best_combination[:] = board[:]
        return
    
    # Incluir el barco actual
    if sum(board) + boats[index] <= capacidad:  # Verificar si añadir este barco supera la capacidad
        board.append(boats[index])
        probar_combinacion(board, boats, values, capacidad, index + 1, current_value + values[index], best_value, best_combination)
        board.pop()  # Remover el barco para probar sin él
    
    # No incluir el barco actual
    probar_combinacion(board, boats, values, capacidad, index + 1, current_value, best_value, best_combination)

def resolver_mochila_batalla_naval(boats, values, capacidad):
    best_value = [0]
    best_combination = []
    probar_combinacion([], boats, values, capacidad, 0, 0, best_value, best_combination)
    return best_combination, best_value[0]


# Datos de ejemplo
pesos = [10, 20, 30]
valores = [60, 100, 120]
capacidad = 50

mejor_combinacion, max_valor = resolver_mochila_batalla_naval(pesos, valores, capacidad)
print("Mejor combinación de pesos:", mejor_combinacion)
print("Valor total maximizado:", max_valor)

# Prueba de la función con un caso de ejemplo
pesos = [10, 20, 30]
valores = [60, 100, 120]
capacidad = 50

# resultado = mochila_a_batalla_naval(pesos, valores, capacidad)
# print("Elementos seleccionados (valor, peso):", resultado[0])
# print("Valor total:", resultado[1])
# # Output esperado: [(20, 100), (30, 120)] 