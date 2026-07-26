import json
import os

print("=== CREANDO GENERADOR PROGRAMÁTICO DE CUADERNO PARA LECCIÓN 4 (.ipynb) ===")

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
add_md(r"""# Lección 4: Medidas Resumen de los Datos I (Posición, Dispersión y Forma)

**Módulo 6: Estadística I**  
*Foundations of Physics - Licenciatura en Física*

---
""")

# --- CELL 2: OBJETIVOS ---
add_md(r"""## Objetivos de Aprendizaje

1. **Calcular e interpretar las Medidas de Posición Central:** Estudiar la definición, dominio de aplicación y propiedades de los 6 promedios estadísticos fundamentales: Media Aritmética, Media Ponderada, Mediana, Moda, Media Geométrica y Media Armónica.
2. **Demostrar rigurosamente las propiedades algebraicas de la Media:** Demostrar formalmente la propiedad del centro de gravedad ($\sum (x_i - \bar{x})n_i = 0$), la invariancia o transformación ante cambios de origen y escala, y la descomponibilidad por subpoblaciones.
3. **Calcular e interpretar Medidas de Posición No Central (Cuantiles):** Determinar Cuartiles ($Q_1, Q_2, Q_3$), Deciles ($D_r$) y Percentiles ($P_r$) en distribuciones de datos discretos y agrupados en intervalos mediante interpolación lineal continua.
4. **Construir y analizar Diagramas de Cajas (Boxplots):** Utilizar la representación de Tukey basada en cuantiles y vallas de detección de valores atípicos (*outliers*).
5. **Evaluar la Representatividad de los Promedios mediante Medidas de Dispersión:** Calcular medidas de dispersión absolutas (Rango, Recorrido Intercuartílico, Desviación Absoluta Media, Varianza y Desviación Típica) y relativas (Coeficiente de Variación de Pearson).
6. **Demostrar el Teorema de Mínimos Cuadrados de la Varianza:** Probar numérica y analíticamente que la media cuadrática de las desviaciones se minimiza exactamente cuando la constante de referencia coincide con la media aritmética ($\min_c \frac{1}{N}\sum (x_i - c)^2 \implies c = \bar{x}$).
7. **Estandarizar distribuciones mediante la Variable Tipificada ($Z$-score):** Probar que $Z = \frac{X - \bar{x}}{S_x}$ posee media $\bar{Z}=0$ y varianza $S_Z^2=1$, permitiendo la comparación objetiva de observaciones procedentes de distribuciones con diferentes unidades y escalas.
8. **Caracterizar la Forma de una Distribución:** Estudiar el Coeficiente de Asimetría de Pearson ($A_P$) y el Coeficiente de Curtosis de Fisher ($g_2$), clasificando las distribuciones en simétricas/asimétricas y leptocúrticas/mesocúrticas/platicúrticas.
""")

