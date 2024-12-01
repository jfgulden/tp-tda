import unittest
import time
import sys
from excercise_1.test import suite as greedyTests
from excercise_2.test_pd import suite as pdTests
COLOR_ROJO = "\033[1;31m"
COLOR_VERDE = "\033[1;32m"
COLOR_AMARILLO = "\033[1;33m"
COLOR_AZUL = "\033[1;34m"
COLOR_MAGENTA = "\033[1;35m"
COLOR_CIAN = "\033[1;36m"


def mostrar_menu():
    print("\n MENU DE OPCIONES")
    print("1:Ejecutar Pruebas Greedy")
    print("2:Ejecutar Pruebas Programacion Dinamica")
    print("3:Ejecutar Pruebas Backtracking")
    print("0:Salir")

def ejecutar_suite(suite):
    runner = unittest.TextTestRunner()
    runner.run(suite)

def mostrar_barra_progreso():
    barra_longitud = 40  
    for i in range(barra_longitud + 1):
        porcentaje = int((i / barra_longitud) * 100)
        barra = f"[{'=' * i}{' ' * (barra_longitud - i)}] {porcentaje}%"
        sys.stdout.write("\r" + barra)  
        sys.stdout.flush()
        time.sleep(0.1)  
    print()  

def mostrar_mensaje(mensaje,color):
    print(f"{color}{mensaje}\033[0m")
    time.sleep(0.5)

def main():

    valor = -1
    while(valor != 0):
        mostrar_menu()
        valor = int(input("seleccione una opcion:"))
        if (valor == 1):
            mostrar_mensaje("\n\t\tEjecutando Pruebas Greedy",COLOR_AMARILLO)
            mostrar_mensaje("Cargando...",COLOR_AMARILLO)
            mostrar_barra_progreso()
            ejecutar_suite(greedyTests())
        elif (valor == 2):
            mostrar_mensaje("\n\t\tEjecutando pruebas Programacion Dinamica",COLOR_CIAN)
            mostrar_mensaje("Cargando...",COLOR_CIAN)
            mostrar_barra_progreso()
            ejecutar_suite(pdTests())
        elif (valor == 3):
            mostrar_mensaje("\n\t\tEjecutando pruebas Backtracking",COLOR_VERDE)
            mostrar_mensaje("Cargando...",COLOR_VERDE)
            mostrar_barra_progreso()
            mostrar_mensaje("No hay pruebas de backtracking (aun...)",COLOR_ROJO)
        elif (valor == 0):
            mostrar_mensaje("Saliendo del programa...",COLOR_MAGENTA)
        else:
            mostrar_mensaje("Error intente nuevamente",COLOR_ROJO)

if __name__ == "__main__":
    main()


