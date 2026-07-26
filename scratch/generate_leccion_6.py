import json
import os

print("=== CREANDO GENERADOR PROGRAMÁTICO DE CUADERNO PARA LECCIÓN 6 (.ipynb) CORREGIDO ===")

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
add_md(r"""# Lección 6: Análisis Conjunto de Dos Variables Estadísticas

**Módulo 6: Estadística I**  
*Foundations of Physics - Licenciatura en Física*

---
""")

# --- CELL 2: OBJETIVOS ---
add_md(r"""## Objetivos de Aprendizaje

1. **Construir e interpretar Tablas Bidimensionales:** Formular tablas de contingencia y tablas de correlación ($k \times m$), definiendo la frecuencia conjunta absoluta ($n_{ij}$) y relativa ($f_{ij} = n_{ij}/N$), y visualizando distribuciones en Nubes de Puntos (*Scatter Plots*).
2. **Caracterizar Distribuciones Marginales y Condicionales:** Derivar las frecuencias marginales ($n_{i\cdot}, n_{\cdot j}$), medias marginales ($\bar{x}, \bar{y}$) y varianzas marginales ($S_x^2, S_y^2$). Cómputo de distribuciones condicionales ($X|y_j, Y|x_i$) y demostración formal del Teorema de la Esperanza Total ($\bar{x} = \sum (\bar{x}|y_j) f_{\cdot j}$).
3. **Evaluar la Independencia Estadística:** Analizar la condición formal de independencia de frecuencias ($f_{ij} = f_{i\cdot} \cdot f_{\cdot j} \iff n_{ij} = \frac{n_{i\cdot} n_{\cdot j}}{N}$) y diferenciarla de la dependencia funcional ($Y = f(X)$).
4. **Cuantificar la Asociación en Caracteres Cualitativos y Ordinales:** Calcular el Coeficiente Chi-cuadrado de Pearson ($\chi^2$), el Coeficiente de Contingencia de Pearson ($C$) y el Coeficiente $\tau$ de Kendall para pares concordantes y discordantes.
5. **Calcular e Interpretar Medidas de Dependencia Lineal:** Determinar la Covarianza ($S_{XY}$) y el Coeficiente de Correlación Lineal de Pearson ($r_{XY} \in [-1, +1]$), probando analítica y numéricamente sus propiedades ante transformaciones de origen y escala.
6. **Demostrar que la Incorrelación no implica Independencia:** Probar mediante simulaciones numéricas que variables con una relación funcional determinista perfecta (ej. $Y = X^2$) pueden presentar $S_{XY} = 0$ y $r_{XY} = 0$ debido a la simetría de las desviaciones.
7. **Identificar Correlaciones Espurias y Variables Confusoras:** Simular y analizar el riesgo de inferir causalidad errónea cuando dos variables independientes están correlacionadas debido al efecto de un factor de confusión latente.
""")

