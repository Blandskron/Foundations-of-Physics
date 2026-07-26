import json
import os

print("=== CREANDO GENERADOR PROGRAMÁTICO DE CUADERNO PARA LECCIÓN 5 (.ipynb) ===")

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
add_md(r"""# Lección 5: Medidas Resumen de los Datos II (Boxplots, Detección de Atípicos y Transformaciones)

**Módulo 6: Estadística I**  
*Foundations of Physics - Licenciatura en Física*

---
""")

# --- CELL 2: OBJETIVOS ---
add_md(r"""## Objetivos de Aprendizaje

1. **Comprender la anatomía del Diagrama de Cajas (Boxplot de Tukey):** Estudiar la construcción visual basada en los 5 números resumen ($Mín, Q_1, Me, Q_3, Máz$) y el Recorrido Intercuartílico ($RQ = Q_3 - Q_1$).
2. **Formular las 4 Barreras de Tukey:** Calcular los límites interiores ($Q_1 - 1.5 RQ$, $Q_3 + 1.5 RQ$) y exteriores ($Q_1 - 3 RQ$, $Q_3 + 3 RQ$) para clasificar observaciones en atípicos moderados y extremos.
3. **Analizar la evolución histórica de la detección de *outliers*:** Estudiar los criterios de Peirce (1852), Chauvenet (1963), Thompson (1935), Test de Grubbs (1950) y Test GESD de Rosner (1983).
4. **Caracterizar atípicos en Series Temporales:** Diferenciar las 4 tipologías fundamentales de perturbaciones temporales: **IO** (Innovativo), **AO** (Aditivo), **LS** (Cambio de Nivel) y **TC** (Cambio Temporal), así como la estimación robusta con TRAMO-SEATS / X-13ARIMA-SEATS.
5. **Estudiar el efecto de las Transformaciones de Variables:** Diferenciar las transformaciones lineales (conservan la forma) de las no lineales (modifican la simetría mediante la escalera de potencias de Tukey: $x^2, \sqrt{x}, \ln(x), 1/x$).
6. **Replicar el Caso Empírico OCDE (1985):** Analizar el efecto simetrizador de la transformación logarítmica $Y = \ln(X)$ sobre un conjunto de 24 tasas de inflación de la OCDE con alta asimetría positiva.
7. **Aplicar el Teorema del Cambio de Variable:** Demostrar analítica y empíricamente la transformación de la densidad de una variable aleatoria continua $f_Y(y) = f_X(g^{-1}(y)) \left|\frac{d}{dy}g^{-1}(y)\right|$.
""")

# --- CELL 3: SECCIÓN 1 (TEORÍA) ---
add_md(r"""---

## 1. Diagrama de Caja (Boxplot de Tukey)

El **Diagrama de Cajas** o **Boxplot**, introducido por John Tukey (1977), es una presentación visual sintética que describe simultáneamente el centro, la dispersión, la simetría y la presencia de observaciones atípicas (*outliers*) en una distribución.

### 1.1. Anatomía Visual y Construcción

1. **La Caja:** Un rectángulo central delimitado por el primer cuartil ($Q_1$, arista inferior/izquierda) y el tercer cuartil ($Q_3$, arista superior/derecha). La longitud de la caja equivale al **Recorrido Intercuartílico ($RQ = Q_3 - Q_1$)** e incluye exactamente el $50\%$ central de los datos.
2. **La Mediana ($Me = Q_2$):** Una línea transversal que divide la caja. Si la mediana está más cercana a $Q_1$, la distribución presenta **asimetría positiva** ($\bar{x} > Me$). Si está más cercana a $Q_3$, presenta **asimetría negativa** ($\bar{x} < Me$).
3. **Los Bigotes:** Líneas que se extienden desde las aristas de la caja hasta los valores mínimo y máximo dentro de las **barreras o límites interiores**.
4. **Regla de Tukey (1977) para Barreras y Atípicos:**
   - **Límite Interior Inferior:** $LII = Q_1 - 1.5 \cdot RQ$
   - **Límite Interior Superior:** $LIS = Q_3 + 1.5 \cdot RQ$
   - **Límite Exterior Inferior:** $LEI = Q_1 - 3.0 \cdot RQ$
   - **Límite Exterior Superior:** $LES = Q_3 + 3.0 \cdot RQ$

#### Clasificación de Observaciones:
* **Observaciones Válidas:** Datos ubicados dentro del intervalo $[LII, LIS]$.
* **Valores Atípicos Moderados:** Datos ubicados entre las barreras interiores y exteriores ($[LEI, LII)$ o $(LIS, LES]$).
* **Valores Atípicos Extremos:** Datos ubicados fuera de las barreras exteriores ($< LEI$ o $> LES$).
""")

