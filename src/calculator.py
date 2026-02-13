"""
Lógica de cálculo para calorimetría.
"""

from constants import CONSTANTES_MATERIALES


class CalculadoraCalor:
    """Clase para realizar cálculos de calorimetría."""
    
    def __init__(self, constantes=None):
        self.constantes = constantes or CONSTANTES_MATERIALES
    
    def calcular_calor_total(self, material, masa, temp_inicial, temp_final):
        """
        Calcula el calor total necesario para cambiar la temperatura de un material.
        
        Args:
            material (str): Nombre del material
            masa (float): Masa en kg
            temp_inicial (float): Temperatura inicial en °C
            temp_final (float): Temperatura final en °C
            
        Returns:
            tuple: (Q_total, resultados_por_etapa, temperaturas, energias)
        """
        const_mat = self.constantes[material]
        resultados = []
        temperaturas = [temp_inicial]
        energias = [0]
        Q_total = 0
        
        # Para agua: manejo completo de fases
        if material == 'Agua (H₂O)':
            Q_total, temperaturas, energias = self._calcular_agua(
                masa, temp_inicial, temp_final, const_mat, resultados
            )
        else:
            # Para otros materiales
            Q_total, temperaturas, energias = self._calcular_otro_material(
                masa, temp_inicial, temp_final, const_mat, resultados
            )
        
        return Q_total, resultados, temperaturas, energias
    
    def _calcular_agua(self, masa, Ti, Tf, const_mat, resultados):
        """Calcula calor para una sustancia con todas las fases (agua)."""
        temperaturas = [Ti]
        energias = [0]
        Q_total = 0
        
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
        
        return Q_total, temperaturas, energias
    
    def _calcular_otro_material(self, masa, Ti, Tf, const_mat, resultados):
        """Calcula calor para materiales sin todas las fases."""
        temperaturas = [Ti]
        energias = [0]
        Q_total = 0
        
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
        
        return Q_total, temperaturas, energias
    
    @staticmethod
    def formatear_resultados(Q_total, resultados):
        """
        Formatea los resultados para mostrar en la interfaz.
        
        Args:
            Q_total (float): Calor total en Joules
            resultados (list): Lista de resultados por etapa
            
        Returns:
            str: Texto formateado para mostrar
        """
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
        
        return texto
