import random

# Generamos 5000 números aleatorios entre 0 y 20
random_numbers = [random.randint(1, 20) for _ in range(5000)]

# Guardamos los números en un archivo con saltos de línea
with open('random_numbers.txt', 'w') as file:
    for number in random_numbers:
        file.write(f"{number}\n")
