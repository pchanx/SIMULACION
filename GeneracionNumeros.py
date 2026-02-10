import tkinter as tk
from tkinter import ttk, messagebox
import math

class GeneradorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador Congruencial Multiplicativo")
        self.root.geometry("600x500")

        # --- Variables de control ---
        self.var_x0 = tk.StringVar(value="17")
        self.var_a = tk.StringVar(value="3")
        self.var_m = tk.StringVar(value="100")
        self.var_n = tk.StringVar(value="20") # Cantidad de números a generar
        self.var_periodo_teorico = tk.StringVar(value="---")
        
        # --- Frame de Entrada de Datos ---
        input_frame = ttk.LabelFrame(root, text="Parámetros del Generador (Xn+1 = a*Xn mod m)")
        input_frame.pack(padx=10, pady=10, fill="x")

        # Grid para inputs
        ttk.Label(input_frame, text="Semilla (X0):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.var_x0).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Multiplicador (a):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.var_a).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Módulo (m):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.var_m).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Números a generar (N):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.var_n).grid(row=1, column=3, padx=5, pady=5)

        # Botones de Acción
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Calcular Tabla", command=self.calcular).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cargar Ejemplo Decimal (Tabla 2.4)", command=self.cargar_ejemplo_decimal).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cargar Ejemplo Binario (Tabla 2.5)", command=self.cargar_ejemplo_binario).pack(side="left", padx=5)

        # --- Información del Periodo ---
        info_frame = ttk.LabelFrame(root, text="Análisis del Periodo")
        info_frame.pack(padx=10, pady=5, fill="x")
        ttk.Label(info_frame, text="Periodo Teórico Estimado:").pack(side="left", padx=5)
        ttk.Label(info_frame, textvariable=self.var_periodo_teorico, font=("Arial", 10, "bold"), foreground="blue").pack(side="left", padx=5)

        # --- Tabla de Resultados ---
        table_frame = ttk.Frame(root)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")

        # Treeview (Tabla)
        columns = ("n", "Xn")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        self.tree.heading("n", text="n (Iteración)")
        self.tree.heading("Xn", text="Xn (Valor Generado)")
        self.tree.column("n", width=100, anchor="center")
        self.tree.column("Xn", width=200, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

    def cargar_ejemplo_decimal(self):
        # Datos de la Imagen 3 (Tabla 2.4)
        self.var_x0.set("17")
        self.var_a.set("3")
        self.var_m.set("100")
        self.var_n.set("25") # Un poco más del periodo (20) para ver repetición
        self.calcular()

    def cargar_ejemplo_binario(self):
        # Datos de la Imagen 4 (Tabla 2.5)
        self.var_x0.set("5")
        self.var_a.set("5")
        self.var_m.set("32")
        self.var_n.set("10") # Un poco más del periodo (8)
        self.calcular()

    def calcular_lambda(self, p, e):
        """Calcula lambda según reglas de la imagen 2 para factores p^e"""
        if p == 2:
            if e == 1: return 1
            if e == 2: return 2
            if e >= 3: return 2**(e-2)
        else:
            return (p**(e-1)) * (p - 1)
        return 1

    def estimar_periodo(self, m):
        """Intenta estimar el periodo máximo teórico basado en m"""
        # Detectar si es potencia de 10 (Sistema Decimal)
        # m = 10^d
        try:
            d_dec = math.log10(m)
            if abs(d_dec - round(d_dec)) < 1e-9: # Es potencia de 10 exacta
                d = int(round(d_dec))
                if d >= 5:
                    return f"{5 * (10**(d-2))} (Regla d>=5)"
                else:
                    # Regla MCM
                    l1 = self.calcular_lambda(2, d)
                    l2 = self.calcular_lambda(5, d)
                    return f"{math.lcm(l1, l2)} (MCM de partes)"
        except:
            pass

        # Detectar si es potencia de 2 (Sistema Binario)
        # m = 2^d
        try:
            d_bin = math.log2(m)
            if abs(d_bin - round(d_bin)) < 1e-9: # Es potencia de 2 exacta
                d = int(round(d_bin))
                if d >= 2:
                    return f"{2**(d-2)} (m/4)"
                else:
                    return "No aplica (d<2)"
        except:
            pass
            
        return "No determinado (m no es 10^d ni 2^d estándar)"

    def calcular(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            x0 = int(self.var_x0.get())
            a = int(self.var_a.get())
            m = int(self.var_m.get())
            n_iter = int(self.var_n.get())
            
            # 1. Calcular y mostrar Periodo Teórico
            periodo_texto = self.estimar_periodo(m)
            self.var_periodo_teorico.set(periodo_texto)

            # 2. Generar Secuencia
            xn = x0
            valores_vistos = {} # Para detectar ciclo real
            ciclo_encontrado = False
            
            for i in range(1, n_iter + 1):
                xn_prev = xn
                xn = (a * xn) % m
                
                # Insertar en tabla
                self.tree.insert("", "end", values=(i, xn))
                
                # Chequeo simple de ciclo (si vuelve a X0)
                if not ciclo_encontrado and xn == x0:
                    print(f"Ciclo detectado en n={i}") # Debug consola
                    
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos enteros válidos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneradorApp(root)
    root.mainloop()
    