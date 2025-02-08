import os
import sys

import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from excercise_3.aproximacion import naval_approximation, parsear_archivo


def calculate_approximation_difference(input_dir_tests, input_dir_results):
    """
    Calcula la diferencia entre el resultado oficial y el resultado aproximado
    para cada archivo en el directorio.

    input_dir_tests: Directorio con los archivos de prueba
                    (test_aproximacion_i.txt)
    input_dir_results: Directorio con los resultados oficiales
                    (result_test_aproximacion_i.txt)
    """
    differences = []

    for file_name in sorted(os.listdir(input_dir_tests)):
        try:
            if (file_name.startswith("test_aproximacion_") and
                    file_name.endswith(".txt")):
                test_file_path = os.path.join(input_dir_tests, file_name)
                result_file_name = f"result_{file_name}"
                result_file_path = os.path.join(
                    input_dir_results, result_file_name)

                if os.path.exists(result_file_path):
                    with open(result_file_path, "r") as result_file:
                        official_result = int(
                            result_file.readline().strip()
                        )
                    demands_rows, demands_cols, ships = parsear_archivo(test_file_path)
                    demanda_inicial = np.sum(demands_rows) + np.sum(demands_cols)
                    result_board = naval_approximation(
                        demands_rows, demands_cols, ships
                    )
                    demanda_insatisfecha = np.sum(demands_rows) + np.sum(demands_cols)
                    approx_result = demanda_inicial - demanda_insatisfecha

                    # Calcular la diferencia
                    difference = abs(approx_result - official_result)
                    differences.append(
                        (file_name, official_result, approx_result, difference)
                    )
                    print(
                        f"{file_name}: Official={official_result}, Approx={approx_result}, Difference={difference}"
                    )
        except Exception as e:
            print(f"Error al procesar {file_name}: {e}")
    # Guardar las diferencias en un archivo de salida
    with open("differences_results.txt", "w") as output_file:
        for file_name, official, approx, diff in differences:
            output_file.write(
                f"{file_name}: Official={official}, Approx={approx}, Difference={diff}\n"
            )

    print(
        "\nProccess completed. Differences saved in differences_results.txt file."
    )


if __name__ == "__main__":
    input_dir_tests = "excercise_3/pruebas_alumnos/pruebas_aproximacion"
    input_dir_results = "excercise_3/pruebas_alumnos/resultados_pruebas_aproximacion"
    calculate_approximation_difference(input_dir_tests, input_dir_results)
