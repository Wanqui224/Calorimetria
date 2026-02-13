# 🔥 Calculadora de Calorimetría Completa

Una aplicación interactiva para realizar cálculos de calorimetría con soporte para cambios de fase, múltiples materiales y visualización gráfica.

## 📋 Descripción

Esta herramienta educativa permite calcular el calor requerido para cambiar la temperatura de una sustancia, considerando cambios de fase (fusión, vaporización). Incluye:

- **Calculadora integrada** con soporte para calentar/enfriar entre diferentes fases
- **Fórmulas de referencia** con despejes para todas las variables
- **Base de datos de constantes** para materiales comunes (agua, aluminio, cobre, hierro)
- **Gráficos interactivos** que visualizan el proceso termodinámico
- **Despejador de variables** para resolver ecuaciones

## ✨ Características Principales

### 🧮 Calculadora
- Seleccionar material de trabajo
- Ingresar masa, temperatura inicial y final
- Cálculo automático del calor total en procesos complejos
- Manejo automático de cambios de fase
- Visualización de resultados detallados con desglose por etapa

### 📚 Fórmulas y Despejes
Referencia completa de:
- **Calor sensible:** Q = m · c · ΔT
- **Calor latente de fusión:** Q = m · L_f
- **Calor latente de vaporización:** Q = m · L_v
- **Conservación de energía:** ΣQ = 0
- Despejes para cada variable en cada fórmula

### 🔬 Constantes de Materiales
Base de datos con propiedades termodinámicas:
- **Agua (H₂O):** calores específicos por fase, puntos de fusión/ebullición, calores latentes
- **Aluminio:** propiedades de fusión
- **Cobre:** propiedades de fusión
- **Hierro:** propiedades de fusión

### 📊 Gráficos
- Visualización del proceso termodinámico
- Temperatura vs. Calor acumulado
- Identificación clara de cambios de fase

## 🚀 Uso

1. Ejecutar la aplicación:
```bash
python src/main.py
```

2. **En la pestaña Calculadora:**
   - Seleccionar un material del menú desplegable
   - Ingresar la masa del objeto (en kg)
   - Ingresar temperatura inicial (en °C)
   - Ingresar temperatura final (en °C)
   - Presionar "Calcular Calor Total"

3. Los resultados mostrarán:
   - Calor total requerido (en Joules)
   - Desglose de calor por cada etapa
   - Representación gráfica del proceso

## 🛠️ Ejemplos de Uso

### Ejemplo 1: Calentar agua de -20°C a 120°C
```
Material: Agua (H₂O)
Masa: 1 kg
Temperatura inicial: -20°C
Temperatura final: 120°C

Resultado:
- Calentar hielo de -20°C a 0°C: Q₁ = m·c_hielo·ΔT
- Fusionar hielo a agua a 0°C: Q₂ = m·L_f
- Calentar agua de 0°C a 100°C: Q₃ = m·c_agua·ΔT
- Vaporizar agua a 100°C: Q₄ = m·L_v
- Calentar vapor de 100°C a 120°C: Q₅ = m·c_vapor·ΔT
- Q_total = Q₁ + Q₂ + Q₃ + Q₄ + Q₅
```

## 📦 Requisitos

- Python 3.6+
- tkinter (incluido con Python)
- matplotlib
- numpy

## 📝 Estructura del Proyecto

```
Calorimetria/
├── README.md
└── src/
    └── main.py          # Aplicación principal
```

## 🔧 Interfaz Gráfica

La aplicación usa **tkinter** con diseño moderno basado en pestañas:

1. **Pestana "Calculadora":** Interfaz principal para cálculos
2. **Pestaña "Fórmulas y Despejes":** Referencia teórica
3. **Pestaña "Constantes":** Base de datos de materiales

## 📐 Conceptos Científicos

### Calor Sensible
Cambio de temperatura SIN cambio de fase:
```
Q = m · c · ΔT
```

### Calor Latente
Cambio de fase a temperatura constante:
```
Q_fusión = m · L_f
Q_vaporización = m · L_v
```

### Conservación de Energía
En un sistema aislado:
```
Q_cedido + Q_absorbido = 0
```

## 📝 Notas

- Todas las temperaturas se expresan en **°C**
- Todas las masas en **kg**
- El calor se calcula en **Joules (J)**
- Las constantes se basan en valores estándar de 25°C

## 👨‍💻 Autor

Proyecto de calorimetría para estudios de termodinámica - 3° Semestre

---

**Última actualización:** Febrero 2026
