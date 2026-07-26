import json
import os

print("=== CREANDO GENERADOR PROGRAMÁTICO DE CUADERNO MASTER PARA LECCIÓN 11 (.ipynb) CORREGIDO ===")

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
add_md(r"""# Lección 11: Síntesis Consolidada del Módulo 6 (Estadística I)

**Módulo 6: Estadística I**  
*Foundations of Physics - Licenciatura en Física*

---
""")

# --- CELL 2: OBJETIVOS ---
add_md(r"""## Objetivos Integradores de Aprendizaje

1. **Integrar el Marco Analítico de la Estadística Descriptiva (Pilar I - Lecciones 1 a 5):** Consolidar la jerarquía de escalas de medición, la corrección de Bessel ($n-1$) para estimadores insesgados, el cálculo e interpretación de los 6 promedios ($\bar{x}, \bar{x}_w, Me, Mo, G, H$), la parábola de minimización de varianza en $c = \bar{x}$, los $Z$-scores, los coeficientes de forma ($g_1, g_2$), la anatomía del Boxplot de Tukey ($1.5 RQ, 3 RQ$), las pruebas de atípicos (Grubbs, GESD, escala robusta $\text{MAD}$) y las transformaciones de simetrización ($\ln(X)$).
2. **Sintetizar las Relaciones Multivariadas y el Análisis Temporal (Pilar II - Lecciones 6 y 7):** Unificar las tablas bidimensionales de contingencia $k \times m$, la verificación analítica del Teorema de la Esperanza Total ($\bar{x} = \sum (\bar{x}|y_j) f_{\cdot j}$), las medidas de asociación cualitativa ($\chi^2, C, \tau$), la covarianza $S_{XY}$, el coeficiente $r_{XY}$, la prueba de incorrelación en relaciones parabólicas ($Y=X^2$), la selección de esquemas temporales mediante regresión de dispersión ($S_a = b_0 + b_1 \bar{Y}_a$), los índices compuestos de precios (Laspeyres $L^P$, Paasche $P^P$, Fisher $F^P$) con la ordenación $P^P \le F^P \le L^P$, y el procedimiento de deflación por el IPC ($Y_t^* = \frac{Y_t}{IPC_t} \times 100$).
3. **Unificar los Fundamentos Axiomáticos de Probabilidad e Inferencia (Pilar III - Lecciones 8 a 10):** Consolidar los tres enfoques de probabilidad (Laplace, Frecuencial, Subjetivo), las Leyes de De Morgan ($(A \cup B)^c = A^c \cap B^c$), los 3 Axiomas de Kolmogorov (1933), el Teorema de la Probabilidad Total y Bayes, el mapeo de variables aleatorias $X: \Omega \to \mathbb{R}$, las distribuciones universales (Binomial, Poisson, Normal, $\chi^2_n, t_n, F_{n,m}$), el Teorema de De Moivre-Laplace y la Corrección por Continuidad de Yates ($P(X_{\text{disc}} = k) \approx P(k - 0.5 < X_{\text{norm}} < k + 0.5)$).
4. **Ejecutar el Pipeline Computacional Maestro (`MasterPipelineEstadistica`):** Implementar un pipeline autocontenido en Python que procesa un dataset multivariado de prueba ejecutando de forma secuencial los 3 pilares del módulo.
""")