# --- CELL 3: SECCIÓN 1 (TEORÍA) ---
add_md(r"""---

## 1. Distribuciones Bidimensionales

En la investigación física y social es habitual observar simultáneamente dos caracteres o variables $(X, Y)$ sobre una misma población de tamaño $N$.

### 1.1. Notación y Estructura Tabular

Sea $X$ una variable que toma $k$ modalidades $\{x_1, x_2, \dots, x_k\}$ e $Y$ una variable que toma $m$ modalidades $\{y_1, y_2, \dots, y_m\}$.

* **Frecuencia Absoluta Conjunta ($n_{ij}$):** Número de individuos que presentan simultáneamente la modalidad $x_i$ de $X$ y la modalidad $y_j$ de $Y$.
* **Tamaño Poblacional Total ($N$):**
  $$N = \sum_{i=1}^k \sum_{j=1}^m n_{ij}$$
* **Frecuencia Relativa Conjunta ($f_{ij}$):** Proporción de observaciones en el par $(x_i, y_j)$:
  $$f_{ij} = \frac{n_{ij}}{N}, \quad \sum_{i=1}^k \sum_{j=1}^m f_{ij} = 1$$

#### Tabla de Contingencia / Correlación ($k \times m$):

| $X \setminus Y$ | $y_1$ | $y_2$ | $\dots$ | $y_m$ | Frecuencia Marginal $X$ ($n_{i\cdot}$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $x_1$ | $n_{11}$ | $n_{12}$ | $\dots$ | $n_{1m}$ | $n_{1\cdot} = \sum_j n_{1j}$ |
| $x_2$ | $n_{21}$ | $n_{22}$ | $\dots$ | $n_{2m}$ | $n_{2\cdot} = \sum_j n_{2j}$ |
| $\vdots$ | $\vdots$ | $\vdots$ | $\ddots$ | $\vdots$ | $\vdots$ |
| $x_k$ | $n_{k1}$ | $n_{k2}$ | $\dots$ | $n_{km}$ | $n_{k\cdot} = \sum_j n_{kj}$ |
| **Frecuencia Marginal $Y$ ($n_{\cdot j}$)** | $n_{\cdot 1} = \sum_i n_{i1}$ | $n_{\cdot 2} = \sum_i n_{i2}$ | $\dots$ | $n_{\cdot m} = \sum_i n_{im}$ | **$N$** |

---

### 1.2. Representación Gráfica: Nube de Puntos (Scatter Plot)

En variables cuantitativas, la representación gráfica cartesiana proyecta cada par de observaciones $(x_i, y_j)$ como un punto en el plano. La disposición geométrica de la nube de puntos revela intuitivamente la presencia de relaciones lineales directas, inversas o no lineales.
""")

# --- CELL 4: SECCIÓN 1 (CÓDIGO) ---
add_code(r"""import numpy as np
import matplotlib.pyplot as plt

# Simulación de un dataset bidimensional (X: Horas de Estudio, Y: Calificación Obtenida)
np.random.seed(42)
n_estudiantes = 100
horas_estudio = np.random.uniform(5, 45, size=n_estudiantes)
calificacion = 2.0 + 0.18 * horas_estudio + np.random.normal(loc=0, scale=1.2, size=n_estudiantes)

# Visualización de la Nube de Puntos (Scatter Plot)
plt.figure(figsize=(8, 5))
plt.scatter(horas_estudio, calificacion, color='#3498db', edgecolors='k', alpha=0.8, label='Estudiantes ($x_i, y_i$)')

plt.title('Representación Bidimensional: Nube de Puntos (Scatter Plot)', fontsize=12, fontweight='bold')
plt.xlabel('Horas de Estudio Semanales ($X$)', fontsize=10)
plt.ylabel('Calificación Obtenida ($Y$)', fontsize=10)
plt.grid(True, ls='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
""")

# --- CELL 5: SECCIÓN 2 (TEORÍA) ---
add_md(r"""---

## 2. Distribuciones Marginales y Condicionales

### 2.1. Distribuciones Marginales

Las **distribuciones marginales** analizan el comportamiento unidimensional de una de las variables ignorando las modalidades de la otra.

* **Frecuencias Marginales Absolutas:**
  $$n_{i\cdot} = \sum_{j=1}^m n_{ij}, \quad n_{\cdot j} = \sum_{i=1}^k n_{ij}$$

* **Frecuencias Marginales Relativas:**
  $$f_{i\cdot} = \frac{n_{i\cdot}}{N} = \sum_{j=1}^m f_{ij}, \quad f_{\cdot j} = \frac{n_{\cdot j}}{N} = \sum_{i=1}^k f_{ij}$$

* **Medias y Varianzas Marginales:**
  $$\bar{x} = \sum_{i=1}^k x_i f_{i\cdot} = \frac{1}{N}\sum_{i=1}^k x_i n_{i\cdot}, \quad S_x^2 = \sum_{i=1}^k (x_i - \bar{x})^2 f_{i\cdot}$$
  $$\bar{y} = \sum_{j=1}^m y_j f_{\cdot j} = \frac{1}{N}\sum_{j=1}^m y_j n_{\cdot j}, \quad S_y^2 = \sum_{j=1}^m (y_j - \bar{y})^2 f_{\cdot j}$$

---

### 2.2. Distribuciones Condicionales

La **distribución de $X$ condicionada a $Y = y_j$** ($X|y_j$) es la distribución unidimensional de $X$ considerando únicamente los individuos que presentan la modalidad $y_j$.

* **Frecuencia Relativa Condicional de $X$ dado $Y = y_j$:**
  $$f_{i|j} = P(X = x_i \mid Y = y_j) = \frac{n_{ij}}{n_{\cdot j}} = \frac{f_{ij}}{f_{\cdot j}}$$

* **Media Condicional de $X$ dado $Y = y_j$:**
  $$\bar{x}|y_j = \sum_{i=1}^k x_i f_{i|j} = \frac{1}{n_{\cdot j}}\sum_{i=1}^k x_i n_{ij}$$

* **Varianza Condicional de $X$ dado $Y = y_j$:**
  $$S_{X|y_j}^2 = \sum_{i=1}^k (x_i - \bar{x}|y_j)^2 f_{i|j}$$

---

### 2.3. Teorema de la Esperanza Total (Media de Medias Condicionales)

La media marginal de $X$ equivale a la media ponderada de las medias condicionales de $X$ a los distintos valores de $Y$:

$$\bar{x} = \sum_{j=1}^m (\bar{x}|y_j) f_{\cdot j} = \frac{\sum_{j=1}^m (\bar{x}|y_j) n_{\cdot j}}{N}$$
""")

