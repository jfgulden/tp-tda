

def obtener_ganador(monedas):
    # Turno Sophia: Agarra la moneda más grande
    # Turno Mateo: Agarra la moneda más chica
    inicio = 0
    fin = len(monedas) - 1
    monedas_sofia = []

    for i in range(len(monedas)): # len(monedas): Turnos totales
        primera = monedas[inicio]
        ultima = monedas[fin]
        if i % 2 == 0:
            if primera > ultima:
                monedas_sofia.append(primera)
                inicio += 1
            else:
                monedas_sofia.append(ultima)
                fin -= 1
        else:
            if primera >= ultima:
                fin -= 1
            else:
                inicio += 1


    return sum(monedas_sofia)

def obtener_monedas_de_archivo(file: str):
    file = open(file, "r")
    file.readline()
    monedas = list(map(int, file.readline().strip().split(';')))
    return monedas

"""
Complejidad: 
    - Temporal: O(n), siendo n la cantidad total de monedas.
    - Espacial: O(n), siendo n la cantidad total de monedas.
"""
monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/20.txt")
print(obtener_ganador(monedas))

monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/25.txt")
print(obtener_ganador(monedas))

monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/50.txt")
print(obtener_ganador(monedas))

monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/100.txt")
print(obtener_ganador(monedas))

monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/1000.txt")
print(obtener_ganador(monedas))

monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/10000.txt")
print(obtener_ganador(monedas))

monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/20000.txt")
print(obtener_ganador(monedas))