# --- CELL 3: SECCIÓN 1 (TEORÍA) ---
add_md(r"""---

## 1. Medidas de Posición Central: Promedios

Las **medidas de posición central** o **promedios** son valores numéricos sintéticos alrededor de los cuales se agrupa la masa de observaciones de una distribución.

### 1.1. La Media Aritmética ($\bar{x}$)

Dada una variable estadística $X$ que toma valores $x_1, x_2, \dots, x_k$ con frecuencias absolutas $n_1, n_2, \dots, n_k$ y tamaño total $N = \sum_{i=1}^k n_i$, la **media aritmética** se define como:

$$\bar{x} = \frac{\sum_{i=1}^k x_i n_i}{N} = \sum_{i=1}^k x_i f_i$$

donde $f_i = n_i / N$ representa la frecuencia relativa.

#### Propiedades Algebraicas Fundamentales:

1. **Propiedad del Centro de Gravedad (Suma de desviaciones nula):**
   $$\sum_{i=1}^k (x_i - \bar{x}) n_i = \sum_{i=1}^k x_i n_i - \bar{x} \sum_{i=1}^k n_i = N \bar{x} - \bar{x} N = 0$$
   *Interpretación física:* La media actúa como el centro de masas de la distribución unidimensional.

2. **Cambio de Origen:** Si $X'_i = x_i + c$ para todo $i$, la nueva media es $\bar{x}' = \bar{x} + c$.

3. **Cambio de Escala:** Si $X'_i = c x_i$ para todo $i$, la nueva media es $\bar{x}' = c \bar{x}$.

4. **Descomponibilidad (Media de Subpoblaciones):** Si una población de tamaño $N$ se divide en $p$ subpoblaciones inconexas de tamaños $N_1, N_2, \dots, N_p$ y medias $\bar{x}_1, \bar{x}_2, \dots, \bar{x}_p$, la media global satisface:
   $$\bar{x} = \frac{\sum_{j=1}^p N_j \bar{x}_j}{N}$$

---

### 1.2. La Media Ponderada ($\bar{x}_w$)

Cuando cada observación $x_i$ posee una importancia relativa dada por un peso o ponderación $w_i > 0$:

$$\bar{x}_w = \frac{\sum_{i=1}^k x_i w_i}{\sum_{i=1}^k w_i}$$

---

### 1.3. La Mediana ($Me$)

La **mediana** es el valor numérico que ocupa la posición central de la distribución ordenada, dividiendo a la población en dos partes de igual frecuencia ($50\%$ a la izquierda y $50\%$ a la derecha).

* **Datos sin agrupar:**
  - Si $N$ es impar: Existe una única observación central $Me = x_{\left(\frac{N+1}{2}\right)}$.
  - Si $N$ es par: Se toma el promedio aritmético de las dos observaciones centrales $Me = \frac{x_{\left(\frac{N}{2}\right)} + x_{\left(\frac{N}{2}+1\right)}}{2}$.

* **Datos agrupados en intervalos $[L_{i-1}, L_i)$:**
  Se identifica el intervalo mediano donde la frecuencia acumulada $N_i \ge N/2$. Asumiendo distribución uniforme dentro del intervalo:

  $$Me = L_{i-1} + \frac{\frac{N}{2} - N_{i-1}}{n_i} \cdot a_i$$

  donde $L_{i-1}$ es el límite inferior, $N_{i-1}$ la frecuencia acumulada anterior, $n_i$ la frecuencia absoluta del intervalo y $a_i$ la amplitud del intervalo.

---

### 1.4. La Moda ($Mo$)

La **moda** es el valor de la variable que presenta la mayor frecuencia absoluta. En datos agrupados por intervalos de misma amplitud $a_i = a$:

$$Mo = L_{i-1} + \frac{h_{i+1}}{h_{i-1} + h_{i+1}} \cdot a_i = L_{i-1} + \frac{n_i - n_{i-1}}{(n_i - n_{i-1}) + (n_i - n_{i+1})} \cdot a_i$$

donde $h_i = n_i / a_i$ es la densidad de frecuencia del intervalo modal.

---

### 1.5. Media Geométrica ($G$) y Media Armónica ($H$)

* **Media Geométrica ($G$):** Raíz $N$-ésima del producto de las observaciones. Válida únicamente para datos estrictamente positivos ($x_i > 0$). Ideal para promediar tasas de variación porcentual e índices:
  $$G = \sqrt[N]{\prod_{i=1}^k x_i^{n_i}} = \exp\left( \frac{1}{N}\sum_{i=1}^k n_i \ln(x_i) \right)$$

* **Media Armónica ($H$):** Recíproco de la media aritmética de los recíprocos. Muy sensible a valores pequeños y no definible si existe algún $x_i = 0$:
  $$H = \frac{N}{\sum_{i=1}^k \frac{n_i}{x_i}}$$

#### Desigualdad Clásica de los Promedios:
Para cualquier conjunto de observaciones reales estrictamente positivas:

$$H \le G \le \bar{x}$$

cumpliéndose la igualdad estricta si y solo si todos los valores de la variable son idénticos ($x_1 = x_2 = \dots = x_k$).

---

### 1.6. Ventajas e Inconvenientes de los Promedios

| Promedio | Ventajas Principal | Inconveniente Principal | Recomendación de Uso |
| :--- | :--- | :--- | :--- |
| **Media Aritmética** | Utiliza todos los datos y posee excelentes propiedades algebraicas. | Extremadamente sensible a *outliers* o valores atípicos. | Distribuciones simétricas y homogéneas. |
| **Mediana** | Invariante a valores extremos atípicos (robusta). | No utiliza el valor numérico de todas las observaciones. | Distribuciones fuertemente sesgadas. |
| **Moda** | Aplicable a cualquier tipo de variable (incluso cualitativas). | Puede no ser única (multimodal) o no existir. | Identificación de valores más frecuentes. |
| **Media Geométrica** | Adecuada para magnitudes multiplicativas y tasas acumulativas. | Indefinida para valores nulos o negativos. | Índices financieros, tasas de crecimiento. |
| **Media Armónica** | Promedia ratios unitarios (ej. velocidad $km/h$). | Sensible a valores cercanos a cero. | Promedios de tasas de rendimiento o velocidad. |
""")

