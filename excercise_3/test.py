def get_better_order_to_iterate(demad: list):
    return [
        indice
        for valor, indice in sorted(
            (valor, indice) for indice, valor in enumerate(demad)
        )
    ]


lista = [10,1, 3, 2, 4, 5]
print(get_better_order_to_iterate(lista))