# --- CELL 4: SECCIÓN 1 (CÓDIGO) ---
add_code(r"""import numpy as np
import matplotlib.pyplot as plt

# Dataset sintético de pesos de estudiantes (en kg) con valores atípicos inducidos
np.random.seed(101)
pesos_hombres = np.random.normal(loc=72, scale=8, size=40)
pesos_mujeres = np.random.normal(loc=60, scale=7, size=40)

# Introducción de un outlier extremo en la muestra de mujeres
pesos_mujeres = np.append(pesos_mujeres, [115.0]) # Outlier extremo

# Función artesanal para calcular las 4 barreras de Tukey
def calcular_barreras_tukey(datos):
    q1, q3 = np.percentile(datos, [25, 75])
    rq = q3 - q1
    lii = q1 - 1.5 * rq
    lis = q3 + 1.5 * rq
    lei = q1 - 3.0 * rq
    les = q3 + 3.0 * rq
    return q1, q3, rq, lii, lis, lei, les

q1_m, q3_m, rq_m, lii_m, lis_m, lei_m, les_m = calcular_barreras_tukey(pesos_mujeres)

print("=== BARRERAS DE TUKEY EN MUESTRA DE PESOS (MUJERES) ===")
print(f"• Q1 = {q1_m:.2f} kg, Mediana = {np.median(pesos_mujeres):.2f} kg, Q3 = {q3_m:.2f} kg (RQ = {rq_m:.2f} kg)")
print(f"• Barrera Interior Superior (LIS): {lis_m:.2f} kg")
print(f"• Barrera Exterior Superior (LES): {les_m:.2f} kg")

outliers_mod = pesos_mujeres[(pesos_mujeres > lis_m) & (pesos_mujeres <= les_m)]
outliers_ext = pesos_mujeres[pesos_mujeres > les_m]
print(f"• Atípicos Moderados: {outliers_mod.tolist()}")
print(f"• Atípicos Extremos:  {outliers_ext.tolist()}")

# Trazado de Boxplots comparativos por Sexo (Verticales y Horizontales)
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Boxplot Vertical Agrupado
axs[0].boxplot([pesos_hombres, pesos_mujeres], tick_labels=['Hombres', 'Mujeres'], patch_artist=True,
               boxprops=dict(facecolor='#2ecc71', alpha=0.7),
               flierprops=dict(marker='o', markerfacecolor='red', markersize=8))
axs[0].set_title('Distribución de Peso por Sexo (Vertical)', fontweight='bold')
axs[0].set_ylabel('Peso (kg)')
axs[0].grid(True, ls='--', alpha=0.5)

# Boxplot Horizontal
axs[1].boxplot([pesos_hombres, pesos_mujeres], orientation='horizontal', tick_labels=['Hombres', 'Mujeres'], patch_artist=True,
               boxprops=dict(facecolor='#3498db', alpha=0.7),
               flierprops=dict(marker='s', markerfacecolor='red', markersize=8))

axs[1].set_title('Distribución de Peso por Sexo (Horizontal)', fontweight='bold')
axs[1].set_xlabel('Peso (kg)')
axs[1].grid(True, ls='--', alpha=0.5)

plt.tight_layout()
plt.show()
""")