# --- CELL 4: SECCIÓN 1 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats

# Configuración de dataset de prueba: Registro de salarios en miles de euros
salarios = np.array([18.5, 20.0, 22.0, 22.0, 25.0, 28.0, 35.0, 42.0, 150.0]) # Incluye un outlier (150k)

# 1. Media Aritmética
m_art = np.mean(salarios)

# 2. Mediana
m_med = np.median(salarios)

# 3. Moda
m_mod = stats.mode(salarios, keepdims=True).mode[0]

# 4. Media Geométrica
m_geo = stats.gmean(salarios)

# 5. Media Armónica
m_arm = stats.hmean(salarios)

print("=== CALCULADORA DE PROMEDIOS ESTADÍSTICOS ===")
print(f"• Media Aritmética:  {m_art:.4f} k€")
print(f"• Mediana (Robusta): {m_med:.4f} k€")
print(f"• Moda:              {m_mod:.4f} k€")
print(f"• Media Geométrica:  {m_geo:.4f} k€")
print(f"• Media Armónica:    {m_arm:.4f} k€")

# Verificación de la Desigualdad H <= G <= Media Aritmética
assert m_arm <= m_geo <= m_art
print("\n[VERIFICACIÓN] Se satisface la Desigualdad H <= G <= Media Aritmética.")

# Demostración numérica de las Propiedades de la Media
# P1: Suma de desviaciones respecto a la media es cero
suma_desv = np.sum(salarios - m_art)
assert np.isclose(suma_desv, 0, atol=1e-10)
print(f"[P1] Suma de desviaciones (Centro de Gravedad): {suma_desv:.5e} == 0")

# P4: Descomponibilidad de subpoblaciones
sub_junior = salarios[:5]
sub_senior = salarios[5:]
media_global_descomp = (len(sub_junior) * np.mean(sub_junior) + len(sub_senior) * np.mean(sub_senior)) / len(salarios)
assert np.isclose(media_global_descomp, m_art, atol=1e-10)
print(f"[P4] Descomponibilidad: Media Global = {media_global_descomp:.4f} == {m_art:.4f}")
""")

# --- CELL 5: SECCIÓN 2 (TEORÍA) ---
add_md(r"""---

## 2. Medidas de Posicionamiento No Central: Cuantiles

Los **cuantiles** son medidas de posición que dividen la distribución de frecuencias acumuladas en partes porcentualmente iguales.

### 2.1. Tipos Principales de Cuantiles

1. **Cuartiles ($Q_r, r=1,2,3$):** Dividen la distribución en 4 partes iguales ($25\%$ cada una).
   - $Q_1$: Primer cuartil ($25\%$ acumulado).
   - $Q_2$: Segundo cuartil ($50\%$ acumulado, coincide exactamente con la Mediana $Me$).
   - $Q_3$: Tercer cuartil ($75\%$ acumulado).

