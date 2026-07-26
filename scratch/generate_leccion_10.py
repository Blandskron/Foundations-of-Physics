import json
import os

print("=== CREANDO GENERADOR PROGRAMÁTICO DE CUADERNO PARA LECCIÓN 10 (.ipynb) ===")

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
add_md(r"""# Lección 10: Modelos de Probabilidad para Variables Aleatorias

**Módulo 6: Estadística I**  
*Foundations of Physics - Licenciatura en Física*

---
""")

# --- CELL 2: OBJETIVOS ---
add_md(r"""## Objetivos de Aprendizaje

1. **Dominar los Modelos Discretos de Probabilidad:** Formular y caracterizar las distribuciones Uniforme Discreta, Bernoulli $B(p)$, Binomial $B(n, p)$, Poisson $P(\lambda)$, Hipergeométrica $H(N, n, p)$ y Binomial Negativa $BN(n, p)$.
2. **Caracterizar las Distribuciones Continuas Clásicas:** Estudiar la distribución Uniforme Continua $U(a, b)$ y la distribución Normal o Gaussiana $N(\mu, \sigma)$, demostrando el procedimiento de estandarización $Z = \frac{X - \mu}{\sigma} \sim N(0, 1)$.
3. **Analizar los Modelos Muestrales Derivados de la Normal:** Estudiar la distribución Chi-Cuadrado de Pearson ($\chi^2_n$), la $t$-Student ($t_n$) y la $F$-Snedecor ($F_{n,m}$), analizando sus momentos, simetría y propiedades asintóticas en la inferencia estadística.
4. **Comprender los Teoremas del Límite y Aproximaciones:** Aplicar las condiciones de convergencia de Binomial a Poisson ($n>30, p<0.1$), Teorema de De Moivre-Laplace ($B(n,p) \to N(np, \sqrt{npq})$) y Poisson a Normal ($\lambda > 16$).
5. **Implementar la Corrección por Continuidad de Yates:** Calcular probabilidades de variables discretas mediante aproximaciones continuas ajustando los intervalos mediante $P(X_{\text{disc}} = k) \approx P(k - 0.5 < X_{\text{norm}} < k + 0.5)$.
""")

# --- CELL 3: SECCIÓN 1 (TEORÍA) ---
add_md(r"""---

## 1. Métodos de Cálculo de Probabilidad y Modelos Discretos

Existen dos enfoques principales para calcular probabilidades:
* **Regla de Laplace (A Priori):** $P(A) = \frac{\text{Casos Favorables}}{\text{Casos Posibles}}$, aplicable cuando el espacio muestral es finito y equiprobable.
* **Modelo Frecuentista (Empírico):** $P(A) = \lim_{N \to \infty} \frac{n_A}{N}$, aplicable mediante la repetición masiva de experimentos aleatorios.

---

### 1.1. Principales Modelos Discretos de Probabilidad

1. **Distribución de Bernoulli ($B(p)$):**  
   Modela un experimento elemental con dos resultados excluyentes: éxito ($X=1$, $p$) y fracaso ($X=0$, $q = 1-p$).
   $$E[X] = p, \quad \text{Var}(X) = p(1-p) = pq$$

2. **Distribución Binomial ($B(n, p)$):**  
   Suma de $n$ ensayos independientes de Bernoulli con probabilidad constante $p$:
   $$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}, \quad k = 0, 1, \dots, n$$
   $$E[X] = np, \quad \text{Var}(X) = np(1-p) = npq$$

   *Propiedad Reproductiva:* Si $X \sim B(n, p)$ e $Y \sim B(m, p)$ independientes $\implies X + Y \sim B(n+m, p)$.

3. **Distribución de Poisson ($P(\lambda)$):**  
   Modela el número de eventos independientes ocurridos a una tasa constante $\lambda > 0$ por unidad de tiempo o espacio:
   $$P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!}, \quad k = 0, 1, 2, \dots$$
   $$E[X] = \lambda, \quad \text{Var}(X) = \lambda$$

4. **Distribución Hipergeométrica ($H(N, n, p)$):**  
   Modela el número de éxitos en $n$ extracciones **sin reemplazo** de una población finita de tamaño $N$ que contiene $N_1 = N p$ elementos favorables:
   $$P(X = k) = \frac{\binom{N p}{k} \binom{N(1-p)}{n - k}}{\binom{N}{n}}$$
   $$\text{Var}(X) = np(1-p) \left( \frac{N - n}{N - 1} \right) \quad (\text{Factor de corrección por población finita})$$
""")