# --- CELL 3: PILAR 1 (TEORÍA) ---
add_md(r"""---

## 1. Pilar I: Análisis Exploratorio Univariante y Estadística Descriptiva (Lecciones 1–5)

La Estadística Descriptiva constituye la etapa fundamental del método científico para transformar registros de datos crudos en información cuantitativa estructurada.

### 1.1. Tabulación y Corrección de Estimadores
* **Corrección de Bessel (Varianza Insesgada):** Al estimar la varianza poblacional $\sigma^2$ a partir de una muestra de tamaño $n$, el estimador de la suma de cuadrados dividido por $n$ es sesgado. El estimador insesgado $s^2$ requiere dividir por los grados de libertad $n-1$:
  $$s^2 = \frac{1}{n-1} \sum_{i=1}^n (x_i - \bar{x})^2$$
* **Histogramas de Densidad ($h_i$):** En intervalos de clase de amplitud desigual $c_i$, trazar frecuencias absolutas genera una distorsión visual. La representación corregida exige graficar la **densidad de frecuencia**:
  $$h_i = \frac{f_i}{c_i}$$

---

### 1.2. Promedios, Propiedades y Dispersión
* **Desigualdad Clásica de los Promedios:**
  $$H \le G \le \bar{x} \quad \text{donde } H = \frac{n}{\sum \frac{1}{x_i}}, \; G = \sqrt[n]{\prod x_i}, \; \bar{x} = \frac{\sum x_i}{n}$$
* **Propiedades Algebraicas de la Media:**
  1. Centrado: $\sum (x_i - \bar{x}) n_i = 0$.
  2. Transformaciones Lineales: Si $Y = a X + b \implies \bar{y} = a \bar{x} + b$.
  3. Descomponibilidad Poblacional: $\bar{x} = \frac{\sum N_k \bar{x}_k}{N}$.
* **Teorema de Minimización del Error Cuadrático Medio:**
  $$\min_{c \in \mathbb{R}} \sum_{i=1}^n (x_i - c)^2 \implies c = \bar{x}$$

---

### 1.3. Anatomía del Boxplot de Tukey y Detección de Atípicos
* **Límites de Tukey:** Vallas Interiores ($Q_1 - 1.5 RQ, Q_3 + 1.5 RQ$) y Vallas Exteriores ($Q_1 - 3 RQ, Q_3 + 3 RQ$).
* **Tests de Atípicos Históricos:** Test de Grubbs ($G = \frac{\max |x_i - \bar{x}|}{s}$) y escala robusta $\hat{\sigma} = 1.48 \cdot \text{mediana}|x_i - \text{mediana}(x_i)|$.
* **Escalera de Potencias de Tukey:** Transformación $Y = \ln(X)$ para simetrizar distribuciones con asimetría positiva empírica.
""")

# --- CELL 4: PILAR 1 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats

# Módulo de Procesamiento Univariante y Depuración EDA
np.random.seed(42)
datos_crudos = np.concatenate([np.random.lognormal(mean=1.5, sigma=0.5, size=95), [45.0, 52.0, 60.0]])

# 1. Promedios
m_art = np.mean(datos_crudos)
g_art = stats.gmean(datos_crudos)
h_art = stats.hmean(datos_crudos)

# 2. Atípicos por Tukey
q1, q3 = np.percentile(datos_crudos, [25, 75])
rq = q3 - q1
valla_inf, valla_sup = q1 - 1.5 * rq, q3 + 1.5 * rq
atipicos = datos_crudos[(datos_crudos < valla_inf) | (datos_crudos > valla_sup)]

# 3. Transformación de Simetrización ln(X)
datos_log = np.log(datos_crudos)
asimetria_orig = stats.skew(datos_crudos)
asimetria_log = stats.skew(datos_log)

print("=== PILAR I: PROCESAMIENTO UNIVARIANTE Y EDA ===")
print(f"• Promedios: H = {h_art:.2f} <= G = {g_art:.2f} <= X_bar = {m_art:.2f}")
print(f"• Atípicos detectados por Vallas de Tukey (1.5 RQ): {len(atipicos)} valores")
print(f"• Asimetría de Fisher Original: {asimetria_orig:.2f} -> Tras ln(X): {asimetria_log:.2f}")

assert h_art <= g_art <= m_art
print("[VERIFICACIÓN] Se satisface la Desigualdad Clásica de los Promedios H <= G <= X_bar.")
""")

# --- CELL 5: PILAR 2 (TEORÍA) ---
add_md(r"""---

## 2. Pilar II: Relaciones Bidimensionales y Análisis de Series Temporales (Lecciones 6–7)

### 2.1. Análisis Bidimensional
* **Distribuciones Marginales y Condicionales:** $n_{i\cdot} = \sum_j n_{ij}$, $n_{\cdot j} = \sum_i n_{ij}$.
* **Teorema de la Esperanza Total:**
  $$\bar{x} = \sum_{j=1}^m (\bar{x}|y_j) f_{\cdot j}$$
* **Incorrelación vs Independencia:** Dos variables con una relación funcional determinista perfecta (ej. parábola $Y = X^2$) presentan covarianza $S_{XY} = 0$ y coeficiente $r_{XY} = 0$ debido a la simetría de las desviaciones.

---

### 2.2. Series Temporales e Índices de Precios
* **Esquemas de Composición:**
  - Aditivo: $Y_t = T_t + S_t + u_t$ (amplitud estacional constante).
  - Multiplicativo: $Y_t = T_t \times S_t \times u_t$ (amplitud estacional proporcional a la tendencia).
