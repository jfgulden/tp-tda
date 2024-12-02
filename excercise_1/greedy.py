import sys
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
    file.close()
    return monedas
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 excercise_1/greedy.py <archivo>")
        sys.exit(1)

    archivo = sys.argv[1]
    try:
        monedas = obtener_monedas_de_archivo(archivo)
        resultado = obtener_ganador(monedas)
        print(f"Sofia obtiene la maxima ganancia y es: {resultado}")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
"""
Complejidad: 
    - Temporal: O(n), siendo n la cantidad total de monedas.
    - Espacial: O(n), siendo n la cantidad total de monedas.
"""