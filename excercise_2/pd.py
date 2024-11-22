import sys
sys.setrecursionlimit(6000)

def obtener_monedas_de_archivo(file: str):
    file = open(file, "r")
    file.readline()
    monedas = list(map(int, file.readline().strip().split(';')))
    return monedas


def reconstruir_solucion(monedas, matriz, inicio, fin, solucion):
    if fin == inicio:
        solucion.append(monedas[inicio])
        return solucion

    if fin - inicio == 1:
        if monedas[fin] > monedas[inicio]:
            solucion.append(monedas[fin])
            return solucion

        solucion.append(monedas[inicio])
        return solucion
        
    opt_1 = monedas[fin] + (matriz[fin-2][inicio] if monedas[fin-1] >= monedas[inicio] else matriz[fin-1][inicio+1])
    opt_2 = monedas[inicio] + (matriz[fin-1][inicio+1] if monedas[fin] >= monedas[inicio+1] else matriz[fin][inicio+2])

    if opt_1 > opt_2:
        solucion.append(monedas[fin])
        if monedas[fin-1] >= monedas[inicio]:
            return reconstruir_solucion(monedas, matriz, inicio, fin-2, solucion)   
        return reconstruir_solucion(monedas, matriz, inicio+1, fin-1, solucion) 

    solucion.append(monedas[inicio])
    if monedas[fin] >= monedas[inicio+1]:
            return reconstruir_solucion(monedas, matriz, inicio+1, fin-1, solucion)   
    return reconstruir_solucion(monedas, matriz, inicio+2, fin, solucion) 


def maxima_ganancia_sofia(monedas):
    n = len(monedas)
    
    #matriz_solucion: matriz_solucion[i][j] almacena la ganancia máxima que Sofia puede obtener en el rango [i, j]
    matriz_solucion = [[None] * n for _ in range(n)] #INICIALIZO EN 0 LA MATRIZ

    # Caso base: cuando solo hay una moneda disponible
    #inicializa la diagonal principal de la matriz_solucion
    for i in range(n):
        matriz_solucion[i][i] = monedas[i]

    for i in range(n - 1):
        matriz_solucion[i+1][i] = max(monedas[i], monedas[i+1])

    for i in range(2, n):  
        k = i
        for j in range(n - i):

            opt_1 = monedas[k] + (matriz_solucion[k-2][j] if monedas[k-1] >= monedas[j] else matriz_solucion[k-1][j+1])
            opt_2 = monedas[j] + (matriz_solucion[k-1][j+1] if monedas[k] >= monedas[j+1] else matriz_solucion[k][j+2])
            
            matriz_solucion[k][j] = max(opt_1, opt_2)
            k += 1

    solucion = []
    reconstruir_solucion(monedas, matriz_solucion, 0, n-1, solucion)
    return solucion

'''
Complejidad: O(n^2), siendo n la cantidad total de monedas. 
TODO: Desarrollar análisis de complejidad.
'''