import json
import os

print("=== CREANDO GENERADOR PROGRAMÁTICO DE CUADERNO PARA LECCIÓN 9 (.ipynb) ===")

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
add_md(r"""# Lección 9: Variables Aleatorias y Funciones de Probabilidad

**Módulo 6: Estadística I**  
*Foundations of Physics - Licenciatura en Física*

---
""")

# --- CELL 2: OBJETIVOS ---
add_md(r"""## Objetivos de Aprendizaje

1. **Definir el Concepto Formal de Variable Aleatoria:** Explicar la variable aleatoria como un mapeo matemático $X: \Omega \to \mathbb{R}$ que asigna un valor numérico real a cada suceso elemental del espacio muestral.
2. **Diferenciar Variables Aleatorias Discretas y Continuas:** Caracterizar las variables discretas (soporte numerable, función de probabilidad de masa $p(x_i)$) y las variables continuas (soporte no numerable, $P(X = x_0) = 0$, función de densidad de probabilidad $f(x)$).
3. **Formular y Calcular Momentos Estadísticos (Media y Varianza):** Obtener la Esperanza Matemática ($\mu = E[X]$), la Varianza ($\sigma^2 = \text{Var}(X) = E[X^2] - \mu^2$) y la Desviación Típica ($\sigma = \sqrt{\text{Var}(X)}$).
4. **Analizar Medidas de Centralización, Posición y Forma:** Evaluar la Moda ($Mo$), la Mediana ($Me$ tal que $F(Me) = 0.5$) y los Cuartiles ($Q_k$) mediante fórmulas analíticas e interpolaciones en datos agrupados.
5. **Construir la Función de Distribución Acumulada $F(x)$:** Definir $F(x) = P(X \le x)$, comprobar sus propiedades (monotonía no decreciente, límites 0 y 1) y calcular probabilidades en subintervalos $P(a < X \le b) = F(b) - F(a)$.
""")

# --- CELL 3: SECCIÓN 1 (TEORÍA) ---
add_md(r"""---

## 1. Concepto y Clasificación de Variables Aleatorias

En los experimentos aleatorios, los resultados pueden ser de naturaleza cualitativa (ej. *Cara/Cruz* en una moneda, *Pieza buena/defectuosa* en un proceso industrial) o cuantitativa (ej. *Número de llamadas*, *Tiempo de fallo*). Para trabajar analíticamente con consecuencias numéricas se define formalmente la **variable aleatoria**.

### 1.1. Definición Matemática

Una **variable aleatoria** $X$ es una aplicación funcional $X: \Omega \to \mathbb{R}$ que asocia a cada suceso elemental $\omega \in \Omega$ de un experimento aleatorio un único número real $X(\omega) \in \mathbb{R}$.

#### Ejemplo Motivador (Lanzamiento de 3 Monedas):
Sea el espacio muestral $\Omega = \{CCC, CCX, CXC, XCC, XCX, XXC, CXX, XXX\}$. Se define la variable aleatoria $X = \text{"Número de Caras obetenidas"}$:
* $X(XXX) = 0 \implies P(X = 0) = P(\{XXX\}) = \frac{1}{8}$
* $X(CXX) = X(XCX) = X(XXC) = 1 \implies P(X = 1) = \frac{3}{8}$
* $X(CCX) = X(CXC) = X(XCC) = 2 \implies P(X = 2) = \frac{3}{8}$
* $X(CCC) = 3 \implies P(X = 3) = \frac{1}{8}$

---

### 1.2. Clasificación: Discretas vs Continuas

1. **Variable Aleatoria Discreta:**
   Toma un número finito o infinito numerable de posibles valores $\{x_1, x_2, \dots, x_n, \dots\}$. La probabilidad se concentra en puntos específicos mediante la **función de probabilidad de masa / cuantía**:
   $$p(x_i) = P(X = x_i), \quad \text{con } p(x_i) \ge 0 \text{ y } \sum_{i} p(x_i) = 1$$

2. **Variable Aleatoria Continua:**
   Toma un número infinito no numerable de valores en uno o varios intervalos continuos de la recta real. Para cualquier valor puntual específico $x_0$, la probabilidad asignada es nula:
   $$P(X = x_0) = 0 \quad \forall x_0 \in \mathbb{R}$$

   La probabilidad sobre un subintervalo $(a, b]$ se calcula integrando su **función de densidad $f(x)$**:
   $$P(a < X \le b) = \int_a^b f(x) \, dx, \quad \text{con } f(x) \ge 0 \text{ y } \int_{-\infty}^\infty f(x) \, dx = 1$$
""")

