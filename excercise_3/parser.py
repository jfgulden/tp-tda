from typing import List, Tuple

import numpy as np


def parsear_archivo(
    archivo: str,
) -> Tuple[List[List[int]], List[int], List[int], List[int]]:
    with open(archivo, "r") as file:
        i = 0
        demandas_filas = []
        demandas_columnas = []
        barcos = []

        for index, line in enumerate(file):
            if index < 2:
                continue
            if line.strip() == "":
                i += 1
                continue
            if i == 0:
                demandas_filas.append(int(line.strip()))
            elif i == 1:
                demandas_columnas.append(int(line.strip()))
            elif i == 2:
                barcos.append(int(line.strip()))

    # print(f"demandas_filas: {demandas_filas}")
    # print(f"demandas_columnas: {demandas_columnas}")
    tablero = np.zeros((len(demandas_filas), len(demandas_columnas)), dtype=int)
    return tablero, barcos, demandas_filas, demandas_columnas
