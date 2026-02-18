import time

def calcular_periodo(a, m, x0):
    """
    Calcula el periodo de un generador congruencial multiplicativo.
    Formula: X_n+1 = (a * X_n) mod m
    """
    current_x = x0
    periodo = 0
    
    # Iniciamos el ciclo
    while True:
        # Aplicamos la fórmula
        current_x = (a * current_x) % m
        periodo += 1
        
        # Si volvemos a la semilla inicial (x0), hemos encontrado el periodo
        if current_x == x0:
            return periodo
            
        # Protección contra bucles infinitos (opcional, por si acaso no cicla pronto)
        if periodo > m: 
             return -1 # Indica error o periodo mayor al módulo (raro en estos casos)

# Definición de los 5 casos de la actividad 2.2
# Formato: (a, m, x0)
casos = [
    {"id": 1, "a": 203, "m": 10**5, "x0": 17},
    {"id": 2, "a": 211, "m": 10**8, "x0": 19},
    {"id": 3, "a": 221, "m": 10**3, "x0": 3},
    {"id": 4, "a": 5,   "m": 64,    "x0": 7},
    {"id": 5, "a": 11,  "m": 128,   "x0": 9}
]

print(f"{'Caso':<5} | {'a':<5} | {'m':<10} | {'X0':<5} | {'Periodo Calculado'}")
print("-" * 55)

for caso in casos:
    start_time = time.time()
    p = calcular_periodo(caso["a"], caso["m"], caso["x0"])
    end_time = time.time()
    
    # Nota: El caso 2 (m=10^8) puede tardar unos segundos
    print(f"{caso['id']:<5} | {caso['a']:<5} | {caso['m']:<10} | {caso['x0']:<5} | {p}")