2. **Deciles ($D_r, r=1, \dots, 9$):** Dividen la distribución en 10 partes iguales ($10\%$ cada una).

3. **Percentiles / Centiles ($P_r, r=1, \dots, 99$):** Dividen la distribución en 100 partes iguales ($1\%$ cada una).

### 2.2. Cálculo para Datos Agrupados en Intervalos

Para calcular el cuartil $Q_r$ en datos agrupados por intervalos $[L_{i-1}, L_i)$, se busca el intervalo donde la frecuencia acumulada $N_i \ge \frac{r \cdot N}{4}$:

$$Q_r = L_{i-1} + \frac{\frac{r \cdot N}{4} - N_{i-1}}{n_i} \cdot a_i$$

De forma análoga, para el decil $D_r$ se utiliza $\frac{r \cdot N}{10}$ y para el percentil $P_r$ se utiliza $\frac{r \cdot N}{100}$.

---

### 2.3. Diagrama de Cajas (Boxplot de Tukey)

El **Diagrama de Cajas** es una representación gráfica sintética basada en 5 números resumen:

$$\text{Mínimo Válido}, \; Q_1, \; Me (Q_2), \; Q_3, \; \text{Máximo Válido}$$

#### Detección de Valores Atípicos (Outliers):
El Recorrido Intercuartílico es $RI = Q_3 - Q_1$. Las **vallas de Tukey** definen los límites para observaciones válidas:

$$\text{Valla Inferior} = Q_1 - 1.5 \cdot RI, \quad \text{Valla Superior} = Q_3 + 1.5 \cdot RI$$

Cualquier dato fuera de este intervalo se grafica individualmente como un *outlier*.
""")

# --- CELL 6: SECCIÓN 2 (CÓDIGO) ---
add_code(r"""import numpy as np
import matplotlib.pyplot as plt

# Dataset de ejemplo: Tiempos de procesamiento de servidores en ms
np.random.seed(42)
tiempos_normales = np.random.normal(loc=120, scale=15, size=100)
tiempos_outliers = np.array([210, 225, 240, 30]) # Outliers provocados por latencia de red
datos_tiempos = np.concatenate([tiempos_normales, tiempos_outliers])

# Cálculo de cuantiles principales
q1 = np.percentile(datos_tiempos, 25)
q2 = np.percentile(datos_tiempos, 50)
q3 = np.percentile(datos_tiempos, 75)
iqr = q3 - q1

valla_inf = q1 - 1.5 * iqr
valla_sup = q3 + 1.5 * iqr

outliers_detectados = datos_tiempos[(datos_tiempos < valla_inf) | (datos_tiempos > valla_sup)]

print("=== CÓMPUTO DE CUANTILES Y VALLAS DE TUKEY ===")
print(f"• Primer Cuartil Q1 (25%): {q1:.2f} ms")
print(f"• Mediana Q2 (50%):        {q2:.2f} ms")
print(f"• Tercer Cuartil Q3 (75%): {q3:.2f} ms")
print(f"• Recorrido Intercuartílico IQR: {iqr:.2f} ms")
print(f"• Vallas de Tukey: [{valla_inf:.2f}, {valla_sup:.2f}] ms")
print(f"• Outliers identificados: {outliers_detectados.tolist()}")

# Generación del Diagrama de Cajas (Boxplot)
plt.figure(figsize=(8, 5))
plt.boxplot(datos_tiempos, orientation='vertical', patch_artist=True,
            boxprops=dict(facecolor='#3498db', color='black', alpha=0.7),
            flierprops=dict(marker='o', markerfacecolor='red', markersize=8))

plt.title('Diagrama de Cajas (Boxplot de Tukey) con Detección de Outliers', fontsize=12, fontweight='bold')
plt.ylabel('Tiempo de Procesamiento (ms)', fontsize=10)
plt.grid(True, ls='--', alpha=0.5)
plt.tight_layout()
plt.show()
""")

# --- CELL 7: SECCIÓN 3 (TEORÍA) ---
add_md(r"""---

