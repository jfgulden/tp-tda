import unittest
import time
from greedy import batalla_naval, parsear_archivo

def resultado_test(resultado_obtenido,resultado_esperado):
    print(f"Demanda insatisfecha obtenida: {resultado_obtenido}")
    print(f"Demanda insatisfecha esperada: {resultado_esperado}")
    print(f"Diferencia: {resultado_esperado - resultado_obtenido}\n\n")

class GameTest:
    def __init__(self, file: str):
        self.file = file

    def run_naval_battle(self):
        barcos, demands_rows, demands_columns = parsear_archivo(f"excercise_3/archivos_pruebas/{self.file}")
        remaining_demand = batalla_naval(barcos, demands_rows[:], demands_columns[:])
        demand_fullfilled = (
            sum(demands_rows) + sum(demands_columns) - remaining_demand
        )
        return demand_fullfilled


class TestGreedy(unittest.TestCase):
    def run(self, resultado=None):
        tiempo_inicio = time.time()  
        super().run(resultado)  
        tiempo_final = time.time()  
        duracion = tiempo_final - tiempo_inicio  
        print(f"{self._testMethodName} - Tiempo de ejecución: {duracion:.6f} segundos")  
 
 
    def test_greedy_3_3_2(self):
        print("============== TEST 3_3_2.txt ==============")
        game = GameTest("3_3_2.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,4)

    def test_greedy_5_5_6(self):
        print("============== TEST 5_5_6.txt ==============")
        game = GameTest("5_5_6.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,12)
 
    def test_greedy_8_7_10(self):
        print("============== TEST 8_7_10.txt ==============")
        game = GameTest("8_7_10.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,26)

    def test_greedy_10_3_3(self):
        print("============== TEST 10_3_3.txt ==============")
        game = GameTest("10_3_3.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,6)


    def test_greedy_10_10_10(self):
        print("============== TEST 10_10_10.txt ==============")
        game = GameTest("10_10_10.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,40)

    def test_greedy_15_10_15(self):
        print("============== TEST 15_10_15.txt ==============")
        game = GameTest("15_10_15.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,40)
        
    def test_greedy_12_12_21(self):
        print("============== TEST 12_12_21.txt ==============")
        game = GameTest("12_12_21.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,46)


    def test_greedy_20_20_20(self):
        print("============== TEST 20_20_20.txt ==============")
        game = GameTest("20_20_20.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,104)

    def test_greedy_20_25_30(self):
        print("============== TEST 20_25_30.txt ==============")
        game = GameTest("20_25_30.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,172)

    def test_greedy_30_25_25(self):
        print("============== TEST 30_25_25.txt ==============")
        game = GameTest("30_25_25.txt")
        resultado = game.run_naval_battle()
        resultado_test(resultado,202)


def suite():

    suite = unittest.TestSuite()

    suite.addTest(TestGreedy('test_greedy_3_3_2'))
    suite.addTest(TestGreedy('test_greedy_5_5_6'))
    suite.addTest(TestGreedy('test_greedy_8_7_10'))
    suite.addTest(TestGreedy('test_greedy_10_3_3'))
    suite.addTest(TestGreedy('test_greedy_10_10_10'))
    suite.addTest(TestGreedy('test_greedy_15_10_15'))
    suite.addTest(TestGreedy('test_greedy_12_12_21'))
    suite.addTest(TestGreedy('test_greedy_20_20_20'))
    suite.addTest(TestGreedy('test_greedy_20_25_30'))
    suite.addTest(TestGreedy('test_greedy_30_25_25'))

    return suite  

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite()) 