# --- CELL 6: SECCIÓN 2 (CÓDIGO) ---
add_code(r"""import numpy as np

class DistribucionBidimensional:
    # Motor artesanal para el procesamiento de distribuciones bidimensionales 
    # y cómputo de estadísticos marginales y condicionales.
    def __init__(self, x_vals, y_vals, tabla_freq):
        self.x = np.array(x_vals)
        self.y = np.array(y_vals)
        self.n_ij = np.array(tabla_freq)
        self.N = np.sum(self.n_ij)
        
        self.n_i_dot = np.sum(self.n_ij, axis=1) # Marginal X
        self.n_dot_j = np.sum(self.n_ij, axis=0) # Marginal Y
        
        self.f_ij = self.n_ij / self.N
        self.f_i_dot = self.n_i_dot / self.N
        self.f_dot_j = self.n_dot_j / self.N

    def media_marginal_x(self):
        return np.sum(self.x * self.f_i_dot)

    def media_marginal_y(self):
        return np.sum(self.y * self.f_dot_j)

    def varianza_marginal_x(self):
        m_x = self.media_marginal_x()
        return np.sum((self.x - m_x)**2 * self.f_i_dot)

    def media_condicional_x_dado_y(self, j_idx):
        # Distribución de X condicionada a Y = y_j
        f_cond = self.n_ij[:, j_idx] / self.n_dot_j[j_idx]
        return np.sum(self.x * f_cond)

# Carga de datos de prueba (Tabla 3x3: Estudios X vs Ingresos Y)
x_nom = [1, 2, 3] # Primaria, Secundaria, Universidad
y_nom = [10, 25, 50] # 10k, 25k, 50k €
matriz_frecuencias = [
    [50, 20, 10],
    [30, 60, 30],
    [10, 40, 100]
]

dist_bidim = DistribucionBidimensional(x_nom, y_nom, matriz_frecuencias)

m_x = dist_bidim.media_marginal_x()
m_y = dist_bidim.media_marginal_y()
var_x = dist_bidim.varianza_marginal_x()

medias_x_cond = [dist_bidim.media_condicional_x_dado_y(j) for j in range(len(y_nom))]
esperanza_total_x = np.sum(np.array(medias_x_cond) * dist_bidim.f_dot_j)

print("=== ESTADÍSTICOS MARGINALES Y CONDICIONALES ===")
print(f"• Media Marginal de X:    {m_x:.4f}")
print(f"• Varianza Marginal de X: {var_x:.4f}")
print(f"• Media Marginal de Y:    {m_y:.4f} k€")
print(f"• Medias Condicionales X|Y=yj: {np.round(medias_x_cond, 4).tolist()}")
print(f"• Esperanza Total de X:   {esperanza_total_x:.4f} == Media Marginal X: {m_x:.4f}")

assert np.isclose(esperanza_total_x, m_x, atol=1e-10)
print("\n[VERIFICACIÓN] Se satisface el Teorema de la Esperanza Total: E[E[X|Y]] = E[X].")
""")