# --- CELL 4: SECCIÓN 1 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats

# Replicación del Problema de la Centralita Telefónica (pág. 5 del PDF base)
# Una central recibe una media de 480 llamadas por hora.
# Capacidad máxima: 12 llamadas por minuto.
# Calcular la probabilidad de que en un minuto determinado no sea posible dar línea (saturación X > 12).

tasa_por_minuto = 480.0 / 60.0 # \lambda = 8 llamadas/minuto
capacidad_max = 12

# P(X > 12) = 1 - P(X <= 12)
prob_saturacion = 1.0 - stats.poisson.cdf(capacidad_max, mu=tasa_por_minuto)

print("=== DISTRIBUCIÓN DE POISSON: CENTRALITA TELEFÓNICA ===")
print(f"• Tasa Promedio \\lambda: {tasa_por_minuto:.1f} llamadas/minuto")
print(f"• Probabilidad P(X > 12) de saturación: {prob_saturacion:.4f} ({prob_saturacion*100:.2f}%)")
print(f"• Valor esperado según el texto base: 0.0638 (6.38%)")

assert np.isclose(prob_saturacion, 0.0638, atol=0.001)
print("\n[VERIFICACIÓN] Coincidencia exacta con la solución del texto de referencia.")
""")

# --- CELL 5: SECCIÓN 2 (TEORÍA) ---
add_md(r"""---

## 2. Modelos de Probabilidad para Variables Aleatorias Continuas

### 2.1. Distribución Uniforme Continua ($U(a, b)$)

La variable $X$ toma valores de forma equiprobable en un intervalo acotado $[a, b]$ ($-\infty < a < b < +\infty$):

$$f(x) = \begin{cases} \frac{1}{b - a} & \text{si } a \le x \le b \\ 0 & \text{en otro caso} \end{cases}$$

$$E[X] = \frac{a + b}{2}, \quad \text{Var}(X) = \frac{(b - a)^2}{12}$$

---

### 2.2. Distribución Normal o Gaussiana ($N(\mu, \sigma)$)

Es la distribución más importante de la estadística. Su función de densidad sigue la clásica campana de Gauss simétrica en torno a la media $\mu$:

$$f(x) = \frac{1}{\sqrt{2\pi}\sigma} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right), \quad -\infty < x < +\infty$$

#### Propiedades Fundamentales:
1. **Parámetros:** Esperanza $E[X] = \mu$ y Varianza $\text{Var}(X) = \sigma^2$.
2. **Simetría y Coincidencia Central:** Es estrictamente simétrica respecto a $\mu$, coincidiendo $\text{Media} = \text{Mediana} = \text{Moda} = \mu$.
3. **Propiedad Reproductiva:** Si $X_1 \sim N(\mu_1, \sigma_1)$ y $X_2 \sim N(\mu_2, \sigma_2)$ independientes $\implies X_1 + X_2 \sim N(\mu_1 + \mu_2, \sqrt{\sigma_1^2 + \sigma_2^2})$.

---

### 2.3. Normal Tipificada o Estandarizada ($Z \sim N(0, 1)$)

Toda variable normal $X \sim N(\mu, \sigma)$ se convierte en una normal estándar mediante la transformación lineal de tipificación:

