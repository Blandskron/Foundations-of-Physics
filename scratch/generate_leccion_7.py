import json
import os

print("=== CREANDO GENERADOR PROGRAMÁTICO DE CUADERNO PARA LECCIÓN 7 (.ipynb) ===")

notebook = {
    "cells": [],
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.10"
        },
        "orig_nbformat": 4
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

def add_md(text):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True)
    })

def add_code(text):
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True)
    })

# --- CELL 1: TITLE & HEADER ---
add_md(r"""# Lección 7: Series Temporales y Números Índices

**Módulo 6: Estadística I**  
*Foundations of Physics - Licenciatura en Física*

---
""")

# --- CELL 2: OBJETIVOS ---
add_md(r"""## Objetivos de Aprendizaje

1. **Analizar la Evolución Temporal de Magnitudes:** Definir formalmente una serie temporal o cronológica ($Y_t$) y aplicar correcciones por calendario (días hábiles, mes estándar de 30 días) y rupturas de homogeneidad metodológica.
2. **Caracterizar las Componentes Clásicas de una Serie Temporal:** Identificar la Tendencia ($T_t$), el Ciclo ($C_t$), la Estacionalidad ($S_t$) y el Residuo Irregular ($u_t$).
3. **Seleccionar el Esquema de Composición (Aditivo vs Multiplicativo):** Diferenciar el modelo aditivo ($Y_t = T_t + S_t + u_t$) del multiplicativo ($Y_t = T_t \times S_t \times u_t$) evaluando la pendiente de la regresión entre desviaciones típicas y medias anuales ($S_a = b_0 + b_1 \bar{Y}_a$).
4. **Extraer la Tendencia mediante Métodos de Suavizado y Ajuste:** Implementar Medias Móviles centradas ($MM_{12}$), Alisado Exponencial Simple ($ME_t = \alpha Y_t + (1-\alpha) ME_{t-1}$) y Ajuste Lineal por Mínimos Cuadrados.
5. **Calcular Números Índices Simples y Tasas de Variación:** Formular el índice simple ($I_{t,0} = \frac{X_t}{X_0} \times 100$), la tasa de variación porcentual y la Tasa Media de Crecimiento Acumulativo geométrica ($r_{t,0}(m)$).
6. **Formular Índices Compuestos Ponderados de Precios:** Calcular y comparar los índices de Laspeyres ($L^P$), Paasche ($P^P$), Fisher ($F^P = \sqrt{L^P \times P^P}$) e Índice de Valor ($IV$), demostrando la ordenación por el efecto sustitución ($P^P \le F^P \le L^P$).
7. **Analizar el IPC, IPCA Armonizado y Deflactar Series Económicas:** Explicar el Índice de Precios de Consumo (IPC del INE), calcular las tasas intermensual, acumulada e interanual, y transformar magnitudes a precios corrientes (nominales) en magnitudes a precios constantes (reales) ($Y_t^* = \frac{Y_t}{IPC_t} \times 100$).
""")

# --- CELL 3: SECCIÓN 1 (TEORÍA) ---
add_md(r"""---

## 1. Evolución Temporal de Magnitudes y Homogeneidad

Una **serie temporal**, serie histórica o cronológica es una secuencia de observaciones cuantitativas $Y_t$ ordenadas correlativamente en el tiempo ($t = 1, 2, \dots, T$).

### 1.1. Comparabilidad y Correcciones de Calendario

Para garantizar la comparabilidad temporal de los datos, las observaciones deben estar distribuidas de forma homogénea en el tiempo. Debido a que los meses del calendario poseen diferente duración (28, 30 o 31 días), es necesario aplicar factores de corrección de calendario:

$$Y_{t,\text{corregido}} = Y_t \cdot \left( \frac{30}{\text{Días del mes } t} \right)$$

### 1.2. Rupturas de Homogeneidad Metodológica

En series económicas o físicas prolongadas (ej. la Tasa de Paro en España estimada por el INE), la introducción de nuevas definiciones estadísticas o cuestionarios genera saltos artificiales o **rupturas de homogeneidad**. En estos casos es preciso empalmar las series históricas mediante coeficientes de enlace.
""")

