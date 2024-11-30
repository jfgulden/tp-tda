# Trabajo Práctico: Juegos de Hermanos

![logofiuba](logofiuba.jpg)

## Integrantes

- Theo Miguel
- Brayan Ricaldi
- Juan Francisco Gulden
- Franco Altiera
- Daniela Gómez

## Introducción

Cada parte del trabajo práctico se encuentra en una carpeta diferente:

- **Parte 1**: carpeta `excercise_1`
- **Parte 2**: carpeta `excercise_2`
- **Parte 3**: carpeta `excercise_3`

Dentro de cada carpeta, se encuentra un archivo con el/los algoritmo/s implementado/s, y otro archivo con las pruebas realizadas.

## Instrucciones de uso

### Requisitos previos

Para correr las pruebas, es necesario tener instalado Python. Para instalarlo, se debe ejecutar el siguiente comando en la terminal:

```bash
sudo apt-get install python3
```

### Ejecución de tests

Cada carpeta contiene los tests realizados para la parte correspondiente.
Para ejecutar los tests, simplemente se debe correr el archivo tests.py en cada carpeta.
Se detallarán las instrucciones específicas para cada parte a continuación.

### Ejecución de los algoritmos

Para correr cada algoritmo, se debe ejecutar el archivo correspondiente a cada parte y pasarle como argumento el archivo de entrada. Dicho archivo debe tener un formato similar a los archivos de entrada provistos por la cátedra para cada ejercicio. También se hará una explicación más detallada en cada parte.

### Ejecución parte 1

Para correr las pruebas de la parte 1, se debe ejecutar el siguiente comando en la terminal:

```python
python3 excercise_1/tests.py
```

Este comando correrá los tests provistos por la cátedra y los tests adicionales que realizamos.

Para correr el algoritmo greedy, se debe ejecutar el siguiente comando en la terminal, al que se le debe pasar como argumento el archivo de entrada. Dicho archivo debe contener todas las monedas en el orden deseado separadas entre sí única y exclusivamente por un `;` en la primera línea del archivo:

```python
python3 excercise_1/greedy.py <archivo>
```

Este comando correrá el algoritmo greedy implementado.

### Ejecución parte 2

Para correr las pruebas de la parte 2, se debe ejecutar el siguiente comando en la terminal:

```python
python3 excercise_2/tests.py
```

Este comando correrá los tests provistos por la cátedra y los tests adicionales que realizamos.

De la misma manera, para correr el algoritmo implementado, se debe ejecutar el siguiente comando en la terminal, al que se le debe pasar como argumento el archivo de entrada. Dicho archivo debe contener todas las monedas en el orden deseado separadas entre sí única y exclusivamente por un `;` en la primera línea del archivo:

```python
python3 excercise_2/dp.py <archivo>
```

Este comando correrá el algoritmo implementado.

### Ejecución parte 3

#### Programación Dinámica

Para correr las pruebas de la parte 3, se debe ejecutar el siguiente comando en la terminal:

```python
python3 excercise_3/tests.py
```

Este comando correrá los tests provistos por la cátedra y los tests adicionales que realizamos.

Para correr el algoritmo implementado, se debe ejecutar el siguiente comando en la terminal, al que se le debe pasar como argumento el archivo de entrada.

```python
python3 excercise_3/backtracking.py <archivo>
```

Dicho archivo debe tener n filas con las demandas de las filas, seguido de un salto de línea, luego m filas con las demandas de las columnas, seguido de otro salto de línea, y luego k filas con el largo de los barcos, separadas por una línea en blanco. Como por ejemplo:

```txt
3
1
2

3
2
0

1
1
```

Donde demandas_filas = [3, 1, 2], demandas_columnas = [3, 2, 0], barcos = [1, 1].

#### Validador eficiente

Este validador se utilizó para demostrar que el problema de la batalla naval es NP. Para correrlo, se debe ejecutar el siguiente comando en la terminal, al que se le debe pasar como argumento el archivo de entrada, con el mismo formato que el archivo de Programación Dinámica.

```python
python3 excercise_3/validador.py <archivo>
```

#### Programación Lineal

Para correr el algoritmo de programación lineal, se debe ejecutar el siguiente comando en la terminal, al que se le debe pasar como argumento el archivo de entrada, con el mismo formato que el archivo de Programación Dinámica.

```python
python3 excercise_3/programacion_lineal.py <archivo>
```
