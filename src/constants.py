"""
Constantes y propiedades termodinámicas de materiales.
"""

CONSTANTES_MATERIALES = {
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


FORMULAS_TEXT = """
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

CONSTANTES_TEXT = """
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