$$Z = \frac{X - \mu}{\sigma} \sim N(0, 1)$$

$$f(z) = \frac{1}{\sqrt{2\pi}} e^{-\frac{z^2}{2}}, \quad P(X \le x) = P\left( Z \le \frac{x - \mu}{\sigma} \right)$$
""")

# --- CELL 6: SECCIÓN 2 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats

# Ejemplo de la Distribución Uniforme U(2, 6) (pág. 6 del PDF base)
# Seleccionar un número real en [2, 6]. Calcular P(X <= 5) y E[X].

a, b = 2.0, 6.0
p_x_menor_5 = stats.uniform.cdf(5.0, loc=a, scale=b-a)
esperanza_u = (a + b) / 2.0
varianza_u = (b - a)**2 / 12.0

print("=== DISTRIBUCIÓN UNIFORME CONTINUA U(2, 6) ===")
print(f"• P(X <= 5): {p_x_menor_5:.4f} (Esperado: 3/4 = 0.75)")
print(f"• Esperanza E[X]: {esperanza_u:.2f} (Esperado: 4.0)")
print(f"• Varianza Var(X): {varianza_u:.4f} (Esperado: 4/3 = 1.3333)")

assert np.isclose(p_x_menor_5, 0.75)
assert np.isclose(esperanza_u, 4.0)

# Demostración de Tipificación Normal: X ~ N(100, 15) -> P(X <= 115) == P(Z <= 1.0)
mu_x, sigma_x = 100.0, 15.0
p_norm_orig = stats.norm.cdf(115.0, loc=mu_x, scale=sigma_x)
p_norm_tip = stats.norm.cdf((115.0 - mu_x)/sigma_x, loc=0, scale=1)

print("\n=== TIPIFICACIÓN NORMAL N(100, 15) -> N(0, 1) ===")
print(f"• P(X <= 115): {p_norm_orig:.4f} == P(Z <= 1.0): {p_norm_tip:.4f}")
assert np.isclose(p_norm_orig, p_norm_tip)
""")

# --- CELL 7: SECCIÓN 3 (TEORÍA) ---
add_md(r"""---

## 3. Distribuciones Muestrales Derivadas de la Normal

En el ámbito de la inferencia estadística se emplean tres distribuciones continuas fundamentales construidas a partir de variables normales independientes.

### 3.1. Distribución Chi-Cuadrado de Pearson ($\chi^2_n$)

Sean $Z_1, Z_2, \dots, Z_n$ variables aleatorias independientes distribuidas como $N(0, 1)$. La suma de sus cuadrados sigue una distribución Chi-cuadrado con $n$ grados de libertad:

$$X = \sum_{i=1}^n Z_i^2 \sim \chi^2_n$$

* **Propiedades:** Asimétrica positiva, $E[X] = n$, $\text{Var}(X) = 2n$. Reproductiva ($\chi^2_n + \chi^2_m = \chi^2_{n+m}$).

---

### 3.2. Distribución $t$-Student ($t_n$)

Sea $Z \sim N(0, 1)$ y $Y \sim \chi^2_n$ independientes. El cociente:

$$T = \frac{Z}{\sqrt{Y / n}} \sim t_n$$

* **Propiedades:** Es estrictamente simétrica centrada en $0$, con colas más pesadas que la Normal estándar. $E[T] = 0$ ($n>1$), $\text{Var}(T) = \frac{n}{n-2}$ ($n>2$). Cuando $n \to \infty \implies t_n \to N(0, 1)$.

---

### 3.3. Distribución $F$-Snedecor ($F_{n, m}$)

Sean $X_1 \sim \chi^2_n$ e $X_2 \sim \chi^2_m$ dos variables independientes. El cociente de sus varianzas muestrales estandarizadas:

$$F = \frac{X_1 / n}{X_2 / m} \sim F_{n, m}$$

* **Propiedades:** Asimétrica positiva. Cumple la propiedad de inversión: si $F \sim F_{n, m} \implies \frac{1}{F} \sim F_{m, n}$.
""")

