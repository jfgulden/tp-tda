import sys
import time
def maxima_ganancia_sofia(monedas):
    # Turno Sophia: Agarra la moneda más grande
    # Turno Mateo: Agarra la moneda más chica
    inicio = 0
    fin = len(monedas) - 1
    monedas_sofia = []

    for i in range(len(monedas)): # len(monedas): Turnos totales
        primera = monedas[inicio]
        ultima = monedas[fin]
        if i % 2 == 0:
            print(f"Monedas restantes: {monedas[inicio:fin+1]}")
            if primera > ultima:
                monedas_sofia.append(primera)
                inicio += 1
                print(f"Sofia toma la moneda {primera}")
            else:
                monedas_sofia.append(ultima)
                fin -= 1
                print(f"Sofia toma la moneda {primera}")
        else:
            if primera >= ultima:
                fin -= 1
                print(f"Mateo toma la moneda {ultima}\n")
            else:
                inicio += 1
                print(f"Mateo toma la moneda {primera}\n")

    return monedas_sofia

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
        start_time = time.time()
        monedas_sofia = maxima_ganancia_sofia(monedas)
        end_time = time.time()
        print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
        print(f"Monedas sacadas por Sofia: {monedas_sofia}")
        print(f"Monto obtenido por Sofia: {sum(monedas_sofia)}")
        print(f"Tiempo de ejecución: {end_time - start_time:.6f} segundos")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
"""
Complejidad: 
    - Temporal: O(n), siendo n la cantidad total de monedas.
    - Espacial: O(n), siendo n la cantidad total de monedas.
"""