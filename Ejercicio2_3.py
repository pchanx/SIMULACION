import math

def obtener_factores_primos(n):
    """Devuelve un conjunto con los factores primos únicos de n"""
    factores = set()
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            factores.add(d)
            temp //= d
        d += 1
    if temp > 1:
        factores.add(temp)
    return factores

def encontrar_parametros_mixto(m):
    """
    Busca 'a' y 'c' que cumplan el Teorema de Hull-Dobell para periodo completo.
    Teorema:
    1. m y c son primos relativos (mcd(c,m) = 1).
    2. (a-1) es divisible por todos los factores primos de m.
    3. Si m es múltiplo de 4, (a-1) también debe serlo.
    """
    factores_m = obtener_factores_primos(m)
    es_m_multiplo_4 = (m % 4 == 0)

    # 1. Buscar un c válido (primo relativo con m)
    # Tomamos el primero que encontremos para el ejemplo (ej: 3, 7, etc)
    c_candidato = 0
    for c in range(1, m):
        if math.gcd(c, m) == 1:
            c_candidato = c
            break # Nos quedamos con el primero que sirva
            
    # 2. Buscar un a válido
    a_candidato = 0
    for a in range(2, 2 * m): # Buscamos un a razonable
        condicion_primos = all((a - 1) % p == 0 for p in factores_m)
        condicion_4 = True
        if es_m_multiplo_4:
            condicion_4 = ((a - 1) % 4 == 0)
        
        if condicion_primos and condicion_4:
            a_candidato = a
            break # Nos quedamos con el primero que sirva

    return a_candidato, c_candidato

def verificar_periodo(a, c, m, x0):
    visited = set()
    current = x0
    # Simulamos hasta que se repita
    while current not in visited:
        visited.add(current)
        current = (a * current + c) % m
    return len(visited)

# --- EJECUCIÓN DEL EJERCICIO 2.3 ---
# Definimos un Módulo m para el ejemplo (puedes cambiarlo a 1000, 64, etc.)
m_ejemplo = 100 
x0_ejemplo = 0 # En periodo completo, la semilla no importa, siempre recorre todo

# Calculamos los parámetros teóricos
a, c = encontrar_parametros_mixto(m_ejemplo)

print(f"--- Solución para Ejercicio 2.3 (Módulo m={m_ejemplo}) ---")
print(f"Parámetros calculados según Hull-Dobell:")
print(f"  a  = {a}")
print(f"  c  = {c}")
print(f"  m  = {m_ejemplo}")
print(f"  X0 = {x0_ejemplo}")
print("-" * 30)

# Verificamos si realmente da periodo completo
periodo_real = verificar_periodo(a, c, m_ejemplo, x0_ejemplo)
print(f"Periodo verificado: {periodo_real}")

if periodo_real == m_ejemplo:
    print("¡CORRECTO! Es periodo completo (igual a m).")
else:
    print("Error: No es periodo completo.")