## 3. Medidas de Dispersión Absoluta y Relativa

Las **medidas de dispersión** cuantifican el grado de separación o variabilidad de las observaciones respecto a una medida de posición central, evaluando la representatividad del promedio.

### 3.1. Medidas de Dispersión Absolutas

1. **Rango o Recorrido ($R$):**
   $$R = \max(x_i) - \min(x_i)$$

2. **Recorrido Intercuartílico ($RI$):**
   $$RI = Q_3 - Q_1$$

3. **Desviación Absoluta Media respecto a la Media ($D_{\bar{x}}$):**
   $$D_{\bar{x}} = \frac{1}{N}\sum_{i=1}^k |x_i - \bar{x}| n_i$$

4. **Varianza ($S_x^2$ o $s^2$):**
   Media de las desviaciones cuadráticas respecto a la media aritmética.
   - Varianza Poblacional ($S_x^2$):
     $$S_x^2 = \frac{1}{N}\sum_{i=1}^k (x_i - \bar{x})^2 n_i = \left( \frac{1}{N}\sum_{i=1}^k x_i^2 n_i \right) - \bar{x}^2$$
   - Varianza Muestral Insesgada ($s^2$):
     $$s^2 = \frac{1}{N-1}\sum_{i=1}^k (x_i - \bar{x})^2 n_i$$

5. **Desviación Típica o Estándar ($S_x$):**
   Raíz cuadrada positiva de la varianza. Viene expresada en las mismas unidades que la variable original:
   $$S_x = +\sqrt{S_x^2}$$

#### Propiedades Cruciales de la Varianza y Desviación Típica:
* **No negatividad:** $S_x^2 \ge 0$.
* **Invariancia ante cambios de origen:** $S_{x+c}^2 = S_x^2$.
* **Escalamiento cuadrático:** $S_{c x}^2 = c^2 S_x^2 \implies S_{c x} = |c| S_x$.
* **Teorema de Minimización de Mínimos Cuadrados:** La función de pérdida cuadrática media $f(c) = \frac{1}{N}\sum_{i=1}^k (x_i - c)^2 n_i$ alcanza su mínimo global estricto única y exclusivamente cuando $c = \bar{x}$.

---

### 3.2. Medidas de Dispersión Relativas: Coeficiente de Variación de Pearson ($V_x$)

Para comparar la variabilidad de dos distribuciones con unidades de medida distintas (ej. peso en $kg$ vs altura en $cm$) o con medias muy distantes, se utiliza una medida adimensional:

$$V_x = \frac{S_x}{|\bar{x}|}$$

* **Propiedad de Invariancia:** $V_x$ es invariant a cambios de escala ($V_{cx} = V_x$), pero varía ante cambios de origen. Un valor $V_x < 0.25$ indica que la media es altamente representativa.
""")

# --- CELL 8: SECCIÓN 3 (CÓDIGO) ---
add_code(r"""import numpy as np
import matplotlib.pyplot as plt

# Dataset de masa de muestras biológicas (en gramos)
masas = np.array([45.2, 48.0, 52.1, 49.5, 50.0, 51.2, 47.8, 53.0, 49.1, 50.5])

# Cómputo de medidas absolutas
rango_val = np.ptp(masas)
q1, q3 = np.percentile(masas, [25, 75])
ri_val = q3 - q1
dev_abs_media = np.mean(np.abs(masas - np.mean(masas)))
var_poblacional = np.var(masas, ddof=0)
std_poblacional = np.std(masas, ddof=0)

# Coeficiente de Variación de Pearson
cv_pearson = std_poblacional / np.mean(masas)

print("=== MEDIDAS DE DISPERSIÓN ABSOLUTA Y RELATIVA ===")
print(f"• Rango (R):                      {rango_val:.2f} g")
print(f"• Recorrido Intercuartílico (RI): {ri_val:.2f} g")
print(f"• Desviación Absoluta Media:     {dev_abs_media:.4f} g")
print(f"• Varianza Poblacional S_x^2:     {var_poblacional:.4f} g²")
print(f"• Desviación Típica S_x:          {std_poblacional:.4f} g")
print(f"• Coeficiente de Variación V_x:   {cv_pearson:.4f} ({cv_pearson*100:.2f}%)")