# --- CELL 4: SECCIÓN 1 (CÓDIGO) ---
add_code(r"""import numpy as np

# Simulación de Monte Carlo del Mapeo de la Variable Aleatoria X = "Número de Caras en 3 Monedas"
np.random.seed(42)
n_simulaciones = 100000

monedas = np.random.choice([0, 1], size=(n_simulaciones, 3)) # 0: Cruz, 1: Cara
x_caras = np.sum(monedas, axis=1)

frecuencias_relativas = [np.mean(x_caras == k) for k in range(4)]
probabilidades_teoricas = [1/8, 3/8, 3/8, 1/8]

print("=== VARIABLE ALEATORIA X: NÚMERO DE CARAS EN 3 MONEDAS ===")
for k in range(4):
    print(f"• P(X = {k}): Empírica = {frecuencias_relativas[k]:.4f} | Teórica = {probabilidades_teoricas[k]:.4f}")
    assert np.isclose(frecuencias_relativas[k], probabilidades_teoricas[k], atol=0.005)

print("\n[VERIFICACIÓN] Las frecuencias empíricas convergen exactamente a la distribución de masa teórica.")
""")

# --- CELL 5: SECCIÓN 2 (TEORÍA) ---
add_md(r"""---

## 2. Medidas y Parámetros de Variables Aleatorias

Los parámetros o momentos estadísticos sintetizan en pocas cifras la posición central, dispersión y forma de la distribución de probabilidad.

### 2.1. Esperanza Matemática (Media $\mu = E[X]$)

Representa el centro de gravedad o valor esperado a largo plazo de la variable aleatoria:

* **Caso Discreto:**
  $$\mu = E[X] = \sum_{i=1}^n x_i P(X = x_i) = \sum_{i=1}^n x_i p_i$$

* **Caso Continuo:**
  $$\mu = E[X] = \int_{-\infty}^\infty x f(x) \, dx$$

#### Sensibilidad a Valores Atípicos:
La esperanza matemática es altamente sensible a observaciones extremas. Por ejemplo, en una serie de valores $\{1, 1, 2, 3, 3, 5, 7, 8, 8\}$, la media es $4.2$; si se añade un valor extremo $50$, la media se desplaza bruscamente a $8.8$.

---

### 2.2. Varianza ($\sigma^2 = \text{Var}(X)$) y Desviación Típica ($\sigma$)

La **varianza** mide el promedio de los cuadrados de las desviaciones respecto a la esperanza matemática:

$$\sigma^2 = \text{Var}(X) = E[(X - \mu)^2] = E[X^2] - \mu^2 = \sum_{i=1}^n x_i^2 p_i - \mu^2$$

La **desviación típica** es la raíz cuadrada positiva de la varianza:

$$\sigma = \sqrt{\text{Var}(X)}$$

---

### 2.3. Medidas de Posición (Moda, Mediana y Cuartiles)

* **Moda ($Mo$):** Valor de la variable que maximiza la función de masa $p(x)$ o la función de densidad $f(x)$.
* **Mediana ($Me$):** Valor que divide la distribución en dos partes de igual probabilidad:
  $$F(Me) = P(X \le Me) = 0.5$$
* **Cuartiles ($Q_k$):** Valores que determinan las frecuencias acumuladas del $25\%$ ($Q_1$), $50\%$ ($Q_2 = Me$) y $75\%$ ($Q_3$). En datos agrupados en intervalos de clase:

  $$Q_k = L_{i-1} + \left( \frac{\frac{k N}{4} - F_{i-1}}{f_i} \right) \cdot C_i$$
""")

# --- CELL 6: SECCIÓN 2 (CÓDIGO) ---
add_code(r"""import numpy as np

class VariableAleatoriaDiscreta:
    # Clase para el cálculo formal de momentos y parámetros de variables aleatorias discretas
    def __init__(self, x_vals, p_vals):
        self.x = np.array(x_vals, dtype=float)
        self.p = np.array(p_vals, dtype=float)
        self.p = self.p / np.sum(self.p) # Normalización
        
    def esperanza(self):
        return np.sum(self.x * self.p)
        
    def varianza(self):
        mu = self.esperanza()
        return np.sum((self.x - mu)**2 * self.p)
        
    def desviacion_tipica(self):
        return np.sqrt(self.varianza())

# Replicación del Ejemplo Empírico de Edades (Tabla 5, pág. 9 del PDF)
edades = [12, 13, 14, 15, 16, 17, 18]
frecuencias_absolutas = [9, 25, 27, 16, 12, 8, 3] # N = 100

va_edades = VariableAleatoriaDiscreta(edades, np.array(frecuencias_absolutas)/100.0)

mu_edades = va_edades.esperanza()
var_edades = va_edades.varianza()
sigma_edades = va_edades.desviacion_tipica()

print("=== EJEMPLO DE EDADES (TABLA 5 DEL TEXTO BASE) ===")
print(f"• Esperanza E[X]:       {mu_edades:.2f} años (PDF: 14.33)")
print(f"• Varianza Var(X):       {var_edades:.4f} (PDF: 2.34)")
print(f"• Desviación Típica sigma: {sigma_edades:.2f} años (PDF: 1.53)")

assert np.isclose(mu_edades, 14.33, atol=0.01)
assert np.isclose(sigma_edades, 1.53, atol=0.01)
print("\n[VERIFICACIÓN] Coincidencia exacta con la solución del texto de referencia.")
""")

