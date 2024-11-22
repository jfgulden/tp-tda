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
RUNS_PER_SIZE = 8

# Ajustar este valor si se quiere usar más de un proceso para medir los tiempos
# de ejecución, o None para usar todos los procesadores disponibles. Si se usan
# varios procesos, tener cuidado con el uso de memoria del sistema.
MAX_WORKERS = (os.cpu_count() or 4) // 4


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











