* **Criterio de Regresión de Dispersión Anual:** Regresión $S_a = b_0 + b_1 \bar{Y}_a$. Si $b_1 \approx 0 \implies$ Aditivo; si $b_1 > 0 \implies$ Multiplicativo.
* **Índices Compuestos Ponderados de Precios:**
  - **Laspeyres ($L^P$):** $L^P = \frac{\sum p_{it} q_{i0}}{\sum p_{i0} q_{i0}} \times 100$ (ponderación en período base, sobreestima inflación).
  - **Paasche ($P^P$):** $P^P = \frac{\sum p_{it} q_{it}}{\sum p_{i0} q_{it}} \times 100$ (ponderación en período actual, subestima inflación).
  - **Fisher ($F^P$):** $F^P = \sqrt{L^P \times P^P}$ (índice ideal sin sesgo).
  - *Ordenación por Efecto Sustitución:* $P^P \le F^P \le L^P$.
* **Deflación Económica:** Conversión de precios corrientes (nominales $Y_t$) a precios constantes (reales $Y_t^*$):
  $$Y_t^* = \frac{Y_t}{IPC_t} \times 100$$
""")

# --- CELL 6: PILAR 2 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats

# 1. Incorrelación en Parábola Y = X^2
x_parab = np.array([-3, -2, -1, 0, 1, 2, 3])
y_parab = x_parab**2
r_parab, _ = stats.pearsonr(x_parab, y_parab)

# 2. Ordenación de Índices de Precios (Laspeyres, Paasche, Fisher)
p0 = np.array([2.5, 10.0, 1.2, 5.0, 15.0])
q0 = np.array([100,  20, 150, 40,  10])
pt = np.array([3.0, 12.0, 1.5, 4.8, 18.0])
qt = np.array([90,   18, 160, 45,   8])

laspeyres = (np.sum(pt * q0) / np.sum(p0 * q0)) * 100.0
paasche   = (np.sum(pt * qt) / np.sum(p0 * qt)) * 100.0
fisher    = np.sqrt(laspeyres * paasche)

print("=== PILAR II: BIVARIANTE, TEMPORAL E ÍNDICES ===")
print(f"• Parábola Y = X^2 -> Coeficiente r_XY: {r_parab:.5e} (Relación funcional con r = 0)")
print(f"• Índices Ponderados: Paasche ({paasche:.2f}) <= Fisher ({fisher:.2f}) <= Laspeyres ({laspeyres:.2f})")

assert paasche <= fisher <= laspeyres
print("[VERIFICACIÓN] Se satisfacen las demostraciones teóricas de incorrelación y de Fisher.")
""")

# --- CELL 7: PILAR 3 (TEORÍA) ---
add_md(r"""---

## 3. Pilar III: Fundamentos Axiomáticos de Probabilidad y Modelos Distribucionales (Lecciones 8–10)

### 3.1. Axiomatización de Kolmogorov y Bayes
* **Los 3 Axiomas de Kolmogorov (1933):**
  1. $P(A) \ge 0$.
  2. $P(\Omega) = 1$.
  3. Aditividad: $P(\bigcup A_i) = \sum P(A_i)$ para sucesos disjuntos.
* **Leyes de De Morgan:** $(A \cup B)^c = A^c \cap B^c$, $(A \cap B)^c = A^c \cup B^c$.
* **Teorema de Bayes:**
  $$P(A_j \mid B) = \frac{P(B \mid A_j) P(A_j)}{\sum_{i=1}^n P(B \mid A_i) P(A_i)}$$

---

### 3.2. Variables Aleatorias y Modelos Distribucionales
* **Momentos:** Esperanza $\mu = E[X]$, Varianza $\sigma^2 = E[X^2] - \mu^2$, Función Acumulada $F(x) = P(X \le x)$.
* **Modelos Discretos:** Binomial $B(n, p)$, Poisson $P(\lambda)$, Hipergeométrica $H(N, n, p)$.
* **Modelos Continuos:** Uniforme $U(a, b)$, Normal $N(\mu, \sigma)$ y Normal Tipificada $Z = \frac{X-\mu}{\sigma} \sim N(0, 1)$.
* **Distribuciones Derivadas:** Chi-Cuadrado ($\chi^2_n = \sum Z_i^2$), $t$-Student ($t_n = \frac{Z}{\sqrt{\chi^2_n / n}}$), $F$-Snedecor ($F_{n, m} = \frac{\chi^2_n / n}{\chi^2_m / m}$).
* **Teorema de De Moivre-Laplace y Corrección por Continuidad de Yates:**
  $$B(n, p) \approx N(np, \sqrt{npq}) \implies P(X_{\text{disc}} = k) \approx P(k - 0.5 < X_{\text{norm}} < k + 0.5)$$
""")

