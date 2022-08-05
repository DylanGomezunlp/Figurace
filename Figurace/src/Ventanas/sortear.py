import random
def sortear_dataset():
    """Elige al azar un dataset de la lista de datasets

    Returns:
        Str: Devuelve el string del dataset elegido
    """
    datasets = {1: 'Spotify', 2: 'Volcan', 3: 'Fifa'}
    x = random.randint(1,3)
    return datasets[x]


def opciones_rand(cantidad,opciones):
    """Elige al azar {cantidad} opciones de cada lista de opciones"""
    return random.choices(opciones, k=cantidad)
