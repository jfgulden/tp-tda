from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from pd import maxima_ganancia_sofia


# Este parámetro controla cuantas veces se ejecuta el algoritmo para cada
# tamaño. Esto es conveniente para reducir el error estadístico en la medición
# de tiempos. Al finalizar las ejecuciones, se promedian los tiempos obtenidos
RUNS_PER_SIZE = 2

# Ajustar este valor si se quiere usar más de un proceso para medir los tiempos
# de ejecución, o None para usar todos los procesadores disponibles. Si se usan
# varios procesos, tener cuidado con el uso de memoria del sistema.
MAX_WORKERS = 4


def _time_run(algorithm, *args):
    start = time.time()
    algorithm(*args)
    return time.time() - start

def time_algorithm(algorithm, sizes, get_args):
    futures = {}
    total_times = {i: 0 for i in sizes}

    # Usa un ProcessPoolExecutor para ejecutar las mediciones en paralelo
    # (el ThreadPoolExecutor no sirve por el GIL de Python)
    with ProcessPoolExecutor(MAX_WORKERS) as p:
        for i in sizes:
            for _ in range(RUNS_PER_SIZE):
                futures[p.submit(_time_run, algorithm, *get_args(i))] = i

        for f in as_completed(futures):
            result = f.result()
            i = futures[f]
            total_times[i] += result

    return {s: t / RUNS_PER_SIZE for s, t in total_times.items()}

def get_random_array(size: int):
    return np.random.randint(0, 100.000, size)


if __name__ == '__main__':
    # La variable x van a ser los valores del eje x de los gráficos en todo el notebook
    # Tamaño mínimo=100, tamaño máximo=10kk, cantidad de puntos=20
    # x = np.linspace(100, 1_000_000, 20).astype(int)
    x = np.linspace(100, 5_000, 20).astype(int)

    results = time_algorithm(maxima_ganancia_sofia, x, lambda s: [get_random_array(s)])

    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.plot(x, [results[i] for i in x], label="Medición")
    ax.set_title('Tiempo de ejecución de monedas programacion dinamica')
    ax.set_xlabel('Tamaño del array')
    ax.set_ylabel('Tiempo de ejecución (s)')
    None

    # Ajuste de curva por mínimos cuadrados
    # La función que ajustamos es c1 * x + c2
    # donde c1 y c2 son los coeficientes que queremos encontrar

    f = lambda x, c1, c2: c1 * x**2 + c2

    c, pcov = sp.optimize.curve_fit(f, x, [results[n] for n in x])

    print(f"c_1 = {c[0]}, c_2 = {c[1]}")
    r = np.sum((c[0] * x * x + c[1] - [results[n] for n in x])**2)
    print(f"Error cuadrático total: {r}")

    ax.plot(x, [c[0] * n **2 + c[1] for n in x], 'r--', label="Ajuste")
    ax.legend()
    fig
    plt.savefig("excercise_2/mediciones.png")


    # Graficamos el error de ajuste

    ax: plt.Axes
    fig, ax = plt.subplots()
    errors = [np.abs(c[0] * n ** 2 + c[1] - results[n]) for n in x]
    ax.plot(x, errors)
    ax.set_title('Error de ajuste')
    ax.set_xlabel('Tamaño del array')
    ax.set_ylabel('Error absoluto (s)')
    plt.savefig("excercise_2/error_ajuste.png")
    None 

    """
    Nos interesa medir los tiempos de ejecucion para valores de monedas que varíen en rango
    Para esto tenemos una carpeta 'tests_distintos_rangos', en donde se encuentran distintos archivos de prueba con monedas que varían en rango, con la misma cantidad de monedas.
    """
    archivos_tests = [archivo for archivo in  os.listdir("excercise_2/tests_distintos_rangos") if archivo.endswith('.txt')]
    archivos_tests.sort(key=lambda archivo: int(archivo.split('_')[2].split('.')[0]))
    cantidad_monedas = [nombre_archivo.split('_')[2].split('.')[0] for nombre_archivo in archivos_tests]
    execution_times = []
    for file in archivos_tests:
        file = open(f"excercise_2/tests_distintos_rangos/{file}", "r")
        file.readline()
        monedas = list(map(int, file.readline().strip().split(';')))
        start_time = time.time()
        maxima_ganancia_sofia(monedas)
        end_time = time.time()
        execution_times.append(end_time - start_time)
        
    fig = plt.figure(figsize = (10, 5))

    # creating the bar plot
    plt.bar(cantidad_monedas, execution_times, color ='tab:blue', width = 0.4)
    plt.xlabel("Rango (desde cero hasta el valor)")
    plt.ylabel("Tiempo de ejecución (s)")
    plt.title("Tiempos de ejecución para distintos rangos de monedas")
    plt.savefig("excercise_2/tiempos_ejecucion_rangos_distintos.png")  # Guardar el gráfico en un archivo
    plt.close()  # Cierra la figura para liberar memoria
        
