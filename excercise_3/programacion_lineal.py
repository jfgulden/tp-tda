import time
import pulp
from typing import List, Tuple
import os
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


def batalla_naval_pl(barcos, demandas_filas, demandas_columnas):
    filas = len(demandas_filas)
    columnas = len(demandas_columnas)

    # posible optimizacion: guardar en una matriz
    tablero = pulp.LpVariable.dicts(
        "tablero", ((i, j) for i in range(filas) for j in range(columnas)), cat="Binary"
    )

    tuples = []

    for i in range(len(barcos)):
        for x in range(filas):
            for y in range(columnas):
                for o in [0, 1]:
                    tuples.append((i, barcos[i], x, y, o))

    pos_barcos = pulp.LpVariable.dicts(
        "pos_barcos",
        tuples,
        cat="Binary",
    )
    
    problema = pulp.LpProblem("Battleship", pulp.LpMaximize)

    # Función objetivo: maximizar la cantidad de celdas ocupadas
    problema += pulp.lpSum(tablero[x, y] for x in range(filas) for y in range(columnas))

    # RESTRICCIONES

    # No se pueden colocar mas que la suma de barcos
    problema += pulp.lpSum(
        tablero[x, y] for x in range(filas) for y in range(columnas)
    ) <= sum(barcos)

    # Asegurar que cada barco este colocado a lo sumo una vez
    for i in range(len(barcos)):
        problema += (
            pulp.lpSum(
                pos_barcos[i, barcos[i], x, y, o]
                for x in range(filas)
                for y in range(columnas)
                for o in [0, 1]
            )
            <= 1
        )

    # Asegurar que cada celda este ocupada a lo sumo una vez
    for x in range(filas):
        for y in range(columnas):
            problema += (
                pulp.lpSum(
                    pos_barcos[i, barcos[i], x, y, o]
                    for i in range(len(barcos))
                    for o in [0, 1]
                )
                <= 1
            )

    # Asegurar que una celda solo pueda ser ocupada por un barco
    for x in range(filas):
        for y in range(columnas):
            # La celda está ocupada solo si algún barco está posicionado para cubrirla
            problema += tablero[x, y] == pulp.lpSum(
                pos_barcos[i, l, xb, yb, o]
                for i, l in enumerate(barcos)
                for xb in range(filas)
                for yb in range(columnas)
                for o in [0, 1]
                if (
                    (o == 0 and xb == x and yb <= y and yb + l > y)  # Horizontal
                    or (o == 1 and yb == y and xb <= x and xb + l > x)  # Vertical
                )
            )

    for f in range(filas):
        suma_ocupadas_fila = pulp.lpSum(tablero[f, c] for c in range(columnas))

        # La suma de ocupadas no puede superar la demanda de la fila
        problema += suma_ocupadas_fila <= demandas_filas[f]


    for c in range(columnas):
        suma_ocupadas_columna = pulp.lpSum(tablero[f, c] for f in range(filas))

        # La suma de ocupadas no puede superar la demanda de la columna
        problema += suma_ocupadas_columna <= demandas_columnas[c]


    # Restricciones para la colocación válida de los barcos
    for x in range(filas):
        for y in range(columnas):
            for o in [0, 1]:  # 0: horizontal, 1: vertical
                for i in range(len(barcos)):
                    l = barcos[i]
                    # Colocación horizontal
                    if o == 0 and y + l - 1 < columnas:
                        # Asegurar que las celdas ocupadas por el barco estén marcadas
                        for largo in range(l):
                            problema += (
                                tablero[x, y + largo] >= pos_barcos[i, l, x, y, o]
                            )

                        # Asegurar que las celdas adyacentes no estén ocupadas

                        # Fila superior adyacente
                        if x > 0:

                            # Esquina superior izquierda
                            if y > 0:
                                problema += (
                                    tablero[x - 1, y - 1] + pos_barcos[i, l, x, y, o]
                                    <= 1
                                )

                            # Esquina superior derecha
                            if y + l < columnas:
                                problema += (
                                    tablero[x - 1, y + l] + pos_barcos[i, l, x, y, o]
                                    <= 1
                                )

                            for largo in range(l):
                                problema += (
                                    tablero[x - 1, y + largo]
                                    + pos_barcos[i, l, x, y, o]
                                    <= 1
                                )

                        # Fila inferior adyacente
                        if x < filas - 1:

                            if y > 0:  # Esquina inferior izquierda
                                problema += (
                                    tablero[x + 1, y - 1] + pos_barcos[i, l, x, y, o]
                                    <= 1
                                )

                            if y + l < columnas:  # Esquina inferior derecha
                                problema += (
                                    tablero[x + 1, y + l] + pos_barcos[i, l, x, y, o]
                                    <= 1
                                )

                            for largo in range(l):
                                problema += (
                                    tablero[x + 1, y + largo]
                                    + pos_barcos[i, l, x, y, o]
                                    <= 1
                                )

                        if y > 0:  # Columna izquierda adyacente
                            problema += (
                                tablero[x, y - 1] + pos_barcos[i, l, x, y, o] <= 1
                            )

                        if y + l < columnas:  # Right adjacent column
                            problema += (
                                tablero[x, y + l] + pos_barcos[i, l, x, y, o] <= 1
                            )

                    # Colocación vertical
                    elif o == 1 and x + l - 1 < filas:
                        # Ensure the cells occupied by the boat are marked
                        for largo in range(l):
                            problema += (
                                tablero[x + largo, y] >= pos_barcos[i, l, x, y, o]
                            )

                        # Assegurar que las celdas adyacentes no estén ocupadas
                        # Fila adyacente izquierda
                        if y > 0:

                            # Esquina superior izquierda
                            if x > 0:
                                problema += (
                                    tablero[x - 1, y - 1] + pos_barcos[i, l, x, y, o]
                                    <= 1
                                )

                            # Esquina inferior izquierda
                            if x + l < filas:
                                problema += (
                                    tablero[x + l, y - 1] + pos_barcos[i, l, x, y, o]
                                    <= 1
                                )

                            for largo in range(l):
                                problema += (
                                    tablero[x + largo, y - 1]
                                    + pos_barcos[i, l, x, y, o]
                                    <= 1
                                )

                        # Fila adyacente derecha
                        if y < columnas - 1:

                            # Esquina superior derecha
                            if x > 0:
                                problema += (
                                    tablero[x - 1, y + 1] + pos_barcos[i, l, x, y, o]
                                    <= 1
                                )

                            # Esquina inferior derecha
                            if x + l < filas:
                                problema += (
                                    tablero[x + l, y + 1] + pos_barcos[i, l, x, y, o]
                                    <= 1
                                )

                            for largo in range(l):
                                problema += (
                                    tablero[x + largo, y + 1]
                                    + pos_barcos[i, l, x, y, o]
                                    <= 1
                                )

                        # Fila superior adyacente
                        if x > 0:
                            problema += (
                                tablero[x - 1, y] + pos_barcos[i, l, x, y, o] <= 1
                            )

                        # Fila inferior adyacente
                        if x + l < filas:
                            problema += (
                                tablero[x + l, y] + pos_barcos[i, l, x, y, o] <= 1
                            )

                    else:
                        # no entra en el tablero. no se puede colocar
                        problema += pos_barcos[i, l, x, y, o] == 0

    # Resolver el problema
    problema.solve(pulp.PULP_CBC_CMD(msg=False))

    # convert tablero into a matrix
    tablero = [[tablero[x, y].varValue for y in range(columnas)] for x in range(filas)]

    # calcular demanda insatisfecha
    celdas_ocupadas = sum(tablero[x][y] for x in range(filas) for y in range(columnas))

    demanda_insatisfecha = (
        sum(demandas_filas) + sum(demandas_columnas) - celdas_ocupadas * 2
    )
    demanda_satisfecha = (
        sum(demandas_filas) + sum(demandas_columnas) - demanda_insatisfecha
    )

    return tablero, demanda_satisfecha, demanda_insatisfecha