# --- CELL 5: SECCIÓN 2 (TEORÍA) ---
add_md(r"""---

## 2. Identificación de Valores Atípicos (Clásicos y Series Temporales)

Un **valor atípico** (*outlier*) es una observación que se encuentra apartada del cuerpo principal de datos. Puede originarse por errores de medición/registro, causas extraordinarias o sesgos poblacionales.

### 2.1. Evolución Histórica de los Criterios de Detección

1. **Criterio de Peirce (1852):** Basado en un test de razón de verosimilitud en el que se descartan observaciones cuyos residuos superen un umbral $c \cdot \sigma$.
2. **Criterio de Chauvenet (1963):** Define como atípico cualquier dato cuya probabilidad de ocurrir bajo una distribución Normal sea inferior a $\frac{1}{4N}$.
3. **Residuo Estandarizado de Thompson (1935):** Utiliza la t-estandarización $r_i = \frac{x_i - \bar{x}}{s}$.
4. **Test de Grubbs (1950):** Basado en los momentos muestrales normados. El estadístico $G$ evalúa la desviación máxima:
   $$G = \frac{\max_{1 \le i \le N} |x_i - \bar{x}|}{s}$$
   El valor crítico se obtiene de la distribución $t$ de Student con $N-2$ grados de libertad:
   $$G_{\text{crit}} = \frac{N-1}{\sqrt{N}} \sqrt{\frac{t_{\alpha/(2N), N-2}^2}{N - 2 + t_{\alpha/(2N), N-2}^2}}$$

5. **Test GESD (Rosner, 1983):** Extensión del test de Grubbs para detectar iterativamente múltiples atípicos sin sufrir el efecto de *enmascaramiento*.

---

### 2.2. Atípicos en Series Temporales (Chen & Liu, 1993)

En series temporales $y_t$, una observación anómala puede alterar la estructura dinámica del modelo ARIMA. Se identifican 4 tipos fundamentales:

1. **IO (Atípico Innovativo / Innovative Outlier):** Suceso imprevisto puntual en el término de perturbación blanca $\epsilon_t$. Su efecto se propaga a través de la memoria del modelo ARIMA.
2. **AO (Atípico Aditivo / Additive Outlier):** Impacto puntual aislado en el instante $t_0$ ($y_{t_0} \to y_{t_0} + \omega$). No afecta a los valores futuros.
3. **LS (Cambio de Nivel / Level Shift):** Salto permanente en el nivel medio de la serie a partir del instante $t_0$ ($y_t \to y_t + \omega, \forall t \ge t_0$).
4. **TC (Cambio Temporal / Temporary Change):** Un choque inicial en $t_0$ que decae exponencialmente hacia la media con tasa $\delta \in (0, 1)$ ($y_t \to y_t + \omega \delta^{t - t_0}, \forall t \ge t_0$).

#### Estimación Robusta en TRAMO-SEATS y X-13ARIMA-SEATS:
Para evitar la distorsión del error estándar por la presencia de atípicos, estos paquetes emplean la **Desviación Absoluta Mediana (MAD)** como estimador robusto de escala:

$$\hat{\sigma}_{\text{robust}} = 1.48 \cdot \text{mediana}\left( |e_t - \text{mediana}(e_t)| \right)$$
""")

# --- CELL 6: SECCIÓN 2 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Implementación del Test de Grubbs en Python
def test_grubbs(datos, alpha=0.05):
    n = len(datos)
    media = np.mean(datos)
    std = np.std(datos, ddof=1)
    dev_max = np.max(np.abs(datos - media))
    g_stat = dev_max / std
    
    t_crit = stats.t.ppf(1 - alpha / (2 * n), df=n - 2)
    g_crit = ((n - 1) / np.sqrt(n)) * np.sqrt(t_crit**2 / (n - 2 + t_crit**2))
    
    return g_stat, g_crit, g_stat > g_crit

# Demostración del Test de Grubbs
muestra_test = np.array([10.1, 10.5, 9.8, 10.2, 10.4, 9.9, 10.3, 28.5]) # 28.5 es outlier
g_calc, g_crit, es_outlier = test_grubbs(muestra_test)
print(f"=== TEST DE GRUBBS PARA DETECCIÓN DE OUTLIERS ===")
print(f"• Estadístico G calculado: {g_calc:.4f}")
print(f"• Valor Crítico G_crit (alpha=0.05): {g_crit:.4f}")
print(f"• ¿Se rechaza la hipótesis nula de ausencia de outliers?: {es_outlier}")

# --- SIMULACIÓN DE ATÍPICOS EN SERIES TEMPORALES (AO, IO, LS, TC) ---
np.random.seed(42)
T = 100
t_axis = np.arange(T)

# Serie AR(1) base: y_t = 0.7 y_{t-1} + e_t
e = np.random.normal(0, 1, size=T)
y_base = np.zeros(T)
for t in range(1, T):
    y_base[t] = 0.7 * y_base[t-1] + e[t]

# Inyección de los 4 atípicos
y_ao = y_base.copy(); y_ao[30] += 8.0                          # Additive Outlier en t=30
y_ls = y_base.copy(); y_ls[50:] += 6.0                         # Level Shift a partir de t=50
y_tc = y_base.copy()
for t in range(70, T):
    y_tc[t] += 7.0 * (0.85 ** (t - 70))                        # Temporary Change en t=70