# Demostración del Teorema de Minimización de Mínimos Cuadrados
c_grid = np.linspace(np.mean(masas) - 5, np.mean(masas) + 5, 200)
ecm_grid = [np.mean((masas - c)**2) for c in c_grid]
c_min = c_grid[np.argmin(ecm_grid)]

print(f"\n[TEOREMA] El mínimo del Error Cuadrático Medio se logra en c = {c_min:.4f} (Media real = {np.mean(masas):.4f})")
assert np.isclose(c_min, np.mean(masas), atol=0.1)

# Visualización de la parábola de error cuadrático
plt.figure(figsize=(8, 4))
plt.plot(c_grid, ecm_grid, color='#e74c3c', lw=2, label=r'$f(c) = \frac{1}{N}\sum (x_i - c)^2$')
plt.axvline(np.mean(masas), color='black', linestyle='--', label=r'Mínimo estricto en $c = \bar{x}$')
plt.title('Teorema de Minimización de Mínimos Cuadrados de la Varianza', fontsize=11, fontweight='bold')
plt.xlabel('Constante $c$', fontsize=10)
plt.ylabel('Suma Cuadrática Media', fontsize=10)
plt.legend()
plt.grid(True, ls='--', alpha=0.5)
plt.tight_layout()
plt.show()
""")

# --- CELL 9: SECCIÓN 4 (TEORÍA) ---
add_md(r"""---

## 4. Variable Tipificada ($Z$-Score)

La **variable tipificada** o **estandarizada** $Z$ expresa la posición relativa de una observación $x_i$ en términos del número de desviaciones típicas que dista de la media aritmética.

### 4.1. Definición Formal

Dada una variable $X$ con media $\bar{x}$ y desviación típica $S_x > 0$:

$$Z = \frac{X - \bar{x}}{S_x}$$

### 4.2. Propiedades de la Variable Tipificada

1. **Media nula:**
   $$E[Z] = \bar{Z} = \frac{E[X - \bar{x}]}{S_x} = \frac{\bar{x} - \bar{x}}{S_x} = 0$$

2. **Varianza unitaria:**
   $$\text{Var}(Z) = S_Z^2 = \frac{\text{Var}(X - \bar{x})}{S_x^2} = \frac{S_x^2}{S_x^2} = 1 \implies S_Z = 1$$

3. **Comparabilidad Multivariada:** Permite comparar puntuaciones de un mismo individuo en distribuciones con medias y dispersiones completamente diferentes (ej. nota de Física $8/10$ vs nota de Matemáticas $75/100$).
""")

# --- CELL 10: SECCIÓN 4 (CÓDIGO) ---
add_code(r"""import numpy as np

# Comparación de desempeño en dos exámenees con escalas diferentes
# Examen 1 (Física): Media = 6.5, Std = 1.2. Nota del estudiante = 8.2
# Examen 2 (Matemáticas): Media = 55, Std = 15. Nota del estudiante = 78

nota_fisica = 8.2
media_fisica, std_fisica = 6.5, 1.2

nota_mates = 78.0
media_mates, std_mates = 55.0, 15.0

# Tipificación (Z-score)
z_fisica = (nota_fisica - media_fisica) / std_fisica
z_mates = (nota_mates - media_mates) / std_mates

print("=== COMPARACIÓN MEDIANTE VARIABLE TIPIFICADA (Z-SCORE) ===")
print(f"• Física:      Nota = {nota_fisica} -> Z-Score = +{z_fisica:.3f} S_x por encima de la media")
print(f"• Matemáticas: Nota = {nota_mates} -> Z-Score = +{z_mates:.3f} S_x por encima de la media")

if z_fisica > z_mates:
    print("-> El rendimiento relativo fue SUPERIOR en Física.")
