import sys
from pd import maxima_ganancia_sofia, obtener_monedas_de_archivo
import time
import os
from typing import List

TEST_FILES_PATH = "excercise_2/archivos_pruebas/"

def es_archivo_numerico(archivo):
    try:
        int(archivo.split('.')[0])
        return True
    except ValueError:
        return False

def mostrar_resultado(monedas: List[int], verbose: bool):
    tiempo_inicio = time.time()
    solucion = maxima_ganancia_sofia(monedas)
    tiempo_fin = time.time()
    tiempo_ejecucion = tiempo_fin - tiempo_inicio
    print("=====================================================================================")
    print(f"Prueba con {len(monedas)} monedas:")
    if verbose:
        print(f"\tmonedas sacadas por Sofia: {solucion}")
        
    print(f"\tMonto obtenido por Sofia:   $ {sum(solucion)}")
    print(f"\tTiempo de ejecución:        {tiempo_ejecucion:.6f} segundos")
    print("=====================================================================================")

if __name__ == "__main__":
    verbose: bool = "-v" in sys.argv or "--verbose" in sys.argv
    
    archivos_tests = [archivo for archivo in  os.listdir(TEST_FILES_PATH) if archivo.endswith('.txt') and es_archivo_numerico(archivo)]
    archivos_tests.sort(key=lambda archivo: int(archivo.split('.')[0]))

    for nombre_archivo in archivos_tests:
        monedas = obtener_monedas_de_archivo(f"{TEST_FILES_PATH}{nombre_archivo}")
        mostrar_resultado(monedas, verbose)