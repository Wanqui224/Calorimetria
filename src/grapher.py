"""
Módulo para generar gráficos de calorimetría.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class GraficadorCalor:
    """Clase para crear gráficos de procesos termodinámicos."""
    
    @staticmethod
    def crear_diagrama_temperatura_energia(frame_grafico, temps, energias):
        """
        Crea un gráfico de temperatura vs energía.
        
        Args:
            frame_grafico: Widget de tkinter donde se mostrará el gráfico
            temps (list): Lista de temperaturas
            energias (list): Lista de energías en Joules
        """
        # Limpiar frame anterior
        for widget in frame_grafico.winfo_children():
            widget.destroy()
        
        # Crear figura
        fig = Figure(figsize=(12, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Convertir energías a kJ
        energias_kJ = [e/1000 for e in energias]
        
        # Graficar
        ax.plot(energias_kJ, temps, 'o-', color='#667eea', linewidth=2, 
                markersize=8, markerfacecolor='#764ba2')
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
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