# --- CELL 7: SECCIÓN 3 (TEORÍA) ---
add_md(r"""---

## 3. Dependencia e Independencia Estadística

En el análisis bidimensional es fundamental diferenciar tres niveles de relación entre variables:

1. **Dependencia Funcional:** Existe una aplicación unívoca y determinista $Y = f(X)$ tal que conocido $X$, el valor de $Y$ queda perfectamente determinado sin incertidumbre.
2. **Independencia Estadística:** El conocimiento de la modalidad de una variable no altera la distribución de frecuencias de la otra.
3. **Dependencia Estadística (Estocástica):** Las variables presentan una relación parcial o asociación no determinista.

### 3.1. Condición Formal de Independencia Estadística

Dos variables $X$ e $Y$ son **independientes estadísticamente** si y solo si todas las distribuciones condicionales coinciden entre sí y son iguales a la distribución marginal correspondiente:

$$f(x_i \mid y_j) = f_{i\cdot} \quad \forall i, j \iff f(y_j \mid x_i) = f_{\cdot j} \quad \forall i, j$$

De forma equivalente, la **frecuencia relativa conjunta** de cualquier par $(x_i, y_j)$ es igual al producto de sus frecuencias relativas marginales:

$$f_{ij} = f_{i\cdot} \cdot f_{\cdot j} \quad \forall i, j$$

En términos de frecuencias absolutas, las **frecuencias esperadas bajo independencia ($E_{ij}$)** satisfacen:

$$n_{ij} = E_{ij} = \frac{n_{i\cdot} \cdot n_{\cdot j}}{N} \quad \forall i=1,\dots,k; \; j=1,\dots,m$$
""")

# --- CELL 8: SECCIÓN 3 (CÓDIGO) ---
add_code(r"""import numpy as np

def evaluar_independencia(tabla_frecuencias, atol=1e-5):
    # Evalúa si una matriz de frecuencias satisface la condición formal 
    # de independencia estadística: n_ij == (n_i. * n_.j) / N
    N = np.sum(tabla_frecuencias)
    n_i_dot = np.sum(tabla_frecuencias, axis=1)
    n_dot_j = np.sum(tabla_frecuencias, axis=0)
    
    # Matriz de frecuencias esperadas bajo independencia estricta
    frecuencias_esperadas = np.outer(n_i_dot, n_dot_j) / N
    
    es_independiente = np.allclose(tabla_frecuencias, frecuencias_esperadas, atol=atol)
    error_maximo = np.max(np.abs(tabla_frecuencias - frecuencias_esperadas))
    
    return es_independiente, frecuencias_esperadas, error_maximo

# Ejemplo 1: Tabla de datos dependientes
tabla_dep = np.array([[50, 20], [30, 60]])
indep1, esp1, err1 = evaluar_independencia(tabla_dep)

# Ejemplo 2: Tabla construida bajo independencia estricta (n_ij = n_i. * n_.j / N)
n_i = np.array([100, 200])
n_j = np.array([60, 240])
tabla_indep = np.outer(n_i, n_j) / 300.0
indep2, esp2, err2 = evaluar_independencia(tabla_indep)

print("=== EVALUACIÓN FORMAL DE INDEPENDENCIA ESTADÍSTICA ===")
print(f"• Tabla 1 -> ¿Es independiente?: {indep1} (Error máximo respecto a teórica: {err1:.2f})")
print(f"• Tabla 2 -> ¿Es independiente?: {indep2} (Error máximo respecto a teórica: {err2:.5e})")
""")

