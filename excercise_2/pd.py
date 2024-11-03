import sys
sys.setrecursionlimit(5000)

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


# Los prints para mostrar las monedas sacadas por Sofia están comentados para mantener la legibilidad de los outputs. 
# Descomentarlos de ser necesario.

monedas_5 = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/5.txt")
solucion_5 = maxima_ganancia_sofia(monedas_5)
print("Prueba con 5 monedas:")
# print(f"\tmonedas sacadas por Sofia: {solucion_5}")
print(f"\tmonto obtenido por Sofia: {sum(solucion_5)}")

monedas_10 = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/10.txt")
solucion_10 = maxima_ganancia_sofia(monedas_10)
print("Prueba con 10 monedas:")
# print(f"\tmonedas sacadas por Sofia: {solucion_10}")
print(f"\tmonto obtenido por Sofia: {sum(solucion_10)}")

monedas_20 = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/20.txt")
solucion_20 = maxima_ganancia_sofia(monedas_20)
print("Prueba con 20 monedas:")
# print(f"\tmonedas sacadas por Sofia: {solucion_20}")
print(f"\tmonto obtenido por Sofia: {sum(solucion_20)}")

monedas_25 = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/25.txt")
solucion_25 = maxima_ganancia_sofia(monedas_25)
print("Prueba con 25 monedas:")
# print(f"\tmonedas sacadas por Sofia: {solucion_25}")
print(f"\tmonto obtenido por Sofia: {sum(solucion_25)}")

monedas_50 = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/50.txt")
solucion_50 = maxima_ganancia_sofia(monedas_50)
print("Prueba con 50 monedas:")
# print(f"\tmonedas sacadas por Sofia: {solucion_50}")
print(f"\tmonto obtenido por Sofia: {sum(solucion_50)}")

monedas_100 = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/100.txt")
solucion_100 = maxima_ganancia_sofia(monedas_100)
print("Prueba con 100 monedas:")
# print(f"\tmonedas sacadas por Sofia: {solucion_100}")
print(f"\tmonto obtenido por Sofia: {sum(solucion_100)}")

monedas_1000 = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/1000.txt")
solucion_1000 = maxima_ganancia_sofia(monedas_1000)
print("Prueba con 1000 monedas:")
# print(f"\tmonedas sacadas por Sofia: {solucion_1000}")
print(f"\tmonto obtenido por Sofia: {sum(solucion_1000)}")

monedas_2000 = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/2000.txt")
solucion_2000 = maxima_ganancia_sofia(monedas_2000)
print("Prueba con 2000 monedas:")
#print(f"\tmonedas sacadas por Sofia: {solucion_2000}")
print(f"\tmonto obtenido por Sofia: {sum(solucion_2000)}")

monedas_5000 = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/5000.txt")
solucion_5000 = maxima_ganancia_sofia(monedas_5000)
print("Prueba con 5000 monedas:")
# print(f"\tmonedas sacadas por Sofia: {solucion_5000}")
print(f"\tmonto obtenido por Sofia: {sum(solucion_5000)}")

monedas_10000 = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/10000.txt")
solucion_10000 = maxima_ganancia_sofia(monedas_10000)
print("Prueba con 10000 monedas:")
# print(f"\tmonedas sacadas por Sofia: {solucion_10000}")
print(f"\tmonto obtenido por Sofia: {sum(solucion_10000)}")
