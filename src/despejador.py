"""
Módulo para el despejador de variables.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class VentanaDespejador:
    """Ventana para despejar variables en ecuaciones de calorimetría."""
    
    def __init__(self, parent):
        self.parent = parent
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("📐 Despejar Variable")
        self.ventana.geometry("600x500")
        self.ventana.configure(bg='#f0f0f0')
        
        # Variables de entrada
        self.Q_var = tk.StringVar()
        self.m_var = tk.StringVar()
        self.c_var = tk.StringVar()
        self.Ti_var = tk.StringVar()
        self.Tf_var = tk.StringVar()
        self.deltaT_var = tk.StringVar()
        self.var_calcular = tk.StringVar()
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de la ventana."""
        frame_principal = ttk.Frame(self.ventana, padding=20)
        frame_principal.pack(fill='both', expand=True)
        
        ttk.Label(frame_principal, text="Calculadora de Variables", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(frame_principal, text="Selecciona la variable a calcular:", 
                 font=('Arial', 10)).pack(pady=5)
        
        combo = ttk.Combobox(frame_principal, textvariable=self.var_calcular, 
                            values=['Masa (m)', 'Calor específico (c)', 
                                   'Temperatura final (Tf)', 'Temperatura inicial (Ti)'],
                            state='readonly', width=30)
        combo.pack(pady=10)
        combo.bind('<<ComboboxSelected>>', self._actualizar_campos)
        
        self.frame_inputs = ttk.LabelFrame(frame_principal, text="Datos", padding=20)
        self.frame_inputs.pack(fill='both', expand=True, pady=10)
        
        # Frame para resultados
        frame_resultado = ttk.LabelFrame(frame_principal, text="Resultado", padding=20)
        frame_resultado.pack(fill='both', expand=True, pady=10)
        
        self.text_resultado = tk.Text(frame_resultado, height=5, font=('Arial', 11))
        self.text_resultado.pack(fill='both', expand=True)
        
        ttk.Button(frame_principal, text="Calcular", 
                  command=self._calcular_variable).pack(pady=10)
    
    def _actualizar_campos(self, event=None):
        """Actualiza los campos de entrada según la variable seleccionada."""
        # Limpiar frame
        for widget in self.frame_inputs.winfo_children():
            widget.destroy()
        
        variable = self.var_calcular.get()
        
        if variable == 'Masa (m)':
            ttk.Label(self.frame_inputs, text="Calor (Q) en Joules:").grid(row=0, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.Q_var, width=25).grid(row=0, column=1, pady=5)
            
            ttk.Label(self.frame_inputs, text="Calor específico (c) en J/(kg·°C):").grid(row=1, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.c_var, width=25).grid(row=1, column=1, pady=5)
            
            ttk.Label(self.frame_inputs, text="Cambio de temperatura (ΔT) en °C:").grid(row=2, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.deltaT_var, width=25).grid(row=2, column=1, pady=5)
            
        elif variable == 'Calor específico (c)':
            ttk.Label(self.frame_inputs, text="Calor (Q) en Joules:").grid(row=0, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.Q_var, width=25).grid(row=0, column=1, pady=5)
            
            ttk.Label(self.frame_inputs, text="Masa (m) en kg:").grid(row=1, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.m_var, width=25).grid(row=1, column=1, pady=5)
            
            ttk.Label(self.frame_inputs, text="Cambio de temperatura (ΔT) en °C:").grid(row=2, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.deltaT_var, width=25).grid(row=2, column=1, pady=5)
        
        elif variable == 'Temperatura final (Tf)':
            ttk.Label(self.frame_inputs, text="Calor (Q) en Joules:").grid(row=0, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.Q_var, width=25).grid(row=0, column=1, pady=5)
            
            ttk.Label(self.frame_inputs, text="Masa (m) en kg:").grid(row=1, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.m_var, width=25).grid(row=1, column=1, pady=5)
            
            ttk.Label(self.frame_inputs, text="Calor específico (c) en J/(kg·°C):").grid(row=2, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.c_var, width=25).grid(row=2, column=1, pady=5)
            
            ttk.Label(self.frame_inputs, text="Temperatura inicial (Ti) en °C:").grid(row=3, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.Ti_var, width=25).grid(row=3, column=1, pady=5)
        
        elif variable == 'Temperatura inicial (Ti)':
            ttk.Label(self.frame_inputs, text="Calor (Q) en Joules:").grid(row=0, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.Q_var, width=25).grid(row=0, column=1, pady=5)
            
            ttk.Label(self.frame_inputs, text="Masa (m) en kg:").grid(row=1, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.m_var, width=25).grid(row=1, column=1, pady=5)
            
            ttk.Label(self.frame_inputs, text="Calor específico (c) en J/(kg·°C):").grid(row=2, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.c_var, width=25).grid(row=2, column=1, pady=5)
            
            ttk.Label(self.frame_inputs, text="Temperatura final (Tf) en °C:").grid(row=3, column=0, sticky='w', pady=5)
            ttk.Entry(self.frame_inputs, textvariable=self.Tf_var, width=25).grid(row=3, column=1, pady=5)
    
    def _calcular_variable(self):
        """Calcula la variable despejada."""
        try:
            variable = self.var_calcular.get()
            
            if not variable:
                messagebox.showerror("Error", "Por favor selecciona una variable.")
                return
            
            resultado = ""
            
            if variable == 'Masa (m)':
                Q = float(self.Q_var.get())
                c = float(self.c_var.get())
                deltaT = float(self.deltaT_var.get())
                
                if deltaT == 0:
                    raise ValueError("ΔT no puede ser cero")
                
                m = Q / (c * deltaT)
                resultado = f"Cálculo de la Masa:\n"
                resultado += f"Fórmula: m = Q / (c · ΔT)\n"
                resultado += f"m = {Q} J / ({c} J/(kg·°C) · {deltaT} °C)\n"
                resultado += f"\nm = {m:.4f} kg"
                
            elif variable == 'Calor específico (c)':
                Q = float(self.Q_var.get())
                m = float(self.m_var.get())
                deltaT = float(self.deltaT_var.get())
                
                if m == 0 or deltaT == 0:
                    raise ValueError("Masa y ΔT no pueden ser cero")
                
                c = Q / (m * deltaT)
                resultado = f"Cálculo del Calor Específico:\n"
                resultado += f"Fórmula: c = Q / (m · ΔT)\n"
                resultado += f"c = {Q} J / ({m} kg · {deltaT} °C)\n"
                resultado += f"\nc = {c:.2f} J/(kg·°C)"
            
            elif variable == 'Temperatura final (Tf)':
                Q = float(self.Q_var.get())
                m = float(self.m_var.get())
                c = float(self.c_var.get())
                Ti = float(self.Ti_var.get())
                
                if m == 0 or c == 0:
                    raise ValueError("Masa y calor específico no pueden ser cero")
                
                Tf = Ti + Q / (m * c)
                resultado = f"Cálculo de la Temperatura Final:\n"
                resultado += f"Fórmula: Tf = Ti + Q / (m · c)\n"
                resultado += f"Tf = {Ti} + {Q} / ({m} · {c})\n"
                resultado += f"\nTf = {Tf:.2f} °C"
            
            elif variable == 'Temperatura inicial (Ti)':
                Q = float(self.Q_var.get())
                m = float(self.m_var.get())
                c = float(self.c_var.get())
                Tf = float(self.Tf_var.get())
                
                if m == 0 or c == 0:
                    raise ValueError("Masa y calor específico no pueden ser cero")
                
                Ti = Tf - Q / (m * c)
                resultado = f"Cálculo de la Temperatura Inicial:\n"
                resultado += f"Fórmula: Ti = Tf - Q / (m · c)\n"
                resultado += f"Ti = {Tf} - {Q} / ({m} · {c})\n"
                resultado += f"\nTi = {Ti:.2f} °C"
            
            self.text_resultado.delete('1.0', tk.END)
            self.text_resultado.insert('1.0', resultado)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Por favor ingresa valores numéricos válidos.\n{str(e)}")
        except ZeroDivisionError:
            messagebox.showerror("Error", "El denominador no puede ser cero.")
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
