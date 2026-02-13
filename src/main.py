"""
Calculadora de Calorimetría Completa.

Aplicación interactiva para realizar cálculos de calorimetría con soporte
para cambios de fase, múltiples materiales y visualización gráfica.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from constants import CONSTANTES_MATERIALES
from calculator import CalculadoraCalor
from grapher import GraficadorCalor
from ui import TabConfigurator
from despejador import VentanaDespejador


class CalorimetriaApp:
    """Aplicación principal de calorimetría."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Calorimetría Completa")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Inicializar módulos
        self.calculadora = CalculadoraCalor(CONSTANTES_MATERIALES)
        self.tab_configurator = TabConfigurator(None, CONSTANTES_MATERIALES)
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz principal con pestañas."""
        # Notebook (pestañas)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear pestañas
        tab_calculadora = ttk.Frame(notebook)
        tab_formulas = ttk.Frame(notebook)
        tab_constantes = ttk.Frame(notebook)
        
        notebook.add(tab_calculadora, text='Calculadora')
        notebook.add(tab_formulas, text='Fórmulas y Despejes')
        notebook.add(tab_constantes, text='Constantes')
        
        # Configurar cada pestaña
        self.tab_config = self.tab_configurator.configurar_tab_calculadora(
            tab_calculadora, 
            {
                'calcular': self.calcular,
                'actualizar': self.actualizar_constantes,
                'despeje': self.abrir_despeje
            }
        )
        
        self.tab_configurator.configurar_tab_formulas(tab_formulas)
        self.tab_configurator.configurar_tab_constantes(tab_constantes)
        
        # Actualizar constantes iniciales
        self.actualizar_constantes()
        
    def actualizar_constantes(self, event=None):
        """Actualiza el texto de constantes para el material seleccionado."""
        material = self.tab_config['material_var'].get()
        TabConfigurator.actualizar_texto_constantes(
            self.tab_config['text_constantes'], 
            material, 
            CONSTANTES_MATERIALES
        )
    
    def calcular(self):
        """Realiza el cálculo de calor total."""
        try:
            material = self.tab_config['material_var'].get()
            masa = float(self.tab_config['masa_var'].get())
            Ti = float(self.tab_config['temp_inicial_var'].get())
            Tf = float(self.tab_config['temp_final_var'].get())
            
            # Calcular
            Q_total, resultados, temperaturas, energias = \
                self.calculadora.calcular_calor_total(material, masa, Ti, Tf)
            
            # Mostrar resultados
            texto = CalculadoraCalor.formatear_resultados(Q_total, resultados)
            self.tab_config['text_resultados'].delete('1.0', tk.END)
            self.tab_config['text_resultados'].insert('1.0', texto)
            
            # Graficar
            GraficadorCalor.crear_diagrama_temperatura_energia(
                self.tab_config['frame_grafico'], 
                temperaturas, 
                energias
            )
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
    
    def abrir_despeje(self):
        """Abre la ventana para despejar variables."""
        VentanaDespejador(self.root)


def main():
    """Función principal."""
    root = tk.Tk()
    app = CalorimetriaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()