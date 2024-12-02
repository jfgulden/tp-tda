import unittest
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from excercise_3.backtracking import naval_battle, parsear_archivo

def resultado_test(resultado_obtenido,resultado_esperado):
    if(resultado_obtenido == resultado_esperado):
        print("✔️  Se cumple la demanda")
    else:
        print("❌  NO se cumple la demanda")
    print(f"Resultado esperado: {resultado_esperado}, Resultado obtenido: {resultado_obtenido}\n")

class GameTest:
    def __init__(self, file: str):
        self.file = file

    def run_naval_battle(self):
        barcos, demands_rows, demands_columns = parsear_archivo(f"excercise_3/archivos_pruebas/{self.file}")
        result = naval_battle(barcos, demands_rows, demands_columns)
        demand_fullfilled = (
            sum(demands_rows) + sum(demands_columns) - result.remaining_demand
        )
        return demand_fullfilled

class TestBacktraking(unittest.TestCase):

    def run(self, resultado=None):
        tiempo_inicio = time.time()  
        super().run(resultado)  
        tiempo_final = time.time()  
        duracion = tiempo_final - tiempo_inicio  
        print(f"{self._testMethodName} - Tiempo de ejecución: {duracion:.6f} segundos")  
        print()

    def test_backtraking_3_3_2(self):
        print("--------SE PRUEBA ARCHIVO 3_3_2.txt--------")
        game = GameTest("3_3_2.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,4)
        self.assertEqual(resultado, 4)
        
    def test_backtraking_5_5_6(self):
        print("--------SE PRUEBA ARCHIVO 5_5_6.txt--------")
        game = GameTest("5_5_6.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,12)
        self.assertEqual(resultado, 12)

    def test_backtraking_8_7_10(self):
        print("--------SE PRUEBA ARCHIVO 8_7_10.txt--------")
        game = GameTest("8_7_10.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,26)
        self.assertEqual(resultado, 26)

    def test_backtraking_10_3_3(self):
        print("--------SE PRUEBA ARCHIVO 10_3_3.txt--------")
        game = GameTest("10_3_3.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,6)
        self.assertEqual(resultado, 6)

    def test_backtraking_10_10_10(self):
        print("--------SE PRUEBA ARCHIVO 10_10_10.txt--------")
        game = GameTest("10_10_10.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,40)
        self.assertEqual(resultado, 40)

    def test_backtraking_15_10_15(self):
        print("--------SE PRUEBA ARCHIVO 15_10_15.txt--------")
        game = GameTest("15_10_15.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,40)
        self.assertEqual(resultado, 40)

    def test_backtraking_12_12_21(self):
        print("--------SE PRUEBA ARCHIVO 12_12_21.txt--------")
        game = GameTest("12_12_21.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,46)
        self.assertEqual(resultado, 46)

    def test_backtraking_20_20_20(self):
        print("--------SE PRUEBA ARCHIVO 20_20_20.txt--------")
        game = GameTest("20_20_20.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,104)
        self.assertEqual(resultado, 104)

    def test_backtraking_20_25_30(self):
        print("--------SE PRUEBA ARCHIVO 20_25_30.txt--------")
        game = GameTest("20_25_30.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,172)
        self.assertEqual(resultado, 172)

    def test_backtraking_30_25_25(self):
        print("--------SE PRUEBA ARCHIVO 30_25_25.txt--------")
        game = GameTest("30_25_25.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,202)
        self.assertEqual(resultado, 202)


def suite():

    suite = unittest.TestSuite()

    suite.addTest(TestBacktraking('test_backtraking_3_3_2'))
    suite.addTest(TestBacktraking('test_backtraking_5_5_6'))
    suite.addTest(TestBacktraking('test_backtraking_8_7_10'))
    suite.addTest(TestBacktraking('test_backtraking_10_3_3'))
    suite.addTest(TestBacktraking('test_backtraking_10_10_10'))
    suite.addTest(TestBacktraking('test_backtraking_15_10_15'))
    suite.addTest(TestBacktraking('test_backtraking_12_12_21'))
    suite.addTest(TestBacktraking('test_backtraking_20_20_20'))
    suite.addTest(TestBacktraking('test_backtraking_20_25_30'))
    suite.addTest(TestBacktraking('test_backtraking_30_25_25'))

    return suite  

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite()) 