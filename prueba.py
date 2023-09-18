import numpy as np
from scipy.stats import multinomial

# Ejemplo de salidas (reemplaza con tus propios datos)
salidas = [
    [5, 18, 22, 36, 11, 4, 7, 14, 26, 33, 9, 20],
    [2, 13, 27, 35, 8, 16, 21, 34, 19, 25, 31, 6],
    [10, 23, 28, 15, 30, 3, 12, 17, 29, 1, 32, 24],
]

# Aplanar la lista de salidas para tener una lista de todos los números
todos_los_numeros = [numero for salida in salidas for numero in salida]

# Calcular frecuencia de cada número
frecuencia_numeros = np.bincount(todos_los_numeros, minlength=37)[1:]

# Ajustar un modelo de distribución multinomial
total_salidas = len(salidas)
probabilidades = frecuencia_numeros / total_salidas
multinomial_model = multinomial(n=total_salidas, p=probabilidades)

# Calcular las probabilidades predichas por el modelo
probabilidades_predichas = multinomial_model.pmf(frecuencia_numeros)

# Mostrar resultados
for numero, frecuencia, prob_predicha in zip(range(1, 37), frecuencia_numeros, probabilidades_predichas):
    print(f"Número {numero}: Frecuencia observada = {frecuencia}, Probabilidad predicha = {prob_predicha:.6f}")