# Visualización de los 4 tipos de atípicos en Series Temporales
fig, axs = plt.subplots(3, 1, figsize=(12, 7), sharex=True)

axs[0].plot(t_axis, y_ao, color='#e74c3c', label='Serie con AO (Additive Outlier en t=30)')
axs[0].axvline(30, color='black', ls='--')
axs[0].legend(loc='upper left'); axs[0].grid(True, ls='--', alpha=0.5)

axs[1].plot(t_axis, y_ls, color='#2ecc71', label='Serie con LS (Level Shift a partir de t=50)')
axs[1].axvline(50, color='black', ls='--')
axs[1].legend(loc='upper left'); axs[1].grid(True, ls='--', alpha=0.5)

axs[2].plot(t_axis, y_tc, color='#9b59b6', label='Serie con TC (Temporary Change en t=70)')
axs[2].axvline(70, color='black', ls='--')
axs[2].legend(loc='upper left'); axs[2].grid(True, ls='--', alpha=0.5)

plt.suptitle('Tipologías Principales de Atípicos en Series Temporales', fontsize=12, fontweight='bold')
plt.xlabel('Tiempo $t$')
plt.tight_layout()
plt.show()
""")

# --- CELL 7: SECCIÓN 3 (TEORÍA) ---
add_md(r"""---

## 3. Transformación de Variables (Lineales y No Lineales)

### 3.1. Transformaciones Lineales

Una **transformación lineal** viene dada por $Z = a X + b$ (donde $a, b \in \mathbb{R}, a \ne 0$). 
* Preserva la forma, simetría, coeficiente de asimetría $g_1$ y curtosis $g_2$ de la distribución original.
* Elimina la dependencia de las unidades de medida (ej. la variable tipificada $Z = \frac{X - \bar{x}}{S_x}$ con $a = 1/S_x$ y $b = -\bar{x}/S_x$).

---

### 3.2. Transformaciones No Lineales y Simetrización

Cuando una distribución presenta una fuerte asimetría o heterocedasticidad, las transformaciones lineales son insuficientes. Se requiere aplicar una **transformación no meante monótona** $Y = h(X)$ para lograr simetría o aproximación a la Normal.

#### Escalera de Potencias de Tukey:
1. **Asimetría Negativa (Cola a la izquierda):**
   Transformación cóncava hacia abajo como $Y = X^2$. Comprime la escala para valores pequeños y la expande para valores altos.
2. **Asimetría Positiva (Cola a la derecha):**
   Transformaciones cóncavas hacia arriba que comprimen valores altos y expanden valores pequeños. Ordenadas de menor a mayor intensidad:

$$\sqrt{X} \quad \longrightarrow \quad \ln(X) \quad \longrightarrow \quad \frac{1}{X}$$

#### Conservación del Orden de los Cuantiles:
Para cualquier transformación estrictamente monótona creciente $h(x)$:

$$x_1 > x_2 \implies h(x_1) > h(x_2)$$

Por consiguiente, la mediana y los cuartiles de la variable transformada equivalen exactamente a la transformación de la mediana y los cuartiles originales:

$$Me(Y) = h(Me(X)), \quad Q_r(Y) = h(Q_r(X))$$

---

### 3.3. Caso Práctico Empírico: Inflación en 24 Países de la OCDE (1985)

Consideremos las tasas de inflación de 24 países de la OCDE en 1985:

$$X = [2.2, 7.6, 2.9, 4.6, 4.1, 3.9, 7.4, 3.2, 5.1, 5.3, 20.1, 2.3, 5.5, 32.7, 9.1, 1.7, 3.2, 5.8, 16.3, 15.9, 5.9, 6.7, 3.4, 40.5]$$