# --- CELL 4: SECCIÓN 1 (CÓDIGO) ---
add_code(r"""import numpy as np
import matplotlib.pyplot as plt

# Simulación de producción mensual no corregida por días del mes (febrero=28, marzo=31)
dias_mes = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
prod_cruda = np.array([310, 280, 310, 300, 310, 300, 310, 310, 300, 310, 300, 310])

# Aplicación del factor de corrección por mes estándar de 30 días (30 / días_mes)
prod_corregida = prod_cruda * (30.0 / dias_mes)

print("=== CORRECCIÓN DE CALENDARIO EN SERIES TEMPORALES ===")
print(f"• Producción Cruda Febrero (28 días): {prod_cruda[1]} unidades")
print(f"• Producción Corregida Febrero (30 días equivalentes): {prod_corregida[1]:.2f} unidades")
print(f"• Producción Cruda Marzo (31 días): {prod_cruda[2]} unidades")
print(f"• Producción Corregida Marzo (30 días equivalentes): {prod_corregida[2]:.2f} unidades")

assert np.isclose(prod_corregida[1], prod_corregida[2])
print("[VERIFICACIÓN] Tras la corrección de calendario, la tasa de producción diaria equivalente es constante.")
""")

# --- CELL 5: SECCIÓN 2 (TEORÍA) ---
add_md(r"""---

## 2. Componentes de una Serie Temporal y Esquemas de Composición

Una serie temporal $Y_t$ se descompone en 4 componentes estocásticas:

1. **Tendencia ($T_t$):** Movimiento suave de fondo a largo plazo (10–30 años).
2. **Ciclo ($C_t$):** Oscilaciones no periódicas a medio plazo (3–8 años). Se suelen agrupar como **Tendencia-Ciclo ($TC_t$)**.
3. **Estacionalidad ($S_t$):** Oscillaciones periódicas regulares que se repiten intraanualmente (subperiodos inferiores al año).
4. **Residuo Irregular ($u_t$):** Variaciones aleatorias o erráticas no predecibles ($u_t = Y_t - f(t)$).

### 2.1. Esquemas de Composición

* **Esquema Aditivo:** $Y_t = T_t + S_t + u_t$  
  Válido cuando la amplitud de la oscilación estacional es **constante** e independiente del nivel de la tendencia.
* **Esquema Multiplicativo:** $Y_t = T_t \times S_t \times u_t$  
  Válido cuando la amplitud de la oscilación estacional aumenta o disminuye de forma **proporcional** al nivel de la tendencia.

### 2.2. Criterio de Selección del Esquema (Regresión de Dispersión Anual)

Para determinar el esquema de composición de una serie de $A$ años, se calcula la media anual $\bar{Y}_a$ y la desviación típica anual $S_a$ para cada año $a=1, \dots, A$. Se ajusta por mínimos cuadrados la regresión:

$$S_a = b_0 + b_1 \bar{Y}_a$$

* Si $b_1 \approx 0 \implies$ **Esquema Aditivo** (la variabilidad es independiente del nivel medio).
* Si $b_1 > 0 \implies$ **Esquema Multiplicativo** (la variabilidad crece linealmente con el nivel de la tendencia).
""")

# --- CELL 6: SECCIÓN 2 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats

# Generación sintética de una serie de 5 años (60 meses) con esquema estacional multiplicativo
np.random.seed(42)
t_idx = np.arange(1, 61)
tendencia_real = 100.0 + 2.0 * t_idx

patron_estacional_12 = np.array([0.85, 0.90, 0.95, 1.00, 1.05, 1.15, 1.25, 1.20, 1.10, 1.00, 0.90, 0.85])
estacionalidad_mult = np.tile(patron_estacional_12, 5)

y_serie = tendencia_real * estacionalidad_mult + np.random.normal(0, 3, 60)

# Criterio de Regresión de Dispersión Anual (S_a = b0 + b1 * Y_bar_a)
medias_anuales = [np.mean(y_serie[a*12 : (a+1)*12]) for a in range(5)]
stds_anuales = [np.std(y_serie[a*12 : (a+1)*12], ddof=1) for a in range(5)]

b1, b0, r_val, p_val, _ = stats.linregress(medias_anuales, stds_anuales)

print("=== SELECCIÓN AUTOMÁTICA DEL ESQUEMA DE COMPOSICIÓN ===")
print(f"• Medias Anuales Y_bar_a:  {np.round(medias_anuales, 2).tolist()}")
print(f"• Desviaciones Anuales S_a: {np.round(stds_anuales, 2).tolist()}")
print(f"• Pendiente b1: {b1:.4f} (p-valor = {p_val:.4f})")

