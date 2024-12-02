import unittest
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from excercise_1.greedy import obtener_ganador,obtener_monedas_de_archivo

def resultado_test(resultado_obtenido,resultado_esperado):
    if(resultado_obtenido == resultado_esperado):
        print("✔️  Sophia obtiene la maxima ganancia")
    else:
        print("❌  Sophia NO obtiene la maxima ganancia")
    print(f"Resultado esperado: {resultado_esperado}, Resultado obtenido: {resultado_obtenido}\n")

class TestAlumnos(unittest.TestCase):

    def run(self, resultado=None):
        tiempo_inicio = time.time()  
        super().run(resultado)  
        tiempo_final = time.time()  
        duracion = tiempo_final - tiempo_inicio  
        print(f"{self._testMethodName} - Tiempo de ejecución: {duracion:.6f} segundos")  
        print()

    def test_arreglo_ordenado_ascendentemente(self):
        print("--------SE PRUEBA UN ARREGLO ORDENADO ASCENDENTEMENTE--------")
        monedas = obtener_monedas_de_archivo("excercise_1/pruebas_alumnos/arregloOrdenadoAscendente.txt")
        resultado = obtener_ganador(monedas)
        resultado_test(resultado,22)
        self.assertEqual(resultado,22)
        
    def test_arreglo_ordenado_descendentemente(self):
        print("--------SE PRUEBA UN ARREGLO ORDENADO DESCENDENTEMENTE--------")
        monedas = obtener_monedas_de_archivo("excercise_1/pruebas_alumnos/arregloOrdenadoDescendente.txt")
        resultado = obtener_ganador(monedas)
        resultado_test(resultado,34)
        self.assertEqual(resultado,34)

    def test_valores_iguales_excepto_uno(self):
        print("--------SE PRUEBA UN ARREGLO CON VALORES IGUALES EXCEPTO UNO--------")
        monedas = obtener_monedas_de_archivo("excercise_1/pruebas_alumnos/arregloValoresIgualesExceptoUno.txt")
        resultado = obtener_ganador(monedas)
        resultado_test(resultado,12)
        self.assertEqual(resultado,12)
    
    def test_arreglo_con_valores_maximos_en_los_extremos(self):
        print("--------SE PRUEBA UN ARREGLO CON VALORES MAXIMOS EN LOS EXTREMOS--------")
        monedas = obtener_monedas_de_archivo("excercise_1/pruebas_alumnos/arregloValoresMaximosEnExtremos.txt")
        resultado = obtener_ganador(monedas)
        resultado_test(resultado,34)
        self.assertEqual(resultado,34)    
    
class TestCatedra(unittest.TestCase):
    def run(self, resultado=None):
        tiempo_inicio = time.time()  
        super().run(resultado)  
        tiempo_final = time.time()  
        duracion = tiempo_final - tiempo_inicio  
        print(f"{self._testMethodName} - Tiempo de ejecución: {duracion:.6f} segundos")  
        print()
           
    def test_20_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 20 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/20.txt")
        resultado = obtener_ganador(monedas)
        resultado_test(resultado,7165)
        self.assertEqual(resultado,7165)

    def test_25_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 25 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/25.txt")
        resultado = obtener_ganador(monedas)
        resultado_test(resultado,9635)
        self.assertEqual(resultado,9635) 

    def test_50_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 50 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/50.txt")
        resultado = obtener_ganador(monedas)
        resultado_test(resultado,17750)
        self.assertEqual(resultado,17750)

    def test_100_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 100 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/100.txt")
        resultado = obtener_ganador(monedas)
        resultado_test(resultado,35009)
        self.assertEqual(resultado,35009)

    def test_1000_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 1000 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/1000.txt")
        resultado = obtener_ganador(monedas)
        resultado_test(resultado,357814)
        self.assertEqual(resultado,357814) 

    def test_10000_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 10000 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/10000.txt")
        resultado = obtener_ganador(monedas)
        resultado_test(resultado,3550307)
        self.assertEqual(resultado,3550307)  

    def test_20000_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 20000 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_1/archivos_pruebas/20000.txt")
        resultado = obtener_ganador(monedas)
        resultado_test(resultado,7139357)
        self.assertEqual(resultado,7139357)   
     

def suite():
    suite = unittest.TestSuite()

    suite.addTest(TestAlumnos('test_arreglo_ordenado_ascendentemente'))
    suite.addTest(TestAlumnos('test_arreglo_ordenado_descendentemente'))
    suite.addTest(TestAlumnos('test_valores_iguales_excepto_uno'))
    suite.addTest(TestAlumnos('test_arreglo_con_valores_maximos_en_los_extremos'))
    
    suite.addTest(TestCatedra('test_20_monedas'))
    suite.addTest(TestCatedra('test_25_monedas'))
    suite.addTest(TestCatedra('test_50_monedas'))
    suite.addTest(TestCatedra('test_100_monedas'))
    suite.addTest(TestCatedra('test_1000_monedas'))
    suite.addTest(TestCatedra('test_10000_monedas'))
    suite.addTest(TestCatedra('test_20000_monedas'))

    return suite

if __name__ == '__main__':

    runner = unittest.TextTestRunner()
    runner.run(suite())