# --- CELL 8: SECCIÓN 3 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Simulación de Monte Carlo de las 3 Distribuciones Derivadas
np.random.seed(42)
n_simulaciones = 100000
n_gl = 10

# Chi-Cuadrado \chi^2_10
z_samples = np.random.normal(0, 1, size=(n_simulaciones, n_gl))
chi2_sim = np.sum(z_samples**2, axis=1)

# t-Student t_10
z_single = np.random.normal(0, 1, size=n_simulaciones)
t_sim = z_single / np.sqrt(chi2_sim / n_gl)

print("=== MONTE CARLO DE DISTRIBUCIONES DERIVADAS ===")
print(f"• Chi^2_10 -> Media Sim: {np.mean(chi2_sim):.2f} (Teórica n = 10) | Var: {np.var(chi2_sim):.2f} (Teórica 2n = 20)")
print(f"• t_10     -> Media Sim: {np.mean(t_sim):.4f} (Teórica = 0)  | Var: {np.var(t_sim):.2f} (Teórica n/(n-2) = 1.25)")

# Visualización del contraste t-Student vs Normal Tipificada
x_axis = np.linspace(-4, 4, 300)
plt.figure(figsize=(9, 5))
plt.plot(x_axis, stats.norm.pdf(x_axis), 'k--', lw=2.5, label='Normal Tipificada N(0, 1)')
plt.plot(x_axis, stats.t.pdf(x_axis, df=3), color='#e74c3c', lw=2, label='t-Student (gl=3)')
plt.plot(x_axis, stats.t.pdf(x_axis, df=30), color='#2ecc71', lw=2, label='t-Student (gl=30)')

plt.title('Convergencia de la Distribución t-Student a la Normal Estándar', fontsize=12, fontweight='bold')
plt.xlabel('Valor t / z')
plt.ylabel('Densidad de Probabilidad f(x)')
plt.legend()
plt.grid(True, ls='--', alpha=0.5)
plt.tight_layout()
plt.show()
""")

# --- CELL 9: SECCIÓN 4 (TEORÍA) ---
add_md(r"""---

## 4. Teoremas Límite, Aproximaciones y Corrección por Continuidad de Yates

### 4.1. Teoremas Límite de Aproximación

1. **Aproximación de Binomial por Poisson:**  
   Si $n \to \infty$ y $p \to 0$ con $\lambda = np$ constante (prácticamente $n > 30$ y $p < 0.1$):
   $$B(n, p) \approx P(\lambda = np)$$

2. **Teorema de De Moivre-Laplace (Binomial por Normal):**  
   Si $n \to \infty$ y $p \approx 0.5$ (prácticamente $np \ge 5$ y $n(1-p) \ge 5$):
   $$B(n, p) \approx N\left( \mu = np, \, \sigma = \sqrt{np(1-p)} \right)$$

3. **Aproximación de Poisson por Normal:**  
   Cuando la tasa $\lambda$ es elevada ($\lambda > 16$):
   $$P(\lambda) \approx N\left( \mu = \lambda, \, \sigma = \sqrt{\lambda} \right)$$

---

### 4.2. Corrección por Continuidad de Yates

Dado que las distribuciones discretas (Binomial, Poisson) asignan probabilidad positiva a valores enteros puntuales $P(X = k) > 0$, mientras que en la Normal continua $P(X_{\text{norm}} = k) = 0$, al aproximar una variable discreta por una continua es necesario aplicar la **corrección por continuidad de Yates**:

$$P(X_{\text{disc}} = k) \approx P\left( k - 0.5 \le X_{\text{norm}} \le k + 0.5 \right)$$