if b1 > 0.05 and p_val < 0.05:
    print("-> RESULTADO: Se selecciona el ESQUEMA MULTIPLICATIVO (la amplitud crece con la tendencia).")
else:
    print("-> RESULTADO: Se selecciona el ESQUEMA ADITIVO.")
""")

# --- CELL 7: SECCIÓN 3 (TEORÍA) ---
add_md(r"""---

## 3. Análisis y Extracción de la Tendencia

La extracción o suavizado de la tendencia pretende aislar el movimiento a largo plazo eliminando las fluctuaciones estacionales e irregulares.

### 3.1. Método Mecánico de Medias Móviles Centradas ($MM$)

Para series mensuales ($p=12$), la **media móvil centrada de orden 12** ajusta el desfase temporal ponderando con $0.5$ las observaciones extremas de la ventana de 13 puntos:

$$MM_t = \frac{\frac{1}{2}Y_{t-6} + Y_{t-5} + Y_{t-4} + \dots + Y_{t+5} + \frac{1}{2}Y_{t+6}}{12}$$

---

### 3.2. Alisado Exponencial Simple (Exponential Smoothing)

El **alisado exponencial** asigna pesos decrecientes exponencialmente a las observaciones pasadas mediante un coeficiente de suavizado $\alpha \in (0, 1)$:

$$ME_t = \alpha Y_t + (1 - \alpha) ME_{t-1}$$

Un valor de $\alpha$ alto (ej. $0.8$) da más peso a la observación reciente, mientras que un $\alpha$ bajo (ej. $0.2$) produce un suavizado más intenso de la serie.

---

### 3.3. Ajuste Lineal por Mínimos Cuadrados

Si la tendencia sigue una trayectoria analítica lineal $T_t = b_0 + b_1 t$, los parámetros se estiman resolviendo:

$$b_1 = \frac{S_{Y,t}}{S_t^2} = \frac{\sum_{t=1}^T (t - \bar{t})(Y_t - \bar{Y})}{\sum_{t=1}^T (t - \bar{t})^2}, \quad b_0 = \bar{Y} - b_1 \bar{t}$$
""")

# --- CELL 8: SECCIÓN 3 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# 1. Medias Móviles Centradas MM12
def medias_moviles_12(y):
    n = len(y)
    mm = np.full(n, np.nan)
    pesos = np.array([0.5] + [1.0]*11 + [0.5])
    for t in range(6, n - 6):
        mm[t] = np.sum(y[t-6 : t+7] * pesos) / 12.0
    return mm

# 2. Alisado Exponencial Simple
def alisado_exponencial(y, alpha=0.3):
    n = len(y)
    me = np.zeros(n)
    me[0] = y[0]
    for t in range(1, n):
        me[t] = alpha * y[t] + (1 - alpha) * me[t-1]
    return me

mm12_tend = medias_moviles_12(y_serie)
me_tend = alisado_exponencial(y_serie, alpha=0.3)

# 3. Ajuste Lineal Mínimo Cuadrático T_t = b0 + b1 * t
b1_t, b0_t, _, _, _ = stats.linregress(t_idx, y_serie)
tend_lineal = b0_t + b1_t * t_idx

# Visualización comparativa de los métodos de extracción de tendencia
plt.figure(figsize=(10, 5))
plt.plot(t_idx, y_serie, color='#3498db', alpha=0.4, label='Serie Observada $Y_t$')
plt.plot(t_idx, mm12_tend, color='#e74c3c', lw=2.5, label='Medias Móviles Centradas $MM_{12}$')
plt.plot(t_idx, me_tend, color='#2ecc71', ls='--', lw=2, label=r'Alisado Exponencial ($\alpha=0.3$)')
plt.plot(t_idx, tend_lineal, color='black', ls=':', lw=2, label=f'Ajuste Lineal Mínimo Cuadrático ($b_1={b1_t:.2f}$)')

plt.title('Comparativa de Métodos de Extracción de Tendencia', fontsize=12, fontweight='bold')
plt.xlabel('Mes $t$')
plt.ylabel('Valor de la Variable')
plt.grid(True, ls='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
""")