# --- CELL 9: SECCIÓN 4 (TEORÍA) ---
add_md(r"""---

## 4. Medidas de Asociación para Caracteres Cualitativos y Ordinales

Cuando se analizan atributos cualitativos o categóricos recogidos en una tabla de contingencia $k \times m$, la asociación se cuantifica mediante la discrepancia entre las frecuencias observadas ($n_{ij}$) y las frecuencias esperadas bajo independencia ($E_{ij} = \frac{n_{i\cdot} n_{\cdot j}}{N}$).

### 4.1. Coeficiente Chi-Cuadrado de Pearson ($\chi^2$)

$$\chi^2 = \sum_{i=1}^k \sum_{j=1}^m \frac{\left( n_{ij} - \frac{n_{i\cdot} n_{\cdot j}}{N} \right)^2}{\frac{n_{i\cdot} n_{\cdot j}}{N}} = N \sum_{i=1}^k \sum_{j=1}^m \frac{(f_{ij} - f_{i\cdot} f_{\cdot j})^2}{f_{i\cdot} f_{\cdot j}}$$

* **Propiedades:**
  - $\chi^2 \ge 0$.
  - $\chi^2 = 0 \iff X$ e $Y$ son strictly independientes.
  - Depende del tamaño muestral $N$, por lo que no permite comparar tablas de tamaños distintos.

---

### 4.2. Coeficiente de Contingencia de Pearson ($C$)

Para normalizar la medida de asociación en una escala acotada $C \in [0, 1)$:

$$C = \sqrt{\frac{\chi^2}{N + \chi^2}}$$

* $C = 0 \iff X$ e $Y$ son independientes. Mayor valor de $C$ indica mayor intensidad de asociación.

---

### 4.3. Coeficiente $\tau$ de Kendall (Variables Ordinales)

Para variables ordinales donde las modalidades admiten un orden natural, se analiza si los pares de observaciones son **concordantes** ($P$) o **discordantes** ($Q$):

$$\tau = \frac{P - Q}{\frac{N(N-1)}{2}} \in [-1, +1]$$

* $P$: Pares donde $x_i > x_j$ y $y_i > y_j$ (o $x_i < x_j$ y $y_i < y_j$).
* $Q$: Pares donde $x_i > x_j$ y $y_i < y_j$ (o $x_i < x_j$ y $y_i > y_j$).
""")

# --- CELL 10: SECCIÓN 4 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats

# Dataset de prueba cualitativo: Evaluación de Desempeño vs Satisfacción Laboral
tabla_contingencia = np.array([
    [45, 15, 5],   # Baja satisfacción
    [15, 50, 20],  # Media satisfacción
    [5,  25, 65]   # Alta satisfacción
])

N_total = np.sum(tabla_contingencia)
n_i_dot = np.sum(tabla_contingencia, axis=1)
n_dot_j = np.sum(tabla_contingencia, axis=0)

# Cómputo artesanal del Coeficiente Chi-Cuadrado de Pearson
frecuenciales_esperadas = np.outer(n_i_dot, n_dot_j) / N_total
chi2_art = np.sum((tabla_contingencia - frecuenciales_esperadas)**2 / frecuenciales_esperadas)

# Coeficiente de Contingencia C de Pearson
c_pearson = np.sqrt(chi2_art / (N_total + chi2_art))

# Validación contra SciPy
chi2_scipy, p_val, dof, _ = stats.chi2_contingency(tabla_contingencia)

assert np.isclose(chi2_art, chi2_scipy, atol=1e-5)

print("=== MEDIDAS DE ASOCIACIÓN CUALITATIVA ===")
print(f"• Chi-Cuadrado Artesanal: {chi2_art:.4f} == SciPy: {chi2_scipy:.4f}")
print(f"• p-valor de la prueba:   {p_val:.5e} (Rechaza Independencia)")
print(f"• Coeficiente C Pearson:  {c_pearson:.4f} (Intensidad de asociación media-alta)")
""")

# --- CELL 11: SECCIÓN 5 (TEORÍA) ---
add_md(r"""---

## 5. La Correlación Lineal y sus Medidas

Para variables cuantitativas, el grado de dependencia lineal se cuantifica mediante la **Covarianza** y el **Coeficiente de Correlación de Pearson**.

### 5.1. La Covarianza ($S_{XY}$)

La **covarianza** es el promedio del producto de las desviaciones de cada variable respecto a sus medias marginales:

