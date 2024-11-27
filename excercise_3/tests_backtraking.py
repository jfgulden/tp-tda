import unittest
from backtraking import naval_battle


class GameTest:
    def __init__(self, file: str):
        self.file = file

    def run_naval_battle(self):
        barcos, demands_rows, demands_columns = self.parsear_archivo()
        result = naval_battle(barcos, demands_rows, demands_columns)
        demand_fullfilled = (
            sum(demands_rows) + sum(demands_columns) - result.remaining_demand
        )
        return demand_fullfilled

    def parsear_archivo(self) -> tuple[list[int], list[int], list[int]]:
        path: str = f"./archivos_pruebas/TP3/{self.file}"
        with open(path, "r") as file:
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

        return barcos, demandas_filas, demandas_columnas


class TestBacktraking(unittest.TestCase):
    def test_backtraking_3_3_2(self):
        game = GameTest("3_3_2.txt")
        self.assertEqual(game.run_naval_battle(), 4)

    def test_backtraking_5_5_6(self):
        game = GameTest("5_5_6.txt")
        self.assertTrue(game.run_naval_battle(), 12)

    def test_backtraking_8_7_10(self):
        game = GameTest("8_7_10.txt")
        self.assertTrue(game.run_naval_battle(), 26)

    def test_backtraking_10_3_3(self):
        game = GameTest("10_3_3.txt")
        self.assertTrue(game.run_naval_battle(), 6)

    def test_backtraking_10_10_10(self):
        game = GameTest("10_10_10.txt")
        self.assertTrue(game.run_naval_battle(), 40)

    def test_backtraking_15_10_15(self):
        game = GameTest("15_10_15.txt")
        self.assertTrue(game.run_naval_battle(), 40)

    def test_backtraking_12_12_21(self):
        game = GameTest("12_12_21.txt")
        self.assertTrue(game.run_naval_battle(), 46)

    def test_backtraking_20_20_20(self):
        game = GameTest("20_20_20.txt")
        self.assertTrue(game.run_naval_battle(), 104)

    def test_backtraking_20_25_30(self):
        game = GameTest("20_25_30.txt")
        self.assertTrue(game.run_naval_battle(), 172)

    def test_backtraking_30_25_25(self):
        game = GameTest("30_25_25.txt")
        self.assertTrue(game.run_naval_battle(), 202)


if __name__ == '__main__':
    unittest.main()

# Run: python3 tests_backtraking.py