# --- CELL 9: SECCIÓN 4 (TEORÍA) ---
add_md(r"""---

## 4. Números Índices Simples, Tasas de Variación y Crecimiento Acumulado

Un **número índice** es una medida estadística diseñada para cuantificar las variaciones relativas de una magnitud (o conjunto de magnitudes) en el tiempo o en el espacio.

### 4.1. Índice Simple Temporal ($I_{t,0}$)

Dada una magnitud $X$ observada en un período base $0$ ($X_0$) y en un período actual $t$ ($X_t$):

$$I_{t,0} = \frac{X_t}{X_0} \times 100$$

* $I_{t,0} > 100 \implies$ Crecimiento de la magnitud en el período $t$ respecto a la base.
* $I_{t,0} < 100 \implies$ Decrecimiento de la magnitud.

---

### 4.2. Tasa de Variación Porcentual ($r_{t,0}$)

La **tasa de variación** representa el incremento o decremento relativo expresado en porcentaje:

$$r_{t,0} = \frac{X_t - X_0}{X_0} \times 100 = \left( \frac{I_{t,0}}{100} - 1 \right) \times 100$$

---

### 4.3. Tasa Media de Crecimiento Acumulativo ($r_{t,0}(m)$)

La **tasa media de crecimiento acumulativo** por subperíodo entre el período $0$ y el período $t$ se obtiene mediante la **media geométrica** de los factores de crecimiento entre períodos consecutivos:

$$r_{t,0}(m) = \left( \sqrt[t]{\prod_{j=1}^t \left( 1 + \frac{r_{j, j-1}}{100} \right)} - 1 \right) \times 100 = \left( \sqrt[t]{\frac{X_t}{X_0}} - 1 \right) \times 100$$
""")

# --- CELL 10: SECCIÓN 4 (CÓDIGO) ---
add_code(r"""import numpy as np

# Datos de PIB anual en miles de millones de euros para 4 años consecutivos
pib_anual = np.array([1000.0, 1030.0, 1071.2, 1114.0])

# Cómputo de Índices Simples con base en Año 0 (100.0)
indices_simples = (pib_anual / pib_anual[0]) * 100.0

# Tasas de variación interanuales r_{j, j-1}
tasas_interanuales = np.diff(pib_anual) / pib_anual[:-1] * 100.0

# Tasa Media de Crecimiento Acumulativo Geométrica r_{3,0}(m)
t_periodos = len(pib_anual) - 1
tasa_media_acum = ((pib_anual[-1] / pib_anual[0]) ** (1.0 / t_periodos) - 1.0) * 100.0

print("=== NÚMEROS ÍNDICES SIMPLES Y TASAS ACUMULATIVAS ===")
for t in range(len(pib_anual)):
    print(f"• Año {t}: PIB = {pib_anual[t]:.1f} B€ | Índice I_{{t,0}} = {indices_simples[t]:.2f}")

print(f"\n• Tasas Interanuales Periódiacas: {np.round(tasas_interanuales, 2).tolist()}%")
print(f"• Tasa Media de Crecimiento Acumulativo r_{{3,0}}(m): {tasa_media_acum:.4f}% anual")

# Verificación de reconstrucción geométrica
pib_reconstruido = pib_anual[0] * ((1.0 + tasa_media_acum / 100.0) ** t_periodos)
assert np.isclose(pib_reconstruido, pib_anual[-1])
print(f"[VERIFICACIÓN] PIB reconstruido con tasa media: {pib_reconstruido:.1f} B€ == {pib_anual[-1]:.1f} B€")
""")