# --- CELL 7: SECCIÓN 3 (TEORÍA) ---
add_md(r"""---

## 3. Función de Probabilidad y Función de Distribución Acumulada $F(x)$

### 3.1. Función de Probabilidad de Masa ($p(x)$)

Para una variable aleatoria discreta $X$, la **función de probabilidad de masa** asigna a cada punto $x_i$ su probabilidad exacta:

$$p(x_i) = P(X = x_i)$$

#### Ejemplo (Dado Asimétrico - Tabla 6 del texto base):
Un dado tiene tres caras marcadas con el número 6, dos caras marcadas con el número 5 y una cara marcada con el número 1:
* $P(X = 1) = \frac{1}{6}$
* $P(X = 5) = \frac{2}{6}$
* $P(X = 6) = \frac{3}{6}$

---

### 3.2. Función de Distribución Acumulada ($F(x)$)

La **función de distribución acumulada** $F(x)$ se define para cualquier variable aleatoria (discreta o continua) como la probabilidad de que $X$ tome valores menores o iguales a $x$:

$$F(x) = P(X \le x) = \sum_{x_i \le x} p(x_i)$$

#### Propiedades Fundamentales de $F(x)$:
1. **Acotamiento:** $0 \le F(x) \le 1, \quad \forall x \in \mathbb{R}$.
2. **Monotonía:** $F(x)$ es una función monótona no decreciente (si $a \le b \implies F(a) \le F(b)$).
3. **Límites Infinitos:**
   $$\lim_{x \to -\infty} F(x) = 0, \quad \lim_{x \to +\infty} F(x) = 1$$
4. **Cómputo de Probabilidades por Intervalos:**
   $$P(a < X \le b) = F(b) - F(a)$$
""")

# --- CELL 8: SECCIÓN 3 (CÓDIGO) ---
add_code(r"""import numpy as np
import matplotlib.pyplot as plt

# Replicación del Dado Asimétrico (Tabla 6, pág. 9)
x_dado = np.array([1, 5, 6])
p_dado = np.array([1/6, 2/6, 3/6])

def funcion_acumulada_dado(val):
    return np.sum(p_dado[x_dado <= val])

# Evaluación de F(x) en la recta real
grid_x = np.linspace(0, 8, 400)
grid_F = [funcion_acumulada_dado(val) for val in grid_x]

# Representación Gráfica de la Función de Distribución Acumulada Escalonada F(x)
plt.figure(figsize=(9, 5))
plt.step(grid_x, grid_F, where='post', color='#e74c3c', lw=2.5, label='F(x) = P(X <= x)')
plt.scatter(x_dado, np.cumsum(p_dado), color='#e74c3c', s=50, zorder=4)

plt.title('Función de Distribución Acumulada Escalonada F(x) (Dado Asimétrico)', fontsize=12, fontweight='bold')
plt.xlabel('Valor de x')
plt.ylabel('Probabilidad Acumulada F(x)')
plt.ylim(-0.05, 1.05)
plt.grid(True, ls='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
""")

# --- CELL 9: RESUMEN ---
add_md(r"""---

## 4. Resumen

En esta lección hemos desarrollado la teoría formal de las **variables aleatorias** y sus **funciones de probabilidad**:

### Puntos Clave:
1. **Definición de Variable Aleatoria:** Mapeo formal $X: \Omega \to \mathbb{R}$ que traduce sucesos cualitativos en valores numéricos.
2. **Discretas vs Continuas:** Las v.a. discretas se caracterizan por su función de masa $p(x_i)$, mientras que las continuas se rigen por la función de densidad $f(x)$ con $P(X = x_0) = 0$.
3. **Momentos Estadísticos:** Se formularon la Esperanza Matemática ($\mu = E[X]$) y la Varianza ($\sigma^2 = E[X^2] - \mu^2$), analizando su sensibilidad ante valores atípicos.
4. **Función de Distribución Acumulada ($F(x)$):** Definida como $F(x) = P(X \le x)$, permite evaluar probabilidades en subintervalos mediante $P(a < X \le b) = F(b) - F(a)$.
""")

# --- CELL 10: BIBLIOGRAFÍA ---
add_md(r"""---

## 5. Bibliografía

1. **Gamero Burón, C., & Iranzo Acosta, J. L. (2013).** *Variable aleatoria. Conceptos básicos.* Universidad de Málaga.
2. **González, M., & Landro, A. (2018).** *Teoría General de las variables aleatorias.* Editorial Temas.
3. **López de Bermúdez, N. Y. (2016).** *Aspectos teóricos en la generación de variables aleatorias.* Universidad de los Andes.
4. **Ross, S. M. (2007).** *Introducción a la estadística.* Editorial Reverté.
""")

# Guardar cuaderno en la carpeta leccion-9
target_dir = os.path.join("06-estadistica-1", "leccion-9")
os.makedirs(target_dir, exist_ok=True)
output_path = os.path.join(target_dir, "variables-aleatorias-funciones-probabilidad.ipynb")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"=== CUADERNO GENERADO EXITOSAMENTE EN: {output_path} ===")
