import unittest
from excercise_2.pd import maxima_ganancia_sofia,obtener_monedas_de_archivo

def resultado_test(resultado_obtenido,resultado_esperado):
    if(resultado_obtenido == resultado_esperado):
        print("✔️  Sophia obtiene la maxima ganancia posible")
    else:
        print("❌  Sophia NO obtiene la maxima ganancia posible")
    print(f"Resultado esperado: {resultado_esperado}, Resultado obtenido: {resultado_obtenido}\n")

class TestCatedra(unittest.TestCase):

    def test_5_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 5 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/5.txt")
        resultado = maxima_ganancia_sofia(monedas)
        suma_total = sum(resultado)
        resultado_test(suma_total,1483)
        self.assertEqual(suma_total,1483)

    def test_10_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 10 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/10.txt")
        resultado = maxima_ganancia_sofia(monedas)
        suma_total = sum(resultado)
        resultado_test(suma_total,2338)
        self.assertEqual(suma_total,2338)

    def test_20_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 20 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/20.txt")
        resultado = maxima_ganancia_sofia(monedas)
        suma_total = sum(resultado)
        resultado_test(suma_total,5234)
        self.assertEqual(suma_total,5234)

    def test_25_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 25 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/25.txt")
        resultado = maxima_ganancia_sofia(monedas)
        suma_total = sum(resultado)
        resultado_test(suma_total,7491)
        self.assertEqual(suma_total,7491)

    def test_50_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 50 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/50.txt")
        resultado = maxima_ganancia_sofia(monedas)
        suma_total = sum(resultado)
        resultado_test(suma_total,14976)
        self.assertEqual(suma_total,14976)

    def test_100_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 100 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/100.txt")
        resultado = maxima_ganancia_sofia(monedas)
        suma_total = sum(resultado)
        resultado_test(suma_total,28844)
        self.assertEqual(suma_total,28844)

    def test_1000_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 1000 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/1000.txt")
        resultado = maxima_ganancia_sofia(monedas)
        suma_total = sum(resultado)
        resultado_test(suma_total,1401590)
        self.assertEqual(suma_total,1401590)

    def test_2000_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 2000 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/2000.txt")
        resultado = maxima_ganancia_sofia(monedas)
        suma_total = sum(resultado)
        resultado_test(suma_total,2869340)
        self.assertEqual(suma_total,2869340)

    def test_5000_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 5000 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/5000.txt")
        resultado = maxima_ganancia_sofia(monedas)
        suma_total = sum(resultado)
        resultado_test(suma_total,9939221)
        self.assertEqual(suma_total,9939221)

    def test_10000_monedas(self):
        print("--------SE PRUEBA UN ARREGLO DE 10000 MONEDAS--------")
        monedas = obtener_monedas_de_archivo("excercise_2/archivos_pruebas/10000.txt")
        resultado = maxima_ganancia_sofia(monedas)
        suma_total = sum(resultado)
        resultado_test(suma_total,34107537)
        self.assertEqual(suma_total,34107537)

def suite():

    suite = unittest.TestSuite()
    
    suite.addTest(TestCatedra('test_5_monedas'))
    suite.addTest(TestCatedra('test_10_monedas'))
    suite.addTest(TestCatedra('test_20_monedas'))
    suite.addTest(TestCatedra('test_25_monedas'))
    suite.addTest(TestCatedra('test_50_monedas'))
    suite.addTest(TestCatedra('test_100_monedas'))
    suite.addTest(TestCatedra('test_1000_monedas'))
    suite.addTest(TestCatedra('test_2000_monedas'))
    suite.addTest(TestCatedra('test_5000_monedas'))
    suite.addTest(TestCatedra('test_10000_monedas'))

    return suite

if __name__ == '__main__':

    runner = unittest.TextTestRunner()
    runner.run(suite())