# --- CELL 11: SECCIÓN 5 (TEORÍA) ---
add_md(r"""---

## 5. Índices Compuestos Ponderados de Precios (Laspeyres, Paasche y Fisher)

Cuando se analiza un conjunto complejo de $n$ bienes con precios $(p_{i0}, p_{it})$ y cantidades $(q_{i0}, q_{it})$, se emplean **índices compuestos ponderados** para sintetizar la evolución de precios en una sola cifra.

### 5.1. Índice de Precios de Laspeyres ($L^P_{t,0}$)

Pondera los índices simples de precios mediante el valor del consumo en el **período base ($w_{i0} = p_{i0} q_{i0}$)**:

$$L^P_{t,0} = \frac{\sum_{i=1}^n p_{it} q_{i0}}{\sum_{i=1}^n p_{i0} q_{i0}} \times 100$$

* **Propiedad:** Tiende a **sobreestimar la inflación** real debido a que mantiene fija la canasta del período base y no recoge la sustitución del consumidor hacia bienes más baratos (*efecto sustitución*).

---

### 5.2. Índice de Precios de Paasche ($P^P_{t,0}$)

Pondera los índices de precios mediante el valor de las cantidades del **período actual ($w_{it} = p_{i0} q_{it}$)**:

$$P^P_{t,0} = \frac{\sum_{i=1}^n p_{it} q_{it}}{\sum_{i=1}^n p_{i0} q_{it}} \times 100$$

* **Propiedad:** Tiende a **subestimar la inflación** al utilizar la canasta del período actual ajustada tras las respuestas de consumo.

---

### 5.3. Índice de Precios de Fisher ($F^P_{t,0}$)

Definido como la **media geométrica** entre los índices de Laspeyres y Paasche:

$$F^P_{t,0} = \sqrt{L^P_{t,0} \times P^P_{t,0}}$$

* **Propiedades:** Es considerado un *índice ideal* porque cumple estrictamente las propiedades de identidad, inversión temporal y circularidad, corregido contra los sesgos de Laspeyres y Paasche. Satisface la desigualdad de ordenación:

$$P^P_{t,0} \le F^P_{t,0} \le L^P_{t,0}$$

---

### 5.4. Índice de Valor ($IV_{t,0}$)

Muestra la variación conjunta del valor monetario total de la canasta (precios y cantidades):

$$IV_{t,0} = \frac{V_t}{V_0} = \frac{\sum_{i=1}^n p_{it} q_{it}}{\sum_{i=1}^n p_{i0} q_{i0}} \times 100$$
""")

# --- CELL 12: SECCIÓN 5 (CÓDIGO) ---
add_code(r"""import numpy as np

# Cesta de 5 bienes representativos: Precios y Cantidades en T=0 y T=t
precios_0   = np.array([2.5, 10.0, 1.2, 5.0, 15.0])
cantidades_0 = np.array([100,  20, 150, 40,  10])

precios_t   = np.array([3.0, 12.0, 1.5, 4.8, 18.0])
cantidades_t = np.array([90,   18, 160, 45,   8])

# 1. Índice de Laspeyres L^P
laspeyres = (np.sum(precios_t * cantidades_0) / np.sum(precios_0 * cantidades_0)) * 100.0

# 2. Índice de Paasche P^P
paasche = (np.sum(precios_t * cantidades_t) / np.sum(precios_0 * cantidades_t)) * 100.0

# 3. Índice de Fisher F^P
fisher = np.sqrt(laspeyres * paasche)

# 4. Índice de Valor IV
indice_valor = (np.sum(precios_t * cantidades_t) / np.sum(precios_0 * cantidades_0)) * 100.0

print("=== CALCULADORA COMPLETA DE ÍNDICES COMPUESTOS DE PRECIOS ===")
print(f"• Laspeyres L^P: {laspeyres:.4f} (Sobreestima Inflación por canasta base fija)")
print(f"• Paasche P^P:   {paasche:.4f} (Subestima Inflación por ajustarse al consumo actual)")
print(f"• Fisher F^P:    {fisher:.4f} (Índice Ideal sin sesgo)")
print(f"• Índice Valor:  {indice_valor:.4f} (Variación conjunta Precios x Cantidades)")

assert paasche <= fisher <= laspeyres
print("\n[VERIFICACIÓN] Se satisface la relación de ordenación de Fisher: Paasche <= Fisher <= Laspeyres.")
""")

# --- CELL 13: SECCIÓN 6 (TEORÍA) ---
add_md(r"""---

## 6. El Índice de Precios de Consumo (IPC), IPCA y Deflación Económica

El **Índice de Precios de Consumo (IPC)** elaborado por el INE es el principal indicador coyuntural de la inflación. En España se calcula como un **índice de Laspeyres encadenado** que incluye una cesta de 489 artículos divididos en parcelas de consumo.

### 6.1. Tasas de Inflación del IPC

Para un mes $m$ del año $t$:
* **Tasa Intermensual:** $V_{(m-1)t \to mt} = \left( \frac{IPC_{m,t}}{IPC_{m-1,t}} - 1 \right) \times 100$
* **Tasa Acumulada (en lo que va de año):** $V_{\text{dic}(t-1) \to mt} = \left( \frac{IPC_{m,t}}{IPC_{\text{dic},t-1}} - 1 \right) \times 100$
* **Tasa Interanual:** $V_{m(t-1) \to mt} = \left( \frac{IPC_{m,t}}{IPC_{m,t-1}} - 1 \right) \times 100$

---

### 6.2. Deflación de Series Económicas (Precios Corrientes vs Constantes)

Para evaluar el crecimiento real del poder adquisitivo o del PIB eliminando el sesgo inflacionario, las magnitudes expresadas a **precios corrientes (nominales $Y_t$)** se convierten a **precios constantes (reales $Y_t^*$)** dividiendo por el IPC:

$$Y_t^* = \frac{Y_t}{IPC_t} \times 100$$
""")

