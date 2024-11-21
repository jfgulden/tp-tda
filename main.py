import unittest
from excercise_1.test import suite as greedyTests
from excercise_2.test_pd import suite as pdTests

def mostrar_menu():
    print("\n MENU DE OPCIONES")
    print("1:Ejecutar Pruebas Greedy")
    print("2:Ejecutar Pruebas Programacion Dinamica")
    print("3:Ejecutar Pruebas Backtracking")
    print("0:Salir")

def ejecutar_suite(suite):
    runner = unittest.TextTestRunner()
    runner.run(suite)

def main():

    valor = -1
    while(valor != 0):
        mostrar_menu()
        valor = int(input("seleccione una opcion:"))
        if (valor == 1):
            print("\n Ejecutando Pruebas Greedy")
            ejecutar_suite(greedyTests())
        elif (valor == 2):
            print("\n Ejecutando pruebas Programacion Dinamica")
            ejecutar_suite(pdTests())
        elif (valor == 3):
            print("\n Ejecutando pruebas Backtracking")
            print("\nno hay pruebas de backtracking(aun.....)")
        elif (valor == 0):
            print("\n Saliendo del programa....")
            break
        else:
            print("\n Error intente Nuevamente")

if __name__ == "__main__":
    main()