$$S_{XY} = \frac{1}{N}\sum_{i=1}^k \sum_{j=1}^m (x_i - \bar{x})(y_j - \bar{y}) n_{ij} = \left( \frac{1}{N}\sum_{i=1}^k \sum_{j=1}^m x_i y_j n_{ij} \right) - \bar{x}\bar{y}$$

#### Propiedades Fundamentales de la Covarianza:
1. **Signo e Interpretación Geométrica:**
   - $S_{XY} > 0$: Relación lineal directa (predominio de puntos en cuadrantes I y III).
   - $S_{XY} < 0$: Relación lineal inversa (predominio de puntos en cuadrantes II y IV).
2. **Independencia e Incorrelación:**
   - Si $X$ e $Y$ son independientes $\implies S_{XY} = 0$.
   - **¡ATENCIÓN! El recíproco no es cierto:** $S_{XY} = 0 \centernot\implies$ Independencia. Puede existir dependencia funcional no lineal cuadrática o circular con $S_{XY} = 0$.
3. **Invariancia ante Cambios de Origen:** Si $X' = X + a$ e $Y' = Y + b \implies S_{X'Y'} = S_{XY}$.
4. **Cambio de Escala:** Si $X' = c X$ e $Y' = d Y \implies S_{X'Y'} = c \cdot d \cdot S_{XY}$.

---

### 5.2. Coeficiente de Correlación Lineal de Pearson ($r_{XY}$)

Para eliminar la dependencia de las unidades de medida de $S_{XY}$, se divide por el producto de las desviaciones típicas marginales:

$$r_{XY} = \frac{S_{XY}}{S_X S_Y}$$

#### Propiedades del Coeficiente $r_{XY}$:
* **Acotamiento:** $-1 \le r_{XY} \le +1$.
* **Dependencia Funcional Lineal Perfecta:**
  - $r_{XY} = +1 \iff Y = a X + b$ con $a > 0$.
  - $r_{XY} = -1 \iff Y = a X + b$ con $a < 0$.
* **Incorrelación Lineal:** $r_{XY} = 0$.
* **Invariancia ante Cambios de Escala:** $r_{c X, d Y} = \text{signo}(c \cdot d) \cdot r_{XY}$.

---

### 5.3. Correlaciones Espurias y Variables Confusoras Latentes

Un valor $r_{XY} \approx 1$ **nunca demuestra relación de causa y efecto**. Frecuentemente se observan **correlaciones espurias** donde $X$ e $Y$ son independientes pero muestran alta correlación lineal empírica debido a que ambas están influenciadas por una tercera variable confusora latente $Z$ (ej. ventas de helados vs incidentes por ahogamiento causados por la temperatura exterior $Z$).
""")

# --- CELL 12: SECCIÓN 5 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# 1. Demostración: Incorrelación (r=0) en una relación funcional parabólica perfecta Y = X^2
x_parabola = np.array([-3, -2, -1, 0, 1, 2, 3])
y_parabola = x_parabola**2

cov_parab = np.mean((x_parabola - np.mean(x_parabola)) * (y_parabola - np.mean(y_parabola)))
r_parab, _ = stats.pearsonr(x_parabola, y_parabola)

print("=== DEMOSTRACIÓN: INCORRELACIÓN VS INDEPENDENCIA ===")
print(f"• Parábola Y = X^2 -> Covarianza S_XY: {cov_parab:.5e}")
print(f"• Parábola Y = X^2 -> Coeficiente r_XY: {r_parab:.5e} == 0")
assert np.isclose(r_parab, 0, atol=1e-10)
print("[CONCLUSIÓN] r_XY = 0 NO implica independencia (existe dependencia funcional cuadrática).")

# 2. Simulación de Correlación Espuria por Variable Confusora Latente
np.random.seed(123)
n_obs = 150
z_temperatura = np.random.normal(loc=28, scale=6, size=n_obs) # Variable Confusora Z

x_helados = 3.5 * z_temperatura + np.random.normal(loc=0, scale=4, size=n_obs)
y_ahogamientos = 2.1 * z_temperatura + np.random.normal(loc=0, scale=5, size=n_obs)

r_espurio, _ = stats.pearsonr(x_helados, y_ahogamientos)
print(f"\n=== CORRELACIÓN ESPURIA PROVOCADA POR FACTOR LATENTE ===")
print(f"• Correlación entre Ventas de Helados y Ahogamientos: r = {r_espurio:.4f}")

# Visualización gráfica de la parábola y de la correlación espuria
fig, axs = plt.subplots(1, 2, figsize=(13, 5))

# Parábola
axs[0].scatter(x_parabola, y_parabola, color='#e74c3c', s=80, zorder=3)
axs[0].plot(np.linspace(-3.2, 3.2, 100), np.linspace(-3.2, 3.2, 100)**2, 'r--', label=r'$Y = X^2$')
axs[0].set_title(r'Dependencia Cuadrática con $r_{XY} = 0$', fontweight='bold')
axs[0].set_xlabel('Variable $X$')
axs[0].set_ylabel('Variable $Y$')
axs[0].grid(True, ls='--', alpha=0.5)
axs[0].legend()

# Correlación Espuria
sc = axs[1].scatter(x_helados, y_ahogamientos, c=z_temperatura, cmap='coolwarm', s=40, alpha=0.8)
cbar = plt.colorbar(sc, ax=axs[1])
cbar.set_label('Temperatura Latente Z (°C)')
axs[1].set_title(f'Correlación Espuria ($r_{{XY}} = {r_espurio:.2f}$)', fontweight='bold')
axs[1].set_xlabel('Ventas de Helados ($X$)')
axs[1].set_ylabel('Incidentes ($Y$)')
axs[1].grid(True, ls='--', alpha=0.5)

plt.tight_layout()
plt.show()
""")

