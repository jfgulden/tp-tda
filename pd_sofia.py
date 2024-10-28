def obtener_monedas_de_archivo(file: str):
    file = open(file, "r")
    file.readline()
    monedas = list(map(int, file.readline().strip().split(';')))
    return monedas

def maxima_ganancia_sofia(monedas):
    n = len(monedas)
    
    #matriz_solucion: matriz_solucion[i][j] almacena la ganancia máxima que Sofia puede obtener en el rango [i, j]
    matriz_solucion = [[0] * n for _ in range(n)] #INICIALIZO EN 0 LA MATRIZ

    # Caso base: cuando solo hay una moneda disponible
    #inicializa la diagonal principal de la matriz_solucion
    for i in range(n):
        matriz_solucion[i][i] = monedas[i]

    # Llenamos la matriz de manera bottom-up
    for longitud in range(2, n + 1):  # longitud es el tamaño del rango actual
        for i in range(n - longitud + 1):
            j = i + longitud - 1  # Extremo derecho del rango

            # Opción 1: Sofia elige la moneda izquierda (monedas[i])
            # Luego Mateo elige la mayor entre monedas[i + 1] y monedas[j]
            if monedas[i + 1] >= monedas[j]:
                ganancia_post_eleccion_mateo_i = matriz_solucion[i + 2][j] if i + 2 <= j else 0
            else:
                ganancia_post_eleccion_mateo_i = matriz_solucion[i + 1][j - 1] if i + 1 <= j - 1 else 0
            opcion1 = monedas[i] + ganancia_post_eleccion_mateo_i

            # opcion 2 : Sofia elige la moneda derecha (monedas[j])
            # Luego Mateo elige la mayor entre monedas[i] y monedas[j - 1]
            if monedas[i] >= monedas[j - 1]:
                ganancia_post_eleccion_mateo_j = matriz_solucion[i + 1][j - 1] if i + 1 <= j - 1 else 0
            else:
                ganancia_post_eleccion_mateo_j = matriz_solucion[i][j - 2] if i <= j - 2 else 0
            opcion2 = monedas[j] + ganancia_post_eleccion_mateo_j

            # Sofia elige la opción que le da la mayor ganancia
            matriz_solucion[i][j] = max(opcion1, opcion2)

    # la solucion optima para sofia esta en [0][n-1]
    return matriz_solucion[0][n - 1]

monedas = obtener_monedas_de_archivo("TP2/5.txt")
print("Valor máximo que sofia puede obtener 5 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("TP2/10.txt")
print("Valor máximo que sofia puede obtener 10 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("TP2/20.txt")
print("Valor máximo que sofia puede obtener 20 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("TP2/25.txt")
print("Valor máximo que sofia puede obtener 25 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("TP2/50.txt")
print("Valor máximo que sofia puede obtener 50 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("TP2/100.txt")
print("Valor máximo que sofia puede obtener 100 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("TP2/1000.txt")
print("Valor máximo que sofia puede obtener 1000 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("TP2/2000.txt")
print("Valor máximo que sofia puede obtener 2000 monedas:", maxima_ganancia_sofia(monedas))

monedas = obtener_monedas_de_archivo("TP2/5000.txt")
print("Valor máximo que sofia puede obtener 5000 monedas:", maxima_ganancia_sofia(monedas))
monedas = obtener_monedas_de_archivo("TP2/10000.txt")
print("Valor máximo que sofia puede obtener 10000 monedas:", maxima_ganancia_sofia(monedas))