# --- CELL 14: SECCIÓN 6 (CÓDIGO) ---
add_code(r"""import numpy as np
import matplotlib.pyplot as plt

# Serie simulada de IPC anual e Ingresos familiares corrientes (2020-2023)
anios = np.array([2020, 2021, 2022, 2023])
ipc = np.array([100.0, 103.1, 108.9, 112.5])          # IPC Base 2020
ingreso_nominal = np.array([20000, 20500, 21200, 21800]) # Ingreso nominal corriente (€)

# Deflación a Euros Constantes Base 2020 (Ingreso Real)
ingreso_real = (ingreso_nominal / ipc) * 100.0

# Tasas interanuales de inflación y de ingreso real
tasa_inflacion_interanual = np.diff(ipc) / ipc[:-1] * 100.0
tasa_ingreso_real = np.diff(ingreso_real) / ingreso_real[:-1] * 100.0

print("=== DEFLACIÓN DE MAGNITUDES Y PODER ADQUISITIVO REAL ===")
for i in range(len(anios)):
    print(f"• {anios[i]}: Nominal = {ingreso_nominal[i]}€ | IPC = {ipc[i]:.1f} | Real (Constante 2020) = {ingreso_real[i]:.2f}€")

# Visualización comparativa de Ingreso Nominal vs Real
plt.figure(figsize=(9, 5))
plt.plot(anios, ingreso_nominal, marker='o', color='#2ecc71', lw=2.5, label='Ingreso Nominal (Precios Corrientes)')
plt.plot(anios, ingreso_real, marker='s', color='#e74c3c', lw=2.5, label='Ingreso Real Deflactado (Precios Constantes 2020)')

plt.title('Deflación Económica: Impacto de la Inflación sobre el Poder Adquisitivo', fontsize=12, fontweight='bold')
plt.xlabel('Año')
plt.ylabel('Euros (€)')
plt.grid(True, ls='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
""")

# --- CELL 15: RESUMEN ---
add_md(r"""---

## 7. Resumen

En esta lección hemos abordado el análisis integral de las **series temporales** y la **teoría de números índices**:

### Puntos Clave:
1. **Componentes y Esquemas:** Se diferenciaron las 4 componentes ($T_t, C_t, S_t, u_t$) y se aplicó la regresión de dispersión anual para seleccionar entre esquema aditivo y multiplicativo.
2. **Extracción de Tendencia:** Se compararon las Medias Móviles centradas ($MM_{12}$), el Alisado Exponencial Simple ($ME_t$) y el Ajuste Lineal Mínimo-Cuadrático.
3. **Índices Ponderados:** Se formularon y programaron los índices compuestos de Laspeyres ($L^P$), Paasche ($P^P$) y Fisher ($F^P$), demostrando el cumplimiento de la relación de ordenación $P^P \le F^P \le L^P$.
4. **IPC y Deflación:** Se estudió la estructura del IPC y se implementó la deflación de magnitudes corrientes a precios constantes ($Y_t^* = \frac{Y_t}{IPC_t} \times 100$) para aislar el poder adquisitivo real.
""")

# --- CELL 16: BIBLIOGRAFÍA ---
add_md(r"""---

## 8. Bibliografía

1. **Berenson, M. L., Levine, D. M., & Krehbiel, T. C. (2010).** *Basic Business Statistics: Concepts and Applications.* Pearson International (12th ed.).
2. **Instituto Nacional de Estadística (INE).** *Metodología del Índice de Precios de Consumo (IPC Base 2011/2021).* Madrid, España.
3. **Pérez, R., Caso, C., Río, M. J., & López, A. J. (2011).** *Introducción a la Estadística Económica.* Ediciones Pirámide / Universidad de Oviedo.
""")

# Guardar cuaderno en la carpeta leccion-7
target_dir = os.path.join("06-estadistica-1", "leccion-7")
os.makedirs(target_dir, exist_ok=True)
output_path = os.path.join(target_dir, "series-temporales-numeros-indices.ipynb")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"=== CUADERNO GENERADO EXITOSAMENTE EN: {output_path} ===")