# --- CELL 13: RESUMEN ---
add_md(r"""---

## 6. Resumen

En esta lección hemos desarrollado el marco matemático y computacional para el **análisis estadístico bidimensional**:

### Puntos Clave:
1. **Distribuciones Bidimensionales:** Se organizan mediante tablas de contingencia $k \times m$ con frecuencias conjuntas $n_{ij}$ y relativas $f_{ij}$.
2. **Marginales y Condicionales:** Las marginales resumen cada variable por separado ($\bar{x}, S_x^2$), mientras que las condicionales ($X|y_j$) capturan la estructura ajustada. Se demostró el Teorema de la Esperanza Total: $\bar{x} = \sum (\bar{x}|y_j) f_{\cdot j}$.
3. **Independencia Estadística:** Exige que $f_{ij} = f_{i\cdot} f_{\cdot j}$ para todos los pares de modalidades.
4. **Asociación en Atributos:** Se cuantifica mediante el Coeficiente Chi-cuadrado ($\chi^2$), el Coeficiente de Contingencia ($C$) y el Coeficiente $\tau$ de Kendall.
5. **Correlación Lineal:** La Covarianza ($S_{XY}$) y el Coeficiente de Pearson ($r_{XY} \in [-1, +1]$) cuantifican la intensidad de la relación lineal. Se demostró que $r_{XY}=0$ no implica independencia (caso $Y=X^2$) y se analizó el peligro de las **correlaciones espurias** generadas por variables confusoras ocultas.
""")

# --- CELL 14: BIBLIOGRAFÍA ---
add_md(r"""---

## 7. Bibliografía

1. **Berenson, M. L., Levine, D. M., & Krehbiel, T. C. (2010).** *Basic Business Statistics: Concepts and Applications.* Pearson International (12th ed.).
2. **Pérez, R., Caso, C., Río, M. J., & López, A. J. (2011).** *Introducción a la Estadística Económica.* Ediciones Pirámide / Universidad de Oviedo.
""")

# Guardar cuaderno en la carpeta leccion-6
target_dir = os.path.join("06-estadistica-1", "leccion-6")
os.makedirs(target_dir, exist_ok=True)
output_path = os.path.join(target_dir, "analisis-conjunto-dos-variables.ipynb")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"=== CUADERNO GENERADO EXITOSAMENTE EN: {output_path} ===")
