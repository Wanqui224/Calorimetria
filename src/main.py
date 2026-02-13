import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
 
class CalorimetriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Calorimetría Completa")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Constantes de materiales
        self.CONSTANTES = {
            'Agua (H₂O)': {
                'c_solido': 2100,      # J/(kg·°C) - hielo
                'c_liquido': 4186,     # J/(kg·°C) - agua
                'c_gas': 2010,         # J/(kg·°C) - vapor
                'Lf': 334000,          # J/kg - fusión
                'Lv': 2260000,         # J/kg - vaporización
                'T_fusion': 0,         # °C
                'T_ebullicion': 100    # °C
            },
            'Aluminio': {
                'c_solido': 900,
                'c_liquido': 1100,
                'Lf': 398000,
                'T_fusion': 660
            },
            'Cobre': {
                'c_solido': 385,
                'c_liquido': 510,
                'Lf': 205000,
                'T_fusion': 1085
            },
            'Hierro': {
                'c_solido': 450,
                'c_liquido': 820,
                'Lf': 272000,
                'T_fusion': 1538
            }
        }
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.tab_calculadora = ttk.Frame(self.notebook)
        self.tab_formulas = ttk.Frame(self.notebook)
        self.tab_constantes = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_calculadora, text='Calculadora')
        self.notebook.add(self.tab_formulas, text='Fórmulas y Despejes')
        self.notebook.add(self.tab_constantes, text='Constantes')
        
        # Configurar cada pestaña
        self.configurar_tab_calculadora()
        self.configurar_tab_formulas()
        self.configurar_tab_constantes()
        
    def configurar_tab_calculadora(self):
        # Frame principal con dos columnas
        frame_principal = ttk.Frame(self.tab_calculadora)
        frame_principal.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame izquierdo - Entradas
        frame_izq = ttk.LabelFrame(frame_principal, text="📊 Datos de Entrada", padding=20)
        frame_izq.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        # Material
        ttk.Label(frame_izq, text="Material:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.material_var = tk.StringVar(value='Agua (H₂O)')
        self.combo_material = ttk.Combobox(frame_izq, textvariable=self.material_var, 
                                           values=list(self.CONSTANTES.keys()), 
                                           state='readonly', width=25)
        self.combo_material.grid(row=0, column=1, pady=5)
        self.combo_material.bind('<<ComboboxSelected>>', self.actualizar_constantes)
        
        # Masa
        ttk.Label(frame_izq, text="Masa (kg):", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.masa_var = tk.StringVar(value='1')
        ttk.Entry(frame_izq, textvariable=self.masa_var, width=27).grid(row=1, column=1, pady=5)
        
        # Temperatura Inicial
        ttk.Label(frame_izq, text="Temperatura Inicial (°C):", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=5)
        self.temp_inicial_var = tk.StringVar(value='-20')
        ttk.Entry(frame_izq, textvariable=self.temp_inicial_var, width=27).grid(row=2, column=1, pady=5)
        
        # Temperatura Final
        ttk.Label(frame_izq, text="Temperatura Final (°C):", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', pady=5)
        self.temp_final_var = tk.StringVar(value='120')
        ttk.Entry(frame_izq, textvariable=self.temp_final_var, width=27).grid(row=3, column=1, pady=5)
        
        # Botón Calcular
        ttk.Button(frame_izq, text="🔥 Calcular Calor Total", 
                  command=self.calcular).grid(row=4, column=0, columnspan=2, pady=20, sticky='ew')
        
        ttk.Button(frame_izq, text="📐 Despejar Variable", 
                  command=self.abrir_despeje).grid(row=5, column=0, columnspan=2, pady=5, sticky='ew')
        
        # Frame derecho - Constantes
        frame_der = ttk.LabelFrame(frame_principal, text="📈 Constantes del Material", padding=20)
        frame_der.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        
        self.text_constantes = tk.Text(frame_der, height=15, width=50, font=('Courier', 10))
        self.text_constantes.pack(fill='both', expand=True)
        self.actualizar_constantes()
        
        # Frame inferior - Resultados
        frame_resultados = ttk.LabelFrame(self.tab_calculadora, text="🎯 Resultados del Cálculo", padding=20)
        frame_resultados.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Texto de resultados
        self.text_resultados = tk.Text(frame_resultados, height=10, width=100, font=('Arial', 10))
        self.text_resultados.pack(fill='both', expand=True)
        
        # Frame para el gráfico
        self.frame_grafico = ttk.Frame(frame_resultados)
        self.frame_grafico.pack(fill='both', expand=True, pady=10)
        
        # Configurar pesos de columnas
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        
    def configurar_tab_formulas(self):
        # Crear un frame con scroll
        canvas = tk.Canvas(self.tab_formulas)
        scrollbar = ttk.Scrollbar(self.tab_formulas, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido de fórmulas
        formulas_text = """
📚 FÓRMULAS DE CALORIMETRÍA

1. CALOR SENSIBLE (cambio de temperatura sin cambio de fase)
   ══════════════════════════════════════════════════════════
   Q = m · c · ΔT
   Q = m · c · (T_final - T_inicial)
   
   DESPEJES:
   • m = Q / (c · ΔT)
   • c = Q / (m · ΔT)
   • ΔT = Q / (m · c)
   • T_final = T_inicial + Q/(m · c)
   • T_inicial = T_final - Q/(m · c)

2. CALOR LATENTE DE FUSIÓN (sólido ↔ líquido)
   ══════════════════════════════════════════════════════════
   Q_fusión = m · L_f
   
   DESPEJES:
   • m = Q_fusión / L_f
   • L_f = Q_fusión / m

3. CALOR LATENTE DE VAPORIZACIÓN (líquido ↔ gas)
   ══════════════════════════════════════════════════════════
   Q_vaporización = m · L_v
   
   DESPEJES:
   • m = Q_vaporización / L_v
   • L_v = Q_vaporización / m

4. CALOR TOTAL (proceso completo)
   ══════════════════════════════════════════════════════════
   Q_total = Σ Q_i
   Q_total = Q_calentar_sólido + Q_fusión + Q_calentar_líquido 
             + Q_vaporización + Q_calentar_gas

5. CONSERVACIÓN DE LA ENERGÍA (Calorimetría)
   ══════════════════════════════════════════════════════════
   Q_cedido + Q_absorbido = 0
   Σ Q_i = 0
   
   El calor cedido (negativo) es igual al calor absorbido (positivo)

═══════════════════════════════════════════════════════════════════

🔄 CONDICIONALES POR FASES (AGUA)

Si T < 0°C       → Fase: Hielo (usar c_hielo)
Si T = 0°C       → Fusión/Solidificación (usar L_f)
Si 0°C < T < 100°C → Fase: Agua líquida (usar c_agua)
Si T = 100°C     → Vaporización/Condensación (usar L_v)
Si T > 100°C     → Fase: Vapor (usar c_vapor)

═══════════════════════════════════════════════════════════════════

📋 ALGORITMO DE CÁLCULO

1. Determinar fase inicial y final
2. Si hay cambio de fase:
   a) Calentar/enfriar hasta temperatura de cambio
   b) Aplicar calor latente
   c) Calentar/enfriar en nueva fase
3. Si NO hay cambio de fase:
   a) Q = m · c · ΔT

═══════════════════════════════════════════════════════════════════
        """
        
        text_widget = tk.Text(scrollable_frame, wrap='word', font=('Courier', 11), 
                            bg='#fffef0', padx=20, pady=20)
        text_widget.insert('1.0', formulas_text)
        text_widget.config(state='disabled')
        text_widget.pack(fill='both', expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def configurar_tab_constantes(self):
        # Crear un frame con scroll
        canvas = tk.Canvas(self.tab_constantes)
        scrollbar = ttk.Scrollbar(self.tab_constantes, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido de constantes
        constantes_text = """
🔬 CONSTANTES DE MATERIALES

═══════════════════════════════════════════════════════════════════
AGUA (H₂O)
═══════════════════════════════════════════════════════════════════
Calor específico del hielo (c_hielo)    : 2100 J/(kg·°C)  | 0.5 cal/(g·°C)
Calor específico del agua (c_agua)      : 4186 J/(kg·°C)  | 1 cal/(g·°C)
Calor específico del vapor (c_vapor)    : 2010 J/(kg·°C)  | 0.48 cal/(g·°C)
Calor latente de fusión (L_f)           : 334000 J/kg     | 80 cal/g
Calor latente de vaporización (L_v)     : 2260000 J/kg    | 540 cal/g
Temperatura de fusión                   : 0 °C            | 273.15 K
Temperatura de ebullición               : 100 °C          | 373.15 K

═══════════════════════════════════════════════════════════════════
ALUMINIO
═══════════════════════════════════════════════════════════════════
Calor específico (c)                    : 900 J/(kg·°C)   | 0.215 cal/(g·°C)
Calor latente de fusión (L_f)           : 398000 J/kg     | 95 cal/g
Temperatura de fusión                   : 660 °C          | 933 K

═══════════════════════════════════════════════════════════════════
COBRE
═══════════════════════════════════════════════════════════════════
Calor específico (c)                    : 385 J/(kg·°C)   | 0.092 cal/(g·°C)
Calor latente de fusión (L_f)           : 205000 J/kg     | 49 cal/g
Temperatura de fusión                   : 1085 °C         | 1358 K

═══════════════════════════════════════════════════════════════════
HIERRO
═══════════════════════════════════════════════════════════════════
Calor específico (c)                    : 450 J/(kg·°C)   | 0.107 cal/(g·°C)
Calor latente de fusión (L_f)           : 272000 J/kg     | 65 cal/g
Temperatura de fusión                   : 1538 °C         | 1811 K

═══════════════════════════════════════════════════════════════════
        """
        
        text_widget = tk.Text(scrollable_frame, wrap='word', font=('Courier', 11), 
                            bg='#e8f5f0', padx=20, pady=20)
        text_widget.insert('1.0', constantes_text)
        text_widget.config(state='disabled')
        text_widget.pack(fill='both', expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def actualizar_constantes(self, event=None):
        material = self.material_var.get()
        const_mat = self.CONSTANTES[material]
        
        texto = f"{'='*50}\n"
        texto += f"{material}\n"
        texto += f"{'='*50}\n\n"
        
        if 'c_solido' in const_mat:
            texto += f"Calor específico (sólido)  : {const_mat['c_solido']} J/(kg·°C)\n"
        if 'c_liquido' in const_mat:
            texto += f"Calor específico (líquido) : {const_mat['c_liquido']} J/(kg·°C)\n"
        if 'c_gas' in const_mat:
            texto += f"Calor específico (gas)     : {const_mat['c_gas']} J/(kg·°C)\n"
        if 'Lf' in const_mat:
            texto += f"\nCalor latente de fusión    : {const_mat['Lf']} J/kg\n"
        if 'Lv' in const_mat:
            texto += f"Calor latente de vapor.    : {const_mat['Lv']} J/kg\n"
        if 'T_fusion' in const_mat:
            texto += f"\nTemperatura de fusión      : {const_mat['T_fusion']} °C\n"
        if 'T_ebullicion' in const_mat:
            texto += f"Temperatura de ebullición  : {const_mat['T_ebullicion']} °C\n"
        
        self.text_constantes.delete('1.0', tk.END)
        self.text_constantes.insert('1.0', texto)
        
    def calcular(self):
        try:
            material = self.material_var.get()
            masa = float(self.masa_var.get())
            Ti = float(self.temp_inicial_var.get())
            Tf = float(self.temp_final_var.get())
            
            const_mat = self.CONSTANTES[material]
            
            resultados = []
            temperaturas = [Ti]
            energias = [0]
            Q_total = 0
            
            # Para agua: manejo completo de fases
            if material == 'Agua (H₂O)':
                # Fase 1: Calentar hielo (si T < 0)
                if Ti < 0 and Tf > 0:
                    Q1 = masa * const_mat['c_solido'] * (0 - Ti)
                    resultados.append({
                        'fase': "Calentar Hielo",
                        'formula': f"Q = m · c_hielo · ΔT = {masa} kg · {const_mat['c_solido']} J/(kg·°C) · {(0-Ti):.2f} °C",
                        'valor': Q1,
                        'rango': f"{Ti}°C → 0°C"
                    })
                    Q_total += Q1
                    temperaturas.append(0)
                    energias.append(Q_total)
                elif Ti < 0 and Tf <= 0:
                    Q1 = masa * const_mat['c_solido'] * (Tf - Ti)
                    resultados.append({
                        'fase': "Calentar/Enfriar Hielo",
                        'formula': f"Q = m · c_hielo · ΔT = {masa} kg · {const_mat['c_solido']} J/(kg·°C) · {(Tf-Ti):.2f} °C",
                        'valor': Q1,
                        'rango': f"{Ti}°C → {Tf}°C"
                    })
                    Q_total += Q1
                    temperaturas.append(Tf)
                    energias.append(Q_total)
                
                # Fase 2: Fusión (0°C)
                if Ti <= 0 and Tf > 0:
                    Q2 = masa * const_mat['Lf']
                    resultados.append({
                        'fase': "Fusión del Hielo",
                        'formula': f"Q = m · L_f = {masa} kg · {const_mat['Lf']} J/kg",
                        'valor': Q2,
                        'rango': "0°C (cambio de fase)"
                    })
                    Q_total += Q2
                    temperaturas.append(0)
                    energias.append(Q_total)
                
                # Fase 3: Calentar agua líquida (0 < T < 100)
                if Ti < 100 and Tf > 0:
                    T_inicio = max(0, Ti)
                    T_fin = min(100, Tf)
                    if T_fin > T_inicio:
                        Q3 = masa * const_mat['c_liquido'] * (T_fin - T_inicio)
                        resultados.append({
                            'fase': "Calentar Agua Líquida",
                            'formula': f"Q = m · c_agua · ΔT = {masa} kg · {const_mat['c_liquido']} J/(kg·°C) · {(T_fin-T_inicio):.2f} °C",
                            'valor': Q3,
                            'rango': f"{T_inicio}°C → {T_fin}°C"
                        })
                        Q_total += Q3
                        temperaturas.append(T_fin)
                        energias.append(Q_total)
                
                # Fase 4: Vaporización (100°C)
                if Ti < 100 and Tf > 100:
                    Q4 = masa * const_mat['Lv']
                    resultados.append({
                        'fase': "Vaporización del Agua",
                        'formula': f"Q = m · L_v = {masa} kg · {const_mat['Lv']} J/kg",
                        'valor': Q4,
                        'rango': "100°C (cambio de fase)"
                    })
                    Q_total += Q4
                    temperaturas.append(100)
                    energias.append(Q_total)
                
                # Fase 5: Calentar vapor (T > 100)
                if Tf > 100:
                    T_inicio = max(100, Ti)
                    Q5 = masa * const_mat['c_gas'] * (Tf - T_inicio)
                    resultados.append({
                        'fase': "Calentar Vapor",
                        'formula': f"Q = m · c_vapor · ΔT = {masa} kg · {const_mat['c_gas']} J/(kg·°C) · {(Tf-T_inicio):.2f} °C",
                        'valor': Q5,
                        'rango': f"{T_inicio}°C → {Tf}°C"
                    })
                    Q_total += Q5
                    temperaturas.append(Tf)
                    energias.append(Q_total)
            else:
                # Para otros materiales
                T_fus = const_mat['T_fusion']
                
                # Calentar sólido hasta fusión
                if Ti < T_fus and Tf > Ti:
                    T_fin = min(T_fus, Tf)
                    Q1 = masa * const_mat['c_solido'] * (T_fin - Ti)
                    resultados.append({
                        'fase': "Calentar Sólido",
                        'formula': f"Q = m · c_sólido · ΔT = {masa} kg · {const_mat['c_solido']} J/(kg·°C) · {(T_fin-Ti):.2f} °C",
                        'valor': Q1,
                        'rango': f"{Ti}°C → {T_fin}°C"
                    })
                    Q_total += Q1
                    temperaturas.append(T_fin)
                    energias.append(Q_total)
                
                # Fusión
                if Ti <= T_fus and Tf > T_fus:
                    Q2 = masa * const_mat['Lf']
                    resultados.append({
                        'fase': "Fusión",
                        'formula': f"Q = m · L_f = {masa} kg · {const_mat['Lf']} J/kg",
                        'valor': Q2,
                        'rango': f"{T_fus}°C (cambio de fase)"
                    })
                    Q_total += Q2
                    temperaturas.append(T_fus)
                    energias.append(Q_total)
                
                # Calentar líquido
                if Tf > T_fus:
                    T_inicio = max(T_fus, Ti)
                    Q3 = masa * const_mat['c_liquido'] * (Tf - T_inicio)
                    resultados.append({
                        'fase': "Calentar Líquido",
                        'formula': f"Q = m · c_líquido · ΔT = {masa} kg · {const_mat['c_liquido']} J/(kg·°C) · {(Tf-T_inicio):.2f} °C",
                        'valor': Q3,
                        'rango': f"{T_inicio}°C → {Tf}°C"
                    })
                    Q_total += Q3
                    temperaturas.append(Tf)
                    energias.append(Q_total)
            
            # Mostrar resultados
            texto = "═" * 80 + "\n"
            texto += "RESULTADOS DEL CÁLCULO\n"
            texto += "═" * 80 + "\n\n"
            
            for i, r in enumerate(resultados, 1):
                texto += f"Etapa {i}: {r['fase']}\n"
                texto += f"Rango: {r['rango']}\n"
                texto += f"Fórmula: {r['formula']}\n"
                texto += f"Q{i} = {r['valor']:.2f} J = {r['valor']/1000:.2f} kJ\n"
                texto += "-" * 80 + "\n\n"
            
            texto += "═" * 80 + "\n"
            texto += "CALOR TOTAL:\n"
            texto += f"Q_total = {' + '.join([f'Q{i+1}' for i in range(len(resultados))])}\n"
            texto += f"Q_total = {Q_total:.2f} J\n"
            texto += f"Q_total = {Q_total/1000:.2f} kJ\n"
            texto += f"Q_total = {Q_total/1000000:.2f} MJ\n"
            texto += "═" * 80 + "\n"
            
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', texto)
            
            # Graficar
            self.graficar_diagrama(temperaturas, energias, resultados)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Por favor ingresa valores numéricos válidos.\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
    
    def graficar_diagrama(self, temps, energias, resultados):
        # Limpiar frame anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
        
        # Crear figura
        fig = Figure(figsize=(12, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Convertir energías a kJ
        energias_kJ = [e/1000 for e in energias]
        
        # Graficar
        ax.plot(energias_kJ, temps, 'o-', color='#667eea', linewidth=2, markersize=8, markerfacecolor='#764ba2')
        ax.set_xlabel('Energía Total (kJ)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Temperatura (°C)', fontsize=12, fontweight='bold')
        ax.set_title('Diagrama Temperatura vs Energía', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#f8f9fa')
        
        # Agregar anotaciones en puntos clave
        for i, (e, t) in enumerate(zip(energias_kJ, temps)):
            if i > 0:  # No anotar el punto inicial
                ax.annotate(f'{t}°C', xy=(e, t), xytext=(5, 5), 
                           textcoords='offset points', fontsize=9)
        
        fig.tight_layout()
        
        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def abrir_despeje(self):
        # Ventana para despejar variables
        ventana = tk.Toplevel(self.root)
        ventana.title("📐 Despejar Variable")
        ventana.geometry("600x500")
        ventana.configure(bg='#f0f0f0')
        
        frame_principal = ttk.Frame(ventana, padding=20)
        frame_principal.pack(fill='both', expand=True)
        
        ttk.Label(frame_principal, text="Calculadora de Variables", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(frame_principal, text="Selecciona la variable a calcular:", 
                 font=('Arial', 10)).pack(pady=5)
        
        var_calcular = tk.StringVar()
        combo = ttk.Combobox(frame_principal, textvariable=var_calcular, 
                            values=['Masa (m)', 'Calor específico (c)', 
                                   'Temperatura final (Tf)', 'Temperatura inicial (Ti)'],
                            state='readonly', width=30)
        combo.pack(pady=10)
        
        frame_inputs = ttk.LabelFrame(frame_principal, text="Datos", padding=20)
        frame_inputs.pack(fill='both', expand=True, pady=10)
        
        # Variables de entrada
        Q_var = tk.StringVar()
        m_var = tk.StringVar()
        c_var = tk.StringVar()
        Ti_var = tk.StringVar()
        Tf_var = tk.StringVar()
        deltaT_var = tk.StringVar()
        
        def actualizar_campos(*args):
            # Limpiar frame
            for widget in frame_inputs.winfo_children():
                widget.destroy()
            
            variable = var_calcular.get()
            
            if variable == 'Masa (m)':
                ttk.Label(frame_inputs, text="Calor (Q) en Joules:").grid(row=0, column=0, sticky='w', pady=5)
                ttk.Entry(frame_inputs, textvariable=Q_var, width=25).grid(row=0, column=1, pady=5)
                
                ttk.Label(frame_inputs, text="Calor específico (c) en J/(kg·°C):").grid(row=1, column=0, sticky='w', pady=5)
                ttk.Entry(frame_inputs, textvariable=c_var, width=25).grid(row=1, column=1, pady=5)
                
                ttk.Label(frame_inputs, text="Cambio de temperatura (ΔT) en °C:").grid(row=2, column=0, sticky='w', pady=5)
                ttk.Entry(frame_inputs, textvariable=deltaT_var, width=25).grid(row=2, column=1, pady=5)
                
            elif variable == 'Calor específico (c)':
                ttk.Label(frame_inputs, text="Calor (Q) en Joules:").grid(row=0, column=0, sticky='w', pady=5)
                ttk.Entry(frame_inputs, textvariable=Q_var, width=25).grid(row=0, column=1, pady=5)
                
                ttk.Label(frame_inputs, text="Masa (m) en kg:").grid(row=1, column=0, sticky='w', pady=5)
                ttk.Entry(frame_inputs, textvariable=m_var, width=25).grid(row=1, column=1, pady=5)
                
                ttk.Label(frame_inputs, text="Cambio de temperatura (ΔT) en °C:").grid(row=2, column=0, sticky='w', pady=5)
                ttk.Entry(frame_inputs, textvariable=deltaT_var, width=25).grid(row=2, column=1, pady=5)
        
        combo.bind('<<ComboboxSelected>>', actualizar_campos)
        
        # Frame para resultados
        frame_resultado = ttk.LabelFrame(frame_principal, text="Resultado", padding=20)
        frame_resultado.pack(fill='both', expand=True, pady=10)
        
        text_resultado = tk.Text(frame_resultado, height=5, font=('Arial', 11))
        text_resultado.pack(fill='both', expand=True)
        
        def calcular_variable():
            try:
                variable = var_calcular.get()
                resultado = ""
                
                if variable == 'Masa (m)':
                    Q = float(Q_var.get())
                    c = float(c_var.get())
                    deltaT = float(deltaT_var.get())
                    m = Q / (c * deltaT)
                    
                    resultado = f"Cálculo de la Masa:\n"
                    resultado += f"Fórmula: m = Q / (c · ΔT)\n"
                    resultado += f"m = {Q} J / ({c} J/(kg·°C) · {deltaT} °C)\n"
                    resultado += f"\nm = {m:.4f} kg"
                    
                elif variable == 'Calor específico (c)':
                    Q = float(Q_var.get())
                    m = float(m_var.get())
                    deltaT = float(deltaT_var.get())
                    c = Q / (m * deltaT)
                    
                    resultado = f"Cálculo del Calor Específico:\n"
                    resultado += f"Fórmula: c = Q / (m · ΔT)\n"
                    resultado += f"c = {Q} J / ({m} kg · {deltaT} °C)\n"
                    resultado += f"\nc = {c:.2f} J/(kg·°C)"
                
                text_resultado.delete('1.0', tk.END)
                text_resultado.insert('1.0', resultado)
                
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")
            except ZeroDivisionError:
                messagebox.showerror("Error", "El denominador no puede ser cero.")
        
        ttk.Button(frame_principal, text="Calcular", 
                  command=calcular_variable).pack(pady=10)

def main():
    root = tk.Tk()
    app = CalorimetriaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()