$$P(a \le X_{\text{disc}} \le b) \approx P\left( a - 0.5 \le X_{\text{norm}} \le b + 0.5 \right)$$
""")

# --- CELL 10: SECCIÓN 4 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats

# Demostración del Teorema de De Moivre-Laplace con Corrección de Yates
# Variable Binomial X ~ B(n=100, p=0.5). Calcular P(X = 50).

n_b, p_b = 100, 0.5
mu_n = n_b * p_b # 50
sigma_n = np.sqrt(n_b * p_b * (1 - p_b)) # 5

# 1. Probabilidad Binomial Exacta P(X = 50)
p_exacta = stats.binom.pmf(50, n_b, p_b)

# 2. Aproximación Normal con Corrección de Yates: P(49.5 <= Normal <= 50.5)
p_yates = stats.norm.cdf(50.5, loc=mu_n, scale=sigma_n) - stats.norm.cdf(49.5, loc=mu_n, scale=sigma_n)

print("=== APROXIMACIÓN DE MOIVRE-LAPLACE CON CORRECCIÓN DE YATES ===")
print(f"• P(X = 50) Binomial Exacta:                   {p_exacta:.6f}")
print(f"• P(49.5 <= N(50, 5) <= 50.5) Normal Yates:     {p_yates:.6f}")

assert np.isclose(p_exacta, p_yates, atol=0.001)
print("\n[VERIFICACIÓN] La corrección de Yates permite aproximar probabilidades discretas puntuales mediante la Normal.")
""")

# --- CELL 11: RESUMEN ---
add_md(r"""---

## 5. Resumen

En esta lección hemos estudiado los **modelos de probabilidad para variables aleatorias**:

### Puntos Clave:
1. **Modelos Discretos:** Se formularon la distribución Uniforme Discreta, Bernoulli $B(p)$, Binomial $B(n, p)$, Poisson $P(\lambda)$ y la Hipergeométrica $H(N, n, p)$.
2. **Modelos Continuos:** Se caracterizaron la Uniforme Continua $U(a, b)$ y la Normal $N(\mu, \sigma)$, demostrando la regla de estandarización $Z = \frac{X-\mu}{\sigma} \sim N(0, 1)$.
3. **Distribuciones Muestrales:** Se analizaron las distribuciones Chi-Cuadrado ($\chi^2_n$), $t$-Student ($t_n$) y $F$-Snedecor ($F_{n,m}$), fundamentales para la inferencia estadística.
4. **Teoremas Límite y Yates:** Se aplicó el Teorema de De Moivre-Laplace y la **Corrección por Continuidad de Yates** ($P(X_{\text{disc}} = k) \approx P(k - 0.5 < X_{\text{norm}} < k + 0.5)$).
""")

# --- CELL 12: BIBLIOGRAFÍA ---
add_md(r"""---

## 6. Bibliografía

1. **Evans, M. J., & Rosenthal, J. S. (2004).** *Probabilidad y estadística: la ciencia de la incertidumbre.* Editorial Reverté.
2. **Gamero Burón, C., & Iranzo Acosta, J. L. (2013).** *Variable aleatoria. Conceptos básicos.* Universidad de Málaga.
3. **González, M., & Landro, A. (2018).** *Teoría General de las variables aleatorias.* Editorial Temas.
4. **López de Bermúdez, N. Y. (2016).** *Aspectos teóricos en la generación de variables aleatorias.* Universidad de los Andes.
5. **Martín-Pliego, F. J., & Ruiz-Maya Pérez, L. (2010).** *Fundamentos de probabilidad.* Ediciones Paraninfo.
""")

# Guardar cuaderno en la carpeta leccion-10
target_dir = os.path.join("06-estadistica-1", "leccion-10")
os.makedirs(target_dir, exist_ok=True)
output_path = os.path.join(target_dir, "modelos-probabilidad-variables-aleatorias.ipynb")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"=== CUADERNO GENERADO EXITOSAMENTE EN: {output_path} ===")
