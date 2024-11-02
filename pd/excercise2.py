def obtener_monedas_de_archivo(file: str):
    file = open(file, "r")
    file.readline()
    monedas = list(map(int, file.readline().strip().split(';')))
    return monedas

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

    return matriz_solucion[n-1][0]


monedas = obtener_monedas_de_archivo("pd/archivos_pruebas/10.txt")
print("Valor máximo que sofia puede obtener 10 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("pd/archivos_pruebas/20.txt")
print("Valor máximo que sofia puede obtener 20 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("pd/archivos_pruebas/25.txt")
print("Valor máximo que sofia puede obtener 25 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("pd/archivos_pruebas/50.txt")
print("Valor máximo que sofia puede obtener 50 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("pd/archivos_pruebas/100.txt")
print("Valor máximo que sofia puede obtener 100 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("pd/archivos_pruebas/1000.txt")
print("Valor máximo que sofia puede obtener 1000 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("pd/archivos_pruebas/2000.txt")
print("Valor máximo que sofia puede obtener 2000 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("pd/archivos_pruebas/5000.txt")
print("Valor máximo que sofia puede obtener 5000 monedas:", maxima_ganancia_sofia(monedas))
monedas = obtener_monedas_de_archivo("pd/archivos_pruebas/10000.txt")
print("Valor máximo que sofia puede obtener 10000 monedas:", maxima_ganancia_sofia(monedas))