else:
    print("-> El rendimiento relativo fue SUPERIOR en Matemáticas.")

# Verificación de propiedades Z-score en una muestra
np.random.seed(123)
muestra_x = np.random.normal(loc=100, scale=25, size=1000)
z_muestra = (muestra_x - np.mean(muestra_x)) / np.std(muestra_x, ddof=0)

assert np.isclose(np.mean(z_muestra), 0, atol=1e-10)
assert np.isclose(np.std(z_muestra, ddof=0), 1, atol=1e-10)
print("\n[VERIFICACIÓN] Muestra tipificada cumple estrictamente E[Z]=0 y S_Z=1.")
""")

# --- CELL 11: SECCIÓN 5 (TEORÍA) ---
add_md(r"""---

## 5. Medidas de Forma: Asimetría y Curtosis

Las **medidas de forma** caracterizan la geometría de la distribución de frecuencias sin necesidad de recurrir a la representación gráfica detallada.

### 5.1. Asimetría

La **asimetría** mide el grado de simetría de la distribución respecto a la perpendicular trazada por su centro de gravedad.

* **Coeficiente de Asimetría de Pearson ($A_P$):**
  $$A_P = \frac{\bar{x} - Mo}{S_x}$$

* **Coeficiente de Asimetría de Fisher ($g_1$):**
  $$g_1 = \frac{m_3}{S_x^3} = \frac{\frac{1}{N}\sum_{i=1}^k (x_i - \bar{x})^3 n_i}{S_x^3}$$

#### Clasificación:
- **$A_P = 0$ ($g_1 = 0$):** Distribución **Simétrica** ($\bar{x} = Me = Mo$).
- **$A_P > 0$ ($g_1 > 0$):** Asimetría **Positiva / A la Derecha** (cola más larga hacia valores altos, $\bar{x} > Me > Mo$).
- **$A_P < 0$ ($g_1 < 0$):** Asimetría **Negativa / A la Izquierda** (cola más larga hacia valores bajos, $\bar{x} < Me < Mo$).

---

### 5.2. Curtosis o Apuntamiento

La **curtosis** mide la concentración de frecuencias alrededor del centro respecto a la distribución Normal.

* **Coeficiente de Apuntamiento de Fisher ($g_2$):**
  $$g_2 = \frac{m_4}{S_x^4} - 3 = \frac{\frac{1}{N}\sum_{i=1}^k (x_i - \bar{x})^4 n_i}{S_x^4} - 3$$

#### Clasificación:
- **$g_2 = 0$:** Distribución **Mesocúrtica** (apuntamiento idéntico a la distribución Normal).
- **$g_2 > 0$:** Distribución **Leptocúrtica** (más apuntada y con colas más pesadas que la Normal).
- **$g_2 < 0$:** Distribución **Platicúrtica** (más aplanada que la Normal).
""")

# --- CELL 12: SECCIÓN 5 (CÓDIGO) ---
add_code(r"""import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Generación sintética de distribuciones con diferente asimetría y curtosis
np.random.seed(42)
n_sim = 5000

# 1. Simétrica / Normal (Mesocúrtica)
dist_norm = np.random.normal(loc=0, scale=1, size=n_sim)

# 2. Asimétrica Positiva (Exponencial / Log-normal)
dist_pos = np.random.exponential(scale=1, size=n_sim)

# 3. Asimétrica Negativa (Beta invertida)
dist_neg = -np.random.exponential(scale=1, size=n_sim)

# Cómputo de coeficientes de Fisher
g1_norm, g2_norm = stats.skew(dist_norm), stats.kurtosis(dist_norm, fisher=True)
g1_pos, g2_pos = stats.skew(dist_pos), stats.kurtosis(dist_pos, fisher=True)
g1_neg, g2_neg = stats.skew(dist_neg), stats.kurtosis(dist_neg, fisher=True)