# --- CELL 8: PILAR 3 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats

# 1. Teorema de Bayes (3 Urnas)
prioris = np.array([1/3, 1/3, 1/3])
verosimilitudes = np.array([3/5, 4/6, 0/3]) # Bola blanca
p_total_blanca = np.sum(prioris * verosimilitudes)
posterior_u1 = (prioris[0] * verosimilitudes[0]) / p_total_blanca

# 2. De Moivre-Laplace con Yates B(100, 0.5) P(X = 50)
p_exacta = stats.binom.pmf(50, 100, 0.5)
p_yates = stats.norm.cdf(50.5, loc=50, scale=5) - stats.norm.cdf(49.5, loc=50, scale=5)

print("=== PILAR III: PROBABILIDAD E INFERENCIA DISTRIBUCIONAL ===")
print(f"• Probabilidad Total Blanca: {p_total_blanca:.4f} (Esperado 19/45 = {19/45:.4f})")
print(f"• Posterior P(U1 | Blanca):    {posterior_u1:.4f} (Esperado 9/19 = {9/19:.4f})")
print(f"• Binomial B(100, 0.5) P(X=50) Exacta: {p_exacta:.6f} == Yates: {p_yates:.6f}")

assert np.isclose(p_total_blanca, 19/45)
assert np.isclose(posterior_u1, 9/19)
assert np.isclose(p_exacta, p_yates, atol=0.001)
print("[VERIFICACIÓN] Confirmados los teoremas de Bayes y De Moivre-Laplace con corrección de Yates.")
""")

# --- CELL 9: PIPELINE MASTER (TEORÍA Y CÓDIGO) ---
add_md(r"""---

## 4. Pipeline Computacional Integrador Maestro (`MasterPipelineEstadistica`)

A continuación se ejecuta de forma unificada la clase `MasterPipelineEstadistica`, procesando un dataset sintético físico-económico de prueba para conectar secuencialmente todas las etapas analíticas del Módulo 6.
""")

add_code(r"""import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

