def obtener_periodo_multiplicativo(a, m, x0):
    visited = set()
    current = x0
    while current not in visited:
        visited.add(current)
        current = (a * current) % m
        if current == 0: # Si llegamos a 0, se rompe el ciclo
            break
    return len(visited)

def encontrar_generador_multiplicativo_optimo(limite_busqueda):
    """
    Busca parámetros para un generador multiplicativo con periodo m-1.
    """
    # 1. Buscamos un número primo para m
    def es_primo(n):
        if n < 2: return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0: return False
        return True

    # Probamos con un primo cercano al límite (ej. cerca de 100)
    m_candidato = 0
    for n in range(limite_busqueda, 2, -1):
        if es_primo(n):
            m_candidato = n
            break
            
    # 2. Buscamos 'a' que sea raíz primitiva (que genere periodo m-1)
    a_optimo = 0
    x0 = 1 # La semilla debe ser > 0
    
    print(f"Buscando raíz primitiva para el primo m={m_candidato}...")
    
    for a in range(2, m_candidato):
        periodo = obtener_periodo_multiplicativo(a, m_candidato, x0)
        if periodo == m_candidato - 1:
            a_optimo = a
            break
            
    return a_optimo, m_candidato, x0

# --- EJECUCIÓN ---
# Buscamos un ejemplo con un módulo cercano a 100 (puedes cambiarlo)
a, m, x0 = encontrar_generador_multiplicativo_optimo(100)

print("-" * 40)
print(f"Solución para Ejercicio 2.4 (Max Periodo):")
print(f"  m (Primo) = {m}")
print(f"  a (Raíz)  = {a}")
print(f"  X0        = {x0}")
print("-" * 40)

# Verificación
p = obtener_periodo_multiplicativo(a, m, x0)
print(f"Periodo verificado: {p}")
if p == m - 1:
    print(f"¡CORRECTO! El periodo es m-1 ({m}-1 = {p}).")
else:
    print("No se logró el periodo máximo.")