print("=== ANÁLISIS DE FORMA: ASIMETRÍA (g1) Y CURTOSIS (g2) ===")
print(f"• Distribución Normal:     g1 = {g1_norm:+.3f} (Simétrica), g2 = {g2_norm:+.3f} (Mesocúrtica)")
print(f"• Distribución Exponencial: g1 = {g1_pos:+.3f} (Asim. Positiva), g2 = {g2_pos:+.3f} (Leptocúrtica)")
print(f"• Distribución Invertida:   g1 = {g1_neg:+.3f} (Asim. Negativa), g2 = {g2_neg:+.3f} (Leptocúrtica)")

# Visualización comparativa
fig, axs = plt.subplots(1, 3, figsize=(15, 4))

axs[0].hist(dist_neg, bins=40, density=True, color='#e74c3c', alpha=0.7)
axs[0].set_title(f'Asimetría Negativa\n$g_1={g1_neg:.2f}, g_2={g2_neg:.2f}$', fontweight='bold')

axs[1].hist(dist_norm, bins=40, density=True, color='#2ecc71', alpha=0.7)
axs[1].set_title(f'Simétrica / Mesocúrtica\n$g_1={g1_norm:.2f}, g_2={g2_norm:.2f}$', fontweight='bold')

axs[2].hist(dist_pos, bins=40, density=True, color='#3498db', alpha=0.7)
axs[2].set_title(f'Asimetría Positiva\n$g_1={g1_pos:.2f}, g_2={g2_pos:.2f}$', fontweight='bold')

for ax in axs:
    ax.grid(True, ls='--', alpha=0.5)
    ax.set_ylabel('Densidad')

plt.tight_layout()
plt.show()
""")

# --- CELL 13: RESUMEN ---
add_md(r"""---

## 6. Resumen

En esta lección hemos desarrollado el marco matemático y computacional para la caracterización unidimensional de conjuntos de datos mediante medidas resumen:

### Puntos Clave:
1. **Medidas de Posición Central:** Se evaluaron 6 promedios ($\bar{x}, \bar{x}_w, Me, Mo, G, H$), destacando la demostración formal de la propiedad del centro de gravedad ($\sum(x_i-\bar{x})n_i = 0$) y la desigualdad clásica $H \le G \le \bar{x}$.
2. **Cuantiles y Diagrama de Cajas:** Los cuantiles ($Q_r, D_r, P_r$) dividen la distribución acumulada. El Boxplot de Tukey condensa $Q_1, Me, Q_3$ e identifica *outliers* fuera de $[Q_1 - 1.5 IQR, Q_3 + 1.5 IQR]$.
3. **Dispersión y Mínimos Cuadrados:** Se demostró que la varianza satisface el principio de minimización de errores cuadráticos en $c = \bar{x}$. El Coeficiente de Variación de Pearson ($V_x$) proporciona una métrica adimensional de variabilidad relativa.
4. **Variable Tipificada ($Z$-score):** La estandarización $Z = \frac{X-\bar{x}}{S_x}$ garantiza $\bar{Z}=0$ y $S_Z^2=1$, permitiendo la comparación objetiva entre distribuciones disímiles.
5. **Forma:** La geometría funcional queda determinada por la Asimetría de Pearson/Fisher ($g_1$) y la Curtosis de Fisher ($g_2$), clasificando las colas y el apuntamiento.
""")

# --- CELL 14: BIBLIOGRAFÍA ---
add_md(r"""---

## 7. Bibliografía

1. **Berenson, M. L., Levine, D. M., & Krehbiel, T. C. (2010).** *Basic Business Statistics: Concepts and Applications.* Pearson International (12th ed.).
2. **Pérez, R., Caso, C., Río, M. J., & López, A. J. (2011).** *Introducción a la Estadística Económica.* Ediciones Pirámide / Universidad de Oviedo.
""")

# Guardar cuaderno en la carpeta leccion-4
target_dir = os.path.join("06-estadistica-1", "leccion-4")
os.makedirs(target_dir, exist_ok=True)
output_path = os.path.join(target_dir, "medidas-resumen-datos-1.ipynb")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"=== CUADERNO GENERADO EXITOSAMENTE EN: {output_path} ===")