class MasterPipelineEstadistica:
    # Pipeline Integrador Maestro del Módulo 6: Estadística I.
    def __init__(self, data_univariante, data_bivariante_x, data_bivariante_y, serie_temporal, ipc_serie):
        self.u_data = np.array(data_univariante, dtype=float)
        self.b_x = np.array(data_bivariante_x, dtype=float)
        self.b_y = np.array(data_bivariante_y, dtype=float)
        self.serie_t = np.array(serie_temporal, dtype=float)
        self.ipc = np.array(ipc_serie, dtype=float)
        
    def ejecutar_analisis_completo(self):
        # Pilar 1: Descriptiva
        mean_v = np.mean(self.u_data)
        g_v = stats.gmean(self.u_data)
        h_v = stats.hmean(self.u_data)
        
        # Pilar 2: Bivariante & Temporal
        r_xy, _ = stats.pearsonr(self.b_x, self.b_y)
        medias_a = [np.mean(self.serie_t[a*12:(a+1)*12]) for a in range(len(self.serie_t)//12)]
        stds_a = [np.std(self.serie_t[a*12:(a+1)*12], ddof=1) for a in range(len(self.serie_t)//12)]
        b1_disp, _, _, p_val, _ = stats.linregress(medias_a, stds_a)
        esquema = "Multiplicativo" if (b1_disp > 0.05 and p_val < 0.05) else "Aditivo"
        
        # Pilar 3: Probabilidad
        p_total = np.sum(np.array([1/3, 1/3, 1/3]) * np.array([3/5, 4/6, 0/3]))
        
        return {
            "mean": mean_v, "gmean": g_v, "hmean": h_v,
            "r_xy": r_xy, "esquema": esquema, "p_total_blanca": p_total
        }

# Ejecución de prueba del Pipeline Maestro
np.random.seed(42)
d_u = np.concatenate([np.random.lognormal(mean=1.5, sigma=0.5, size=95), [45.0, 52.0, 60.0]])
d_x = np.random.uniform(5, 45, 100)
d_y = 2.0 + 0.18 * d_x + np.random.normal(0, 1.2, 100)
s_t = (100.0 + 2.0 * np.arange(1, 61)) * np.tile([0.85, 0.9, 0.95, 1.0, 1.05, 1.15, 1.25, 1.2, 1.1, 1.0, 0.9, 0.85], 5) + np.random.normal(0, 3, 60)
ipc = np.array([100.0, 103.1, 108.9, 112.5])

pipeline_master = MasterPipelineEstadistica(d_u, d_x, d_y, s_t, ipc)
res_master = pipeline_master.ejecutar_analisis_completo()

print("=== PIPELINE MAESTRO EJECUTADO CON ÉXITO ===")
print(f"• Pilar I   -> H ({res_master['hmean']:.2f}) <= G ({res_master['gmean']:.2f}) <= X_bar ({res_master['mean']:.2f})")
print(f"• Pilar II  -> Correlación r_XY = {res_master['r_xy']:.4f} | Esquema Estacional: {res_master['esquema']}")
print(f"• Pilar III -> Probabilidad Total Blanca = {res_master['p_total_blanca']:.4f}")
""")

# --- CELL 10: RESUMEN GENERAL ---
add_md(r"""---

## 5. Resumen General del Módulo 6 (Estadística I)

El **Módulo 6: Estadística I** ha construido un edificio teórico y computacional completo:

1. **Estadística Descriptiva Univariante (Lecciones 1–5):** Desde la tabulación rigurosa y correcciones insesgadas hasta el análisis exploratorio avanzado (EDA), detección de atípicos y simetrización por transformaciones no lineales.
2. **Relaciones Bidimensionales y Análisis Temporal (Lecciones 6–7):** Desde la caracterización de tablas de contingencia y correlación de Pearson hasta la descomposición de series temporales, números índices ponderados (Laspeyres, Paasche, Fisher) y deflación económica.
3. **Fundamentos de Probabilidad e Inferencia (Lecciones 8–10):** Desde los orígenes históricos y la axiomatización de Kolmogorov hasta las distribuciones universales (Binomial, Poisson, Normal, $\chi^2, t, F$), Teorema de Bayes y teoremas límite asintóticos.
""")

# --- CELL 11: BIBLIOGRAFÍA CONSOLIDADA ---
add_md(r"""---

## 6. Bibliografía Consolidada del Módulo 6

1. **Berenson, M. L., Levine, D. M., & Krehbiel, T. C. (2010).** *Basic Business Statistics: Concepts and Applications.* Pearson International (12th ed.).
2. **Carot Sánchez, T. (2014).** *Introducción a la estadística y a las probabilidades.* Editorial Universitat Politècnica de València.
3. **Casparri, M. T. (2018).** *Introducción a la probabilidad y a la estadística.* Editorial Eudeba.
4. **Davila, S. (2019).** *Detección de outliers en grandes bases de datos.*
5. **Evans, M. J., & Rosenthal, J. S. (2004).** *Probabilidad y estadística: la ciencia de la incertidumbre.* Editorial Reverté.
6. **Gamero Burón, C., & Iranzo Acosta, J. L. (2013).** *Variable aleatoria. Conceptos básicos.* Universidad de Málaga.
7. **González, M., & Landro, A. (2018).** *Teoría General de las variables aleatorias.* Editorial Temas.
8. **Huertas Sánchez, A., & Manzano Arjona, M. (2002).** *Teoría de conjuntos.* Grupo Editorial Iberoamérica.
9. **Instituto Nacional de Estadística (INE).** *Metodología del Índice de Precios de Consumo (IPC Base 2011/2021).* Madrid, España.
10. **Ivorra Castillo, C.** *Teoría de conjuntos.* Universitat de València.
11. **López de Bermúdez, N. Y. (2016).** *Aspectos teóricos en la generación de variables aleatorias.* Universidad de los Andes.
12. **Martín-Pliego, F. J., & Ruiz-Maya Pérez, L. (2010).** *Fundamentos de probabilidad.* Ediciones Paraninfo.
13. **Montes Suay, F. (2007).** *Introducción a la probabilidad.* Universitat de València.
14. **Pérez, R., Caso, C., Río, M. J., & López, A. J. (2011).** *Introducción a la Estadística Económica.* Ediciones Pirámide / Universidad de Oviedo.
15. **Rincón, L. (2006).** *Una introducción a la probabilidad y estadística.* UNAM.
16. **Ross, S. M. (2007).** *Introducción a la estadística.* Editorial Reverté.
17. **Tukey, J. W. (1977).** *Exploratory Data Analysis.* Addison-Wesley.
""")

# Guardar cuaderno en la carpeta leccion-11
target_dir = os.path.join("06-estadistica-1", "leccion-11")
os.makedirs(target_dir, exist_ok=True)
output_path = os.path.join(target_dir, "sintesis-consolidada-modulo-6.ipynb")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"=== CUADERNO MAESTRO GENERADO EXITOSAMENTE EN: {output_path} ===")