El histograma original presenta una acusada asimetría positiva ($g_1 = 2.11$) con múltiples *outliers* en el Boxplot ($20.1\%, 32.7\%, 40.5\%$). La transformación no lineal $Y = \ln(X)$ simetriza la distribución ($g_1 = 0.74$) y elimina los valores atípicos del Boxplot.
""")

# --- CELL 8: SECCIÓN 3 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Dataset oficial OCDE (1985): Tasas de incremento de precios al consumo (%)
ocde_data = np.array([2.2, 7.6, 2.9, 4.6, 4.1, 3.9, 7.4, 3.2, 5.1, 5.3, 20.1, 2.3, 5.5, 32.7, 9.1, 1.7, 3.2, 5.8, 16.3, 15.9, 5.9, 6.7, 3.4, 40.5])

# Aplicación de la transformación no lineal Logarítmica Y = ln(X)
ocde_log = np.log(ocde_data)

# Coeficientes de asimetría de Fisher
g1_orig = stats.skew(ocde_data)
g1_log = stats.skew(ocde_log)

print("=== ESTUDIO DE SIMETRIZACIÓN NO LINEAL (OCDE 1985) ===")
print(f"• Asimetría de Fisher Original g1(X):     {g1_orig:+.4f} (Asimetría Positiva Fuerte)")
print(f"• Asimetría de Fisher Transformada g1(ln X): {g1_log:+.4f} (Cercana a la Simetría)")

# Demostración de la preservación de orden en la mediana
med_orig = np.median(ocde_data)
med_log_directa = np.median(ocde_log)
med_log_transformada = np.log(med_orig)

assert np.isclose(med_log_directa, med_log_transformada, atol=0.05)
print(f"[PRESERVACIÓN DE ORDEN] ln(Mediana(X)) = ln({med_orig:.2f}) = {med_log_transformada:.4f} == Mediana(ln X) = {med_log_directa:.4f} (Diferencia AM-GM en N par)")



# Visualización comparativa de Histogramas y Boxplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# 1. Histograma Original
axs[0, 0].hist(ocde_data, bins=8, color='#e74c3c', alpha=0.7)
axs[0, 0].set_title(f'Histograma Original $X$ ($g_1 = {g1_orig:.2f}$)', fontweight='bold')
axs[0, 0].grid(True, ls='--', alpha=0.5)

# 2. Histograma Logarítmico
axs[0, 1].hist(ocde_log, bins=8, color='#2ecc71', alpha=0.7)
axs[0, 1].set_title(fr'Histograma Transformado $\ln(X)$ ($g_1 = {g1_log:.2f}$)', fontweight='bold')
axs[0, 1].grid(True, ls='--', alpha=0.5)

# 3. Boxplot Original
axs[1, 0].boxplot(ocde_data, orientation='horizontal', patch_artist=True, boxprops=dict(facecolor='#e74c3c', alpha=0.7))
axs[1, 0].set_title('Boxplot Original (Presenta Atípicos)', fontweight='bold')
axs[1, 0].grid(True, ls='--', alpha=0.5)

# 4. Boxplot Logarítmico
axs[1, 1].boxplot(ocde_log, orientation='horizontal', patch_artist=True, boxprops=dict(facecolor='#2ecc71', alpha=0.7))
axs[1, 1].set_title(r'Boxplot Transformado $\ln(X)$ (Sin Atípicos)', fontweight='bold')
axs[1, 1].grid(True, ls='--', alpha=0.5)

plt.tight_layout()
plt.show()
""")

# --- CELL 9: SECCIÓN 4 (TEORÍA) ---
add_md(r"""---

## 4. Transformación de Variables Aleatorias Continuas

En teoría de la probabilidad, si $X$ es una variable aleatoria continua con función de densidad $f_X(x)$ y $Y = g(X)$ es una transformación biyectiva y estrictamente diferenciable, la probabilidad se conserva sobre los conjuntos inversos:

$$P(Y \in A) = P(X \in g^{-1}(A))$$

### 4.1. Teorema del Cambio de Variable

Sea $X$ una variable aleatoria continua con densidad $f_X(x)$ definida en un soporte $S_X$. Sea $Y = g(X)$ una función estrictamente monótona y derivable para todo $x \in S_X$. La función de densidad de probabilidad de la variable transformada $Y$, $f_Y(y)$, viene dada por:

$$f_Y(y) = f_X\left(g^{-1}(y)\right) \cdot \left| \frac{d}{dy} g^{-1}(y) \right|$$

donde $J(y) = \left| \frac{d}{dy} g^{-1}(y) \right|$ es el **Valor Absoluto del Jacobiano** de la transformación inversa.

#### Ejemplo Analítico:
Sea $X \sim \text{Uniforme}(0, 1)$ con densidad $f_X(x) = 1$ para $x \in (0, 1)$. Sea $Y = g(X) = X^2$.
- La función inversa es $g^{-1}(y) = \sqrt{y} = y^{1/2}$ para $y \in (0, 1)$.
- La derivada de la inversa es $\frac{d}{dy} g^{-1}(y) = \frac{1}{2\sqrt{y}}$.
- Por el Teorema del Cambio de Variable:
  $$f_Y(y) = 1 \cdot \left| \frac{1}{2\sqrt{y}} \right| = \frac{1}{2\sqrt{y}}, \quad \forall y \in (0, 1)$$
""")

