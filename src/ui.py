"""
Módulo para las pestañas de la interfaz gráfica.
"""

import tkinter as tk
from tkinter import ttk
from constants import FORMULAS_TEXT, CONSTANTES_TEXT


class TabConfigurator:
    """Configurador de pestañas para la aplicación de calorimetría."""
    
    def __init__(self, notebook, constantes_materiales):
        self.notebook = notebook
        self.constantes_materiales = constantes_materiales
    
    def configurar_tab_calculadora(self, tab_calculadora, callbacks):
        """
        Configura la pestaña de calculadora.
        
        Args:
            tab_calculadora: Widget de la pestaña
            callbacks: dict con funciones de callback {'calcular': func, 'actualizar': func}
        """
        # Frame principal con dos columnas
        frame_principal = ttk.Frame(tab_calculadora)
        frame_principal.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame izquierdo - Entradas
        frame_izq = ttk.LabelFrame(frame_principal, text="📊 Datos de Entrada", padding=20)
        frame_izq.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        # Material
        ttk.Label(frame_izq, text="Material:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        material_var = tk.StringVar(value='Agua (H₂O)')
        combo_material = ttk.Combobox(frame_izq, textvariable=material_var, 
                                       values=list(self.constantes_materiales.keys()), 
                                       state='readonly', width=25)
        combo_material.grid(row=0, column=1, pady=5)
        combo_material.bind('<<ComboboxSelected>>', callbacks['actualizar'])
        
        # Masa
        ttk.Label(frame_izq, text="Masa (kg):", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        masa_var = tk.StringVar(value='1')
        ttk.Entry(frame_izq, textvariable=masa_var, width=27).grid(row=1, column=1, pady=5)
        
        # Temperatura Inicial
        ttk.Label(frame_izq, text="Temperatura Inicial (°C):", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=5)
        temp_inicial_var = tk.StringVar(value='-20')
        ttk.Entry(frame_izq, textvariable=temp_inicial_var, width=27).grid(row=2, column=1, pady=5)
        
        # Temperatura Final
        ttk.Label(frame_izq, text="Temperatura Final (°C):", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', pady=5)
        temp_final_var = tk.StringVar(value='120')
        ttk.Entry(frame_izq, textvariable=temp_final_var, width=27).grid(row=3, column=1, pady=5)
        
        # Botones
        ttk.Button(frame_izq, text="🔥 Calcular Calor Total", 
                  command=callbacks['calcular']).grid(row=4, column=0, columnspan=2, pady=20, sticky='ew')
        
        ttk.Button(frame_izq, text="📐 Despejar Variable", 
                  command=callbacks['despeje']).grid(row=5, column=0, columnspan=2, pady=5, sticky='ew')
        
        # Frame derecho - Constantes
        frame_der = ttk.LabelFrame(frame_principal, text="📈 Constantes del Material", padding=20)
        frame_der.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        
        text_constantes = tk.Text(frame_der, height=15, width=50, font=('Courier', 10))
        text_constantes.pack(fill='both', expand=True)
        
        # Frame inferior - Resultados
        frame_resultados = ttk.LabelFrame(tab_calculadora, text="🎯 Resultados del Cálculo", padding=20)
        frame_resultados.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Texto de resultados
        text_resultados = tk.Text(frame_resultados, height=10, width=100, font=('Arial', 10))
        text_resultados.pack(fill='both', expand=True)
        
        # Frame para el gráfico
        frame_grafico = ttk.Frame(frame_resultados)
        frame_grafico.pack(fill='both', expand=True, pady=10)
        
        # Configurar pesos de columnas
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        
        return {
            'material_var': material_var,
            'masa_var': masa_var,
            'temp_inicial_var': temp_inicial_var,
            'temp_final_var': temp_final_var,
            'text_constantes': text_constantes,
            'text_resultados': text_resultados,
            'frame_grafico': frame_grafico
        }
    
    def configurar_tab_formulas(self, tab_formulas):
        """Configura la pestaña de fórmulas."""
        canvas = tk.Canvas(tab_formulas)
        scrollbar = ttk.Scrollbar(tab_formulas, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        text_widget = tk.Text(scrollable_frame, wrap='word', font=('Courier', 11), 
                            bg='#fffef0', padx=20, pady=20)
        text_widget.insert('1.0', FORMULAS_TEXT)
        text_widget.config(state='disabled')
        text_widget.pack(fill='both', expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def configurar_tab_constantes(self, tab_constantes):
        """Configura la pestaña de constantes."""
        canvas = tk.Canvas(tab_constantes)
        scrollbar = ttk.Scrollbar(tab_constantes, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        text_widget = tk.Text(scrollable_frame, wrap='word', font=('Courier', 11), 
                            bg='#e8f5f0', padx=20, pady=20)
        text_widget.insert('1.0', CONSTANTES_TEXT)
        text_widget.config(state='disabled')
        text_widget.pack(fill='both', expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    @staticmethod
    def actualizar_texto_constantes(text_widget, material, constantes_materiales):
        """Actualiza el texto de constantes para el material seleccionado."""
        const_mat = constantes_materiales[material]
        
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
        
        text_widget.delete('1.0', tk.END)
        text_widget.insert('1.0', texto)
