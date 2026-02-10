import tkinter as tk
from tkinter import ttk, messagebox
import math

class GeneradorMixtoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador Congruencial Mixto - Solucionador")
        self.root.geometry("700x600")

        # --- Variables de control ---
        self.var_x0 = tk.StringVar()
        self.var_a = tk.StringVar()
        self.var_c = tk.StringVar()
        self.var_m = tk.StringVar()
        self.var_n = tk.StringVar(value="20") # Cantidad de iteraciones por defecto
        self.var_resultado_periodo = tk.StringVar(value="---")
        
        # --- 1. Frame de Entrada de Datos ---
        input_frame = ttk.LabelFrame(root, text="Parámetros: Xn+1 = (a * Xn + c) mod m")
        input_frame.pack(padx=10, pady=5, fill="x")

        # Grid para inputs
        # Fila 0
        ttk.Label(input_frame, text="Semilla (X0):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.var_x0, width=15).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Multiplicador (a):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.var_a, width=15).grid(row=0, column=3, padx=5, pady=5)

        # Fila 1
        ttk.Label(input_frame, text="Constante (c):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.var_c, width=15).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Módulo (m):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.var_m, width=15).grid(row=1, column=3, padx=5, pady=5)
        
        # Fila 2
        ttk.Label(input_frame, text="Iteraciones (N):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.var_n, width=15).grid(row=2, column=1, padx=5, pady=5)

        # Botón Principal
        ttk.Button(input_frame, text="CALCULAR TABLA", command=self.calcular).grid(row=2, column=2, columnspan=2, pady=5, sticky="ew", padx=5)

        # --- 2. Frame de Casos Rápidos (Ejercicios de la imagen) ---
        cases_frame = ttk.LabelFrame(root, text="Cargar Ejercicios de la Imagen 2.1")
        cases_frame.pack(padx=10, pady=5, fill="x")

        # Botones para cada caso
        ttk.Button(cases_frame, text="Caso 1\n(8X+16 mod 100)", command=lambda: self.cargar_caso(15, 8, 16, 100)).pack(side="left", fill="x", expand=True, padx=2, pady=5)
        ttk.Button(cases_frame, text="Caso 2\n(50X+17 mod 64)", command=lambda: self.cargar_caso(13, 50, 17, 64)).pack(side="left", fill="x", expand=True, padx=2, pady=5)
        ttk.Button(cases_frame, text="Caso 3\n(5X+24 mod 32)", command=lambda: self.cargar_caso(7, 5, 24, 32)).pack(side="left", fill="x", expand=True, padx=2, pady=5)
        ttk.Button(cases_frame, text="Caso 4\n(5X+21 mod 100)", command=lambda: self.cargar_caso(3, 5, 21, 100)).pack(side="left", fill="x", expand=True, padx=2, pady=5)
        ttk.Button(cases_frame, text="Caso 5\n(9X+13 mod 32)", command=lambda: self.cargar_caso(8, 9, 13, 32)).pack(side="left", fill="x", expand=True, padx=2, pady=5)

        # --- 3. Información del Periodo ---
        info_frame = ttk.LabelFrame(root, text="Análisis del Periodo")
        info_frame.pack(padx=10, pady=5, fill="x")
        ttk.Label(info_frame, text="Resultado:").pack(side="left", padx=5)
        ttk.Label(info_frame, textvariable=self.var_resultado_periodo, font=("Arial", 10, "bold"), foreground="blue").pack(side="left", padx=5)

        # --- 4. Tabla de Resultados ---
        table_frame = ttk.Frame(root)
        table_frame.pack(padx=10, pady=5, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")

        columns = ("n", "Xn", "Repetido")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        
        self.tree.heading("n", text="n (Iteración)")
        self.tree.heading("Xn", text="Xn (Valor)")
        self.tree.heading("Repetido", text="¿Ciclo?")
        
        self.tree.column("n", width=80, anchor="center")
        self.tree.column("Xn", width=150, anchor="center")
        self.tree.column("Repetido", width=100, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        # Cargar el primer caso por defecto al iniciar
        self.cargar_caso(15, 8, 16, 100)

    def cargar_caso(self, x0, a, c, m):
        """Carga los valores en los campos de texto"""
        self.var_x0.set(str(x0))
        self.var_a.set(str(a))
        self.var_c.set(str(c))
        self.var_m.set(str(m))
        self.var_n.set("25") # Reiniciar N a un valor razonable
        self.var_resultado_periodo.set("Pulsa Calcular...")
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

    def calcular(self):
        # Limpiar tabla anterior
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            # Obtener datos
            x0 = int(self.var_x0.get())
            a = int(self.var_a.get())
            c = int(self.var_c.get())
            m = int(self.var_m.get())
            n_iter = int(self.var_n.get())
            
            xn = x0
            # Diccionario para guardar en qué 'n' apareció cada valor: {valor: n}
            historial = {x0: 0} 
            periodo = None
            
            # Insertar X0 (semilla) como fila 0 (opcional, pero ayuda a ver el inicio)
            # self.tree.insert("", "end", values=(0, x0, "Semilla"))

            for i in range(1, n_iter + 1):
                # Fórmula Congruencial Mixta
                xn = (a * xn + c) % m
                
                nota = ""
                
                # DETECCIÓN DE PERIODO
                if periodo is None:
                    if xn in historial:
                        # ¡Encontramos un valor repetido!
                        n_anterior = historial[xn]
                        periodo = i - n_anterior
                        nota = f"Repite n={n_anterior}"
                        self.var_resultado_periodo.set(f"¡Ciclo encontrado! Periodo = {periodo} (Se repite cada {periodo} números)")
                    else:
                        historial[xn] = i
                
                # Insertar en la tabla visual
                if nota:
                    self.tree.insert("", "end", values=(i, xn, nota), tags=('ciclo',))
                else:
                    self.tree.insert("", "end", values=(i, xn, ""))
            
            if periodo is None:
                self.var_resultado_periodo.set(f"No se completó un ciclo en {n_iter} iteraciones.")
                
            # Colorear la fila donde se detecta el ciclo
            self.tree.tag_configure('ciclo', background='#ffcccc')

        except ValueError:
            messagebox.showerror("Error", "Asegúrate de que todos los campos sean números enteros.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneradorMixtoApp(root)
    root.mainloop()

    #ffoimbfdnbjfndboif