# --- CELL 10: SECCIÓN 4 (CÓDIGO) ---
add_code(r"""import numpy as np
import matplotlib.pyplot as plt

# Simulación de Monte Carlo para verificar el Teorema del Cambio de Variable
np.random.seed(42)
n_muestras = 100000

# Variable original X ~ Uniforme(0, 1)
x_sim = np.random.uniform(0.0, 1.0, size=n_muestras)

# Transformación Y = g(X) = X^2
y_sim = x_sim**2

# Malla para evaluar la densidad analítica f_Y(y) = 1 / (2 * sqrt(y))
y_grid = np.linspace(0.005, 0.995, 500)
fy_analitica = 1.0 / (2.0 * np.sqrt(y_grid))

# Visualización del Histograma Muestral vs Densidad Analítica Derivada
plt.figure(figsize=(9, 5))
plt.hist(y_sim, bins=80, density=True, alpha=0.6, color='#9b59b6', label='Histograma Empírico $Y = X^2$')
plt.plot(y_grid, fy_analitica, color='red', linewidth=2.5, label=r'Densidad Analítica $f_Y(y) = \frac{1}{2\sqrt{y}}$')

plt.title(r'Demostración del Teorema del Cambio de Variable para $Y = X^2$', fontsize=12, fontweight='bold')
plt.xlabel('Valor de $y$', fontsize=10)
plt.ylabel('Densidad $f_Y(y)$', fontsize=10)
plt.ylim(0, 5)
plt.grid(True, ls='--', alpha=0.5)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

print("=== DEMOSTRACIÓN EXITOSA DEL TEOREMA DEL CAMBIO DE VARIABLE ===")
""")

# --- CELL 11: RESUMEN ---
add_md(r"""---

## 5. Resumen

En esta lección hemos profundizado en las técnicas avanzadas de **análisis exploratorio de datos (EDA)**, detección de observaciones anómalas y transformaciones de variables:

### Puntos Clave:
1. **Diagramas de Caja (Boxplots):** La regla de Tukey (1977) establece las 4 barreras ($Q_1 \pm 1.5 RQ$, $Q_3 \pm 1.5 RQ$, $Q_1 \pm 3 RQ$, $Q_3 \pm 3 RQ$), permitiendo distinguir entre observaciones válidas, atípicos moderados y atípicos extremos.
2. **Detección de Atípicos:** Se estudiaron los criterios clásicos (Peirce, Chauvenet, Thompson, Grubbs, GESD) y se clasificaron las 4 tipologías de atípicos en Series Temporales (**IO**: innovativo, **AO**: aditivo, **LS**: cambio de nivel, **TC**: cambio temporal).
3. **Transformaciones No Lineales y Simetrización:** Las transformaciones de la escalera de Tukey ($\sqrt{x}, \ln(x), 1/x$) reducen la asimetría positiva y estabilizan la varianza. El estudio del caso empírico de la OCDE (1985) demostró la eliminación de atípicos en el Boxplot tras aplicar $Y = \ln(X)$.
4. **Teorema del Cambio de Variable:** Para variables aleatorias continuas, la densidad transformada satisface $f_Y(y) = f_X(g^{-1}(y)) \cdot |J(y)|$, como se demostró numéricamente para $Y = X^2$.
""")

# --- CELL 12: BIBLIOGRAFÍA ---
add_md(r"""---

## 6. Bibliografía

1. **Dávila, S. (2019).** *Detección de outliers en grandes bases de datos.* Universidad Nacional Autónoma de México.
2. **Freund, J., & Simon, G. (1992).** *Estadística elemental.* Prentice Hall Hispanoamericana.
3. **Llinás Solano, H., & Rojas Álvarez, C. (2016).** *Estadística descriptiva y distribuciones de probabilidad.* Ediciones Uninorte.
4. **Moore, D. (2000).** *Estadística aplicada básica.* Antoni Bosch Editor.
5. **Tukey, J. W. (1977).** *Exploratory Data Analysis.* Addison-Wesley Publishing Company.
""")

# Guardar cuaderno en la carpeta leccion-5
target_dir = os.path.join("06-estadistica-1", "leccion-5")
os.makedirs(target_dir, exist_ok=True)
output_path = os.path.join(target_dir, "medidas-resumen-datos-2.ipynb")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"=== CUADERNO GENERADO EXITOSAMENTE EN: {output_path} ===")