if __name__ == "__main__":

    files = []

    files.append("3_3_2")
    files.append("5_5_6")
    files.append("8_7_10")
    files.append("10_3_3")
    files.append("10_10_10")

    for file in files:
        print(f"File: {file}")

        tablero, barcos, demandas_filas, demandas_columnas = parsear_archivo(
            f"excercise_3/archivos_pruebas/{file}.txt"
        )
        demanda_total = sum(demandas_filas) + sum(demandas_columnas)
        start_time = time.time()
        tablero, demanda_satisfecha, demanda_insatisfecha = batalla_naval_pl(
            barcos, demandas_filas, demandas_columnas
        )
        end_time = time.time()

        # pretty print tablero
        for row in tablero:
            print("".join("X " if cell == 1 else "- " for cell in row))
        print()
        print(f"Demanda satisfecha: {demanda_satisfecha}")
        print(f"Demanda total: {demanda_total}")
        print(f"Demanda insatisfecha: {demanda_insatisfecha}")
        print(f"Execution time: {end_time - start_time} seconds")

        # Ensure the results directory exists
        os.makedirs("excercise_3/results", exist_ok=True)

        # save results to file
        with open(f"excercise_3/results/{file}_pl.txt", "w") as f:
            for row in tablero:
                f.write("".join("X " if cell == 1 else "- " for cell in row) + "\n")
            f.write("\n")
            f.write(f"Demanda satisfecha: {demanda_satisfecha}\n")
            f.write(f"Demanda total: {demanda_total}\n")
            f.write(f"Demanda insatisfecha: {demanda_insatisfecha}\n")
            f.write(f"Execution time: {end_time - start_time} seconds\n")
