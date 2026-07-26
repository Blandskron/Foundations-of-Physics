import json
import os

# Asegurar que existe la carpeta destino
output_dir = r"c:\Users\BlandskronNotebook\Documents\blandskron\licenciatura-en-fisica\06-estadistica-1\leccion-1"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "introduccion-a-la-estadistica.ipynb")

notebook = {
  "cells": [],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.10.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 2
}

def add_markdown(source_list):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source_list]
    })

def add_code(source_list):
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source_list]
    })

# --- CELL 1: HEADER ---
add_markdown([
    "# Lección 1: Introducción a la Estadística",
    "### Módulo 6: Estadística I",
    "",
    "---",
    "",
    "La estadística es una de las herramientas más poderosas del método científico. En las ciencias físicas y naturales, donde la variabilidad experimental y la incertidumbre en las mediciones son inevitables, la estadística nos permite pasar del dato crudo a la formulación de leyes y a la validación de hipótesis teóricas.",
    "",
    "En esta lección introductoria, exploraremos los **conceptos fundamentales** de la estadística, su evolución histórica y las etapas metodológicas de un estudio estadístico. Además, utilizaremos simulaciones en Python para ilustrar empíricamente conceptos abstractos pero fundamentales: cómo una muestra representa a una población (la Ley de los Grandes Números) y por qué la varianza muestral requiere una corrección matemática específica (la **corrección de Bessel**) para ser un estimador insesgado.",
    "",
    "---"
])

# --- CELL 2: OBJECTIVES ---
add_markdown([
    "## Objetivos de Aprendizaje",
    "",
    "Al finalizar esta lección, serás capaz de:",
    "1. **Describir** la evolución histórica de la estadística y sus principales hitos teóricos (de los censos antiguos a Fisher).",
    "2. **Identificar** las etapas metodológicas de un estudio estadístico completo.",
    "3. **Diferenciar** con rigor entre población, muestra representativa, individuo, parámetro y estadístico.",
    "4. **Clasificar** variables estadísticas según su nivel de medición (nominal, ordinal, intervalo, razón) y su naturaleza (cualitativas y cuantitativas).",
    "5. **Demostrar analítica y numéricamente** la existencia de sesgo en el estimador de la varianza muestral por división de $n$ y su corrección mediante el divisor $n-1$ (corrección de Bessel) usando simulaciones de Monte Carlo.",
    "6. **Construir** tablas de distribución de frecuencias y determinar el número óptimo de intervalos de clase aplicando la **Regla de Sturges**."
])

# --- CELL 3: HISTORY AND STAGES ---
add_markdown([
    "## 1. Perspectiva Histórica y Metodología de la Estadística",
    "",
    "### 1.1 Breve Evolución Histórica",
    "El término *Estadística* proviene del latín *status*, que hace referencia al estado de las cosas. Históricamente, nació vinculada a las necesidades administrativas de los primeros imperios (Babilonia, Egipto, Roma, China) para realizar **censos** de población, tierras y riquezas con fines tributarios y militares.",
    "",
    "Con el tiempo, la estadística evolucionó a través de tres grandes etapas:",
    "1. **Estadística Descriptiva (Hasta el siglo XVIII):** Enfocada puramente en la recolección, síntesis y representación gráfica de datos demográficos y económicos.",
    "2. **Incorporación de la Probabilidad (Siglo XIX):** Científicos como Gauss introdujeron la **Distribución Normal** como modelo para describir los errores en las observaciones astronómicas y físicas.",
    "3. **Inferencia Estadística Moderna (Siglo XX):** Impulsada por Ronald A. Fisher, Karl Pearson, Egon Pearson y Jerzy Neyman. Desarrollaron la teoría del diseño experimental, la estimación de parámetros y el contraste de hipótesis, permitiendo extraer conclusiones generales de poblaciones gigantescas a partir de muestras reducidas.",
    "",
    "### 1.2 Etapas de un Estudio Estadístico",
    "Cualquier investigación científica basada en datos debe seguir de forma rigurosa las siguientes fases:",
    "1. **Planteamiento del problema:** Definir con claridad los objetivos de la investigación y el universo o **población** bajo estudio.",
    "2. **Planificación del trabajo de campo:** Diseñar el método de recolección (encuesta, muestreo, experimentación física) y el tamaño de la muestra.",
    "3. **Recopilación y depuración de información:** Obtener los datos y tratar problemas prácticos como datos faltantes, errores de oficina o datos anómalos (*outliers*).",
    "4. **Análisis de los datos:**",
    "   - **Análisis descriptivo:** Organizar los datos mediante tablas y gráficos y resumir sus propiedades clave.",
    "   - **Inferencia estadística:** Construir modelos de probabilidad y generalizar los resultados de la muestra a la población.",
    "   - **Validación del modelo:** Comprobar la validez de los supuestos teóricos (ej. pruebas de normalidad).",
    "5. **Interpretación:** Extraer conclusiones físicas o prácticas y tomar decisiones fundamentadas."
])

# --- CELL 4: BASIC CONCEPTS ---
add_markdown([
    "## 2. Conceptos Básicos: Población, Muestra y Muestreo",
    "",
    "Para formalizar el análisis estadístico, definimos tres términos esenciales:",
    "- **Población:** El conjunto total de individuos, objetos o mediciones que poseen la característica común que deseamos estudiar. Puede ser **finita** (ej. los estudiantes de una universidad) o **infinita** (ej. el número de lanzamientos posibles de una moneda o la posición de un electrón en mecánica cuántica).",
    "- **Individuo o elemento:** Cada uno de los componentes de la población.",
    "- **Muestra:** Un subconjunto de la población sobre el cual realizamos mediciones reales. Para poder generalizar las conclusiones, la muestra debe ser **representativa**, lo que significa que debe reflejar fielmente las proporciones y la diversidad de la población original.",
    "- **Muestra Aleatoria Simple:** Es un método de muestreo donde cada elemento de la población posee exactamente la misma probabilidad de ser seleccionado en la muestra. Esto previene sesgos humanos y garantiza la validez teórica de la inferencia.",
    "",
    "### Simulación en Python: El Principio de Representatividad",
    "A continuación, generaremos una población hipotética que modela la altura de 10,000 personas en una región (distribución normal con media $\\mu = 175$ cm y desviación estándar $\\sigma = 7$ cm). Simularemos la extracción de muestras aleatorias simples de diferentes tamaños ($n=10$, $n=50$ y $n=500$) para ilustrar visualmente cómo las muestras grandes reproducen con mayor fidelidad la densidad de probabilidad de la población original."
])

# --- CELL 5: CODE - SAMPLING AND REPRESENTATIVITY ---
add_code([
    "import numpy as np",
    "import matplotlib.pyplot as plt",
    "from scipy.stats import norm",
    "",
    "# Configurar estilo de graficación",
    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')",
    "",
    "# 1. Generar población de alturas (N = 10,000)",
    "np.random.seed(42)",
    "mu_pop, sigma_pop = 175.0, 7.0",
    "population = np.random.normal(mu_pop, sigma_pop, 10000)",
    "",
    "# 2. Tomar muestras aleatorias de diferentes tamaños",
    "sizes = [10, 50, 500]",
    "samples = {n: np.random.choice(population, size=n, replace=False) for n in sizes}",
    "",
    "# 3. Graficar histogramas de las muestras comparadas con la densidad de la población",
    "x_axis = np.linspace(150, 200, 300)",
    "pdf_pop = norm.pdf(x_axis, mu_pop, sigma_pop)",
    "",
    "fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)",
    "",
    "for idx, n in enumerate(sizes):",
    "    ax = axes[idx]",
    "    ax.hist(samples[n], bins=15, density=True, color='royalblue', alpha=0.6, edgecolor='black', label=f'Muestra (n={n})')",
    "    ax.plot(x_axis, pdf_pop, 'r-', linewidth=2.5, label='Población Real (PDF)')",
    "    ax.set_title(f'Tamaño de Muestra: n = {n}', fontweight='bold')",
    "    ax.set_xlabel('Altura (cm)')",
    "    if idx == 0:",
    "        ax.set_ylabel('Densidad de Probabilidad')",
    "    ax.legend(frameon=True)",
    "    ax.grid(True, linestyle='--', alpha=0.5)",
    "",
    "plt.tight_layout()",
    "plt.show()"
])

# --- CELL 6: PARAMETERS VS STATISTICS & BESSEL ---
add_markdown([
    "## 3. Parámetros frente a Estadísticos y el Sesgo de la Varianza",
    "",
    "Es vital distinguir entre la información de la población y la de la muestra:",
    "- **Parámetro:** Un valor numérico que describe una característica global de la **población**. Los parámetros son fijos y generalmente desconocidos (ej. la media poblacional $\\mu$, la varianza poblacional $\\sigma^2$).",
    "- **Estadístico (o Estimador):** Un valor numérico calculado a partir de los datos de la **muestra**. Los estadísticos son variables aleatorias, pues su valor cambia de una muestra a otra (ej. la media muestral $\\bar{x}$, la varianza muestral $S^2$).",
    "",
    "### El Sesgo y la Varianza Muestral (Corrección de Bessel)",
    "Consideremos una muestra aleatoria de tamaño $n$: $X_1, X_2, ..., X_n$.",
    "La **media muestral** $\\bar{x}$ se define como:",
    "$$\\bar{x} = \\frac{1}{n} \\sum_{i=1}^n X_i$$",
    "La media muestral es un estimador *insesgado* de la media poblacional, lo que significa que el valor esperado de la media de las muestras es igual al parámetro poblacional: $E[\\bar{x}] = \\mu$.",
    "",
    "Sin embargo, si intentamos calcular la varianza de la muestra usando la definición natural de varianza (dividiendo por $n$):",
    "$$S_{\\text{sesgada}}^2 = \\frac{1}{n} \\sum_{i=1}^n (X_i - \\bar{x})^2$$",
    "",
    "este estimador resulta estar **sesgado**. Tiende a subestimar sistemáticamente la verdadera varianza poblacional $\\sigma^2$. Esto ocurre porque los datos de la muestra están, en promedio, más cerca de su propia media muestral $\\bar{x}$ que de la verdadera media poblacional $\\mu$. Se puede demostrar analíticamente que la esperanza del estimador dividido por $n$ es:",
    "$$E[S_{\\text{sesgada}}^2] = \\frac{n-1}{n} \\sigma^2$$",
    "",
    "Para corregir este sesgo negativo, multiplicamos el estimador por el factor $\\frac{n}{n-1}$, dando origen a la **varianza muestral insesgada** (con la **corrección de Bessel**):",
    "$$S_{\\text{insesgada}}^2 = \\frac{1}{n-1} \\sum_{i=1}^n (X_i - \\bar{x})^2$$",
    "",
    "De este modo, su valor esperado coincide exactamente con el parámetro poblacional: $E[S_{\\text{insesgada}}^2] = \\sigma^2$.",
    "",
    "### Demostración Numérica por Simulación de Monte Carlo",
    "A continuación, realizaremos un experimento de Monte Carlo. Extraeremos 10,000 muestras aleatorias pequeñas de tamaño $n=5$ de nuestra población de alturas (cuya varianza real es $\\sigma^2 = 49.0$). Evaluaremos el promedio de los estimadores con divisor $n$ y con divisor $n-1$ para comprobar empíricamente cuál de ellos recupera el valor teórico sin sesgo."
])

# --- CELL 7: CODE - MONTE CARLO BESSEL CORRECTION ---
add_code([
    "import numpy as np",
    "",
    "np.random.seed(42)",
    "n_sample = 5",
    "n_simulations = 10000",
    "true_variance = sigma_pop**2  # 7^2 = 49.0",
    "",
    "variances_n = []",
    "variances_n_minus_1 = []",
    "",
    "# Ejecutar la simulación de Monte Carlo",
    "for _ in range(n_simulations):",
    "    # Extraer una muestra pequeña de la población",
    "    sample = np.random.choice(population, size=n_sample, replace=False)",
    "    sample_mean = np.mean(sample)",
    "    ",
    "    # Estimador con divisor n (sesgado)",
    "    var_n = np.sum((sample - sample_mean)**2) / n_sample",
    "    # Estimador con divisor n-1 (insesgado - Corrección de Bessel)",
    "    var_n_1 = np.sum((sample - sample_mean)**2) / (n_sample - 1)",
    "    ",
    "    variances_n.append(var_n)",
    "    variances_n_minus_1.append(var_n_1)",
    "",
    "# Calcular los promedios de los estimadores",
    "mean_var_n = np.mean(variances_n)",
    "mean_var_n_1 = np.mean(variances_n_minus_1)",
    "",
    "print(\"=== MONTE CARLO: SESGO DE LA VARIANZA MUESTRAL ===\")",
    "print(f\"Varianza Poblacional Real (teórica):        sigma^2 = {true_variance:.4f}\")",
    "print(f\"Promedio de Varianza Muestral con divisor n: E[S_n^2] = {mean_var_n:.4f}  (Sesgado)\")",
    "print(f\"Promedio de Varianza con divisor n-1:       E[S_{{n-1}}^2] = {mean_var_n_1:.4f}  (Insesgado)\")",
    "print(f\"Valor teórico esperado para S_n^2:          (n-1)/n * sigma^2 = {(n_sample-1)/n_sample * true_variance:.4f}\")",
    "",
    "# Validación numérica de tolerancia",
    "assert np.isclose(mean_var_n_1, true_variance, atol=1.0), \"Error en la simulación de Monte Carlo.\""
])

# --- CELL 8: VARIABLES AND SCALES ---
add_markdown([
    "## 4. Tipos de Variables y Escalas de Medición",
    "",
    "Antes de aplicar cualquier método matemático o gráfico, debemos clasificar las variables del estudio de acuerdo a su naturaleza y su escala de medida. Esto define qué operaciones aritméticas son válidas.",
    "",
    "### 4.1 Clasificación según Escala de Medida (Jerarquía de Medición)",
    "1. **Nominal:** Es el nivel más simple. Las categorías representan cualidades mutuamente excluyentes sin ningún orden lógico entre ellas (ej. sexo, nacionalidad, estado civil). Solo podemos verificar igualdad o diferencia ($=$ o $\\ne$).",
    "2. **Ordinal:** Además de clasificar, las categorías poseen un orden de jerarquía lógico (ej. rango militar, nivel de satisfacción, nivel de estudios). Podemos establecer comparaciones de orden ($<$ o $>$) pero no medir distancias numéricas entre categorías.",
    "3. **De Intervalo:** Nivel métrico para variables numéricas. Existe una unidad de medida constante que permite cuantificar la distancia exacta entre dos valores. Sin embargo, **el cero es arbitrario** (no representa la ausencia de la característica). El ejemplo clásico es la temperatura en grados Celsius: la diferencia entre $10^\\circ\\text{C}$ y $20^\\circ\\text{C}$ es la misma que entre $20^\\circ\\text{C}$ y $30^\\circ\\text{C}$, pero no podemos decir que $20^\\circ\\text{C}$ es el 'doble de caliente' que $10^\\circ\\text{C}$.",
    "4. **De Razón:** Es el nivel superior. Posee todas las propiedades de la escala de intervalo y además **un cero absoluto real** que representa la ausencia completa de la característica (ej. ingresos, masa de una partícula, edad, número de hijos). Permite realizar comparaciones multiplicativas (ej. un peso de 10 kg es exactamente el doble que un peso de 5 kg).",
    "",
    "### 4.2 Clasificación según su Naturaleza",
    "- **Variables Cualitativas o Categóricas:** Sus valores indican una cualidad y no pueden expresarse mediante cifras numéricas ni operarse aritméticamente (ej. nominales y ordinales). Pueden ser **dicotómicas** (solo dos opciones, ej. vivo/muerto) o **politómicas** (múltiples opciones, ej. color de ojos).",
    "- **Variables Cuantitativas o Numéricas:** Expresan cantidades en cifras y permiten realizar promedios y operaciones algebraicas. Se dividen en:",
    "  - **Discretas:** Toman valores aislados, típicamente enteros, separados por espacios vacíos (ej. número de hijos, número de colisiones de partículas).",
    "  - **Continuas:** Pueden tomar cualquier valor real dentro de un intervalo continuo (ej. tiempo de vida medio de un isótopo, longitud, masa)."
])

# --- CELL 9: CODE - DATASET GENERATION AND PLOTTING ---
add_code([
    "from collections import Counter",
    "import matplotlib.pyplot as plt",
    "",
    "# Crear datos sintéticos con diferentes tipos de variables",
    "sex_data = ['Hombre', 'Mujer', 'Mujer', 'Hombre', 'Mujer', 'Hombre', 'Mujer', 'Hombre', 'Hombre', 'Mujer']",
    "sat_data = ['Alta', 'Media', 'Baja', 'Alta', 'Alta', 'Media', 'Baja', 'Media', 'Alta', 'Media']",
    "hijos_data = [2, 0, 1, 3, 0, 2, 1, 0, 4, 1]",
    "peso_data = [75.4, 62.1, 58.5, 88.0, 54.2, 70.1, 65.3, 79.8, 92.5, 60.0]",
    "",
    "# Configurar subplots para representar gráficamente cada tipo de variable",
    "fig, axes = plt.subplots(2, 2, figsize=(14, 10))",
    "",
    "# 1. Gráfico de barras para variable Nominal (Sexo)",
    "sex_counts = Counter(sex_data)",
    "axes[0, 0].bar(list(sex_counts.keys()), list(sex_counts.values()), color=['skyblue', 'salmon'], edgecolor='black', width=0.5)",
    "axes[0, 0].set_title('Variable Nominal: Conteo por Sexo', fontweight='bold')",
    "axes[0, 0].set_ylabel('Frecuencia')",
    "axes[0, 0].grid(True, linestyle='--', alpha=0.5)",
    "",
    "# 2. Gráfico de barras ordenado para variable Ordinal (Satisfacción)",
    "sat_counts = Counter(sat_data)",
    "satisfaction_order = ['Baja', 'Media', 'Alta']",
    "sat_values = [sat_counts[cat] for cat in satisfaction_order]",
    "axes[0, 1].bar(satisfaction_order, sat_values, color='lightgreen', edgecolor='black', width=0.5)",
    "axes[0, 1].set_title('Variable Ordinal: Grado de Satisfacción', fontweight='bold')",
    "axes[0, 1].set_ylabel('Frecuencia')",
    "axes[0, 1].grid(True, linestyle='--', alpha=0.5)",
    "",
    "# 3. Gráfico de bastones para variable Cuantitativa Discreta (N_Hijos)",
    "hijos_counts = Counter(hijos_data)",
    "hijos_labels = sorted(list(hijos_counts.keys()))",
    "hijos_values = [hijos_counts[val] for val in hijos_labels]",
    "axes[1, 0].stem(hijos_labels, hijos_values, linefmt='b-', markerfmt='bo', basefmt='r-')",
    "axes[1, 0].set_title('Variable Cuantitativa Discreta: Número de Hijos', fontweight='bold')",
    "axes[1, 0].set_xlabel('Hijos')",
    "axes[1, 0].set_ylabel('Frecuencia')",
    "axes[1, 0].set_xticks(range(0, 5))",
    "axes[1, 0].grid(True, linestyle='--', alpha=0.5)",
    "",
    "# 4. Boxplot para variable Cuantitativa Continua (Peso_kg)",
    "axes[1, 1].boxplot(peso_data, patch_artist=True, boxprops=dict(facecolor='plum', color='black'))",
    "axes[1, 1].set_title('Variable Cuantitativa Continua: Distribución de Pesos', fontweight='bold')",
    "axes[1, 1].set_xticklabels(['Peso (kg)'])",
    "axes[1, 1].set_ylabel('Peso (kg)')",
    "axes[1, 1].grid(True, linestyle='--', alpha=0.5)",
    "",
    "plt.tight_layout()",
    "plt.show()"
])

# --- CELL 10: BINNING AND STURGES ---
add_markdown([
    "### 4.3 Agrupación en Intervalos de Clase y la Regla de Sturges",
    "",
    "Cuando trabajamos con variables cuantitativas continuas (o discretas con gran cantidad de valores únicos), presentar los datos de forma individual resulta ineficiente. En su lugar, agrupamos las observaciones en **intervalos de clase** (también llamados *bins* o contenedores).",
    "",
    "#### Determinación del número de intervalos: La Regla de Sturges",
    "Para evitar arbitrariedades al definir la cantidad de intervalos $k$ en una muestra de tamaño $n$, el matemático Herbert Sturges propuso en 1926 una regla empírica basada en la distribución binomial:",
    "",
    "$$k = 1 + \\log_2(n) = 1 + \\frac{\\ln(n)}{\\ln(2)}$$",
    "",
    "Generalmente, el valor obtenido se redondea al entero más cercano (o al entero superior). Una vez determinado $k$, el ancho de cada intervalo (amplitud $A$) se calcula a partir del rango de los datos (valor máximo menos mínimo):",
    "$$A = \\frac{\\text{Rango}}{k} = \\frac{X_{\\text{max}} - X_{\\text{min}}}{k}$$",
    "",
    "### Ejemplo Didáctico: Tabla de Frecuencias de Alturas",
    "A continuación, tomaremos una muestra de $n = 200$ alturas de nuestra población original y construiremos una **tabla de distribución de frecuencias** desde cero utilizando la Regla de Sturges. Calcularemos:",
    "1. Las marcas de clase (punto medio del intervalo).",
    "2. La frecuencia absoluta ($f_i$): cantidad de datos en el intervalo.",
    "3. La frecuencia relativa ($h_i = f_i / n$): proporción de datos.",
    "4. Las frecuencias acumuladas absolutas ($F_i$) y relativas ($H_i$)."
])

# --- CELL 11: CODE - FREQUENCY TABLE AND STURGES ---
add_code([
    "# 1. Tomar muestra de n = 200",
    "n_sample = 200",
    "sample_heights = np.random.choice(population, size=n_sample, replace=False)",
    "",
    "# 2. Aplicar la Regla de Sturges",
    "k = int(np.ceil(1 + np.log2(n_sample)))",
    "min_val = np.min(sample_heights)",
    "max_val = np.max(sample_heights)",
    "rango = max_val - min_val",
    "amplitud = rango / k",
    "",
    "print(f\"Tamaño de muestra (n):            {n_sample}\")",
    "print(f\"Intervalos según Sturges (k):     {k}\")",
    "print(f\"Amplitud del intervalo:          {amplitud:.4f} cm\\n\")",
    "",
    "# 3. Construir intervalos y calcular frecuencias manualmente",
    "limites = [min_val + i * amplitud for i in range(k + 1)]",
    "intervalos = []",
    "marcas_clase = []",
    "f_absoluta = []",
    "",
    "for i in range(k):",
    "    lim_inf = limites[i]",
    "    # Para incluir el valor máximo en el último intervalo",
    "    lim_sup = limites[i+1]",
    "    intervalos.append(f\"[{lim_inf:.2f}, {lim_sup:.2f})\")",
    "    marcas_clase.append((lim_inf + lim_sup) / 2.0)",
    "    ",
    "    # Contar datos en el intervalo",
    "    if i == k - 1:",
    "        count = np.sum((sample_heights >= lim_inf) & (sample_heights <= lim_sup))",
    "    else:",
    "        count = np.sum((sample_heights >= lim_inf) & (sample_heights < lim_sup))",
    "    f_absoluta.append(count)",
    "",
    "# Calcular frecuencias relativas y acumuladas",
    "f_relativa = [f / n_sample for f in f_absoluta]",
    "F_acumulada = np.cumsum(f_absoluta)",
    "H_acumulada = np.cumsum(f_relativa)",
    "",
    "# Mostrar la tabla de frecuencias",
    "print(\"=== TABLA DE DISTRIBUCIÓN DE FRECUENCIAS ===\")",
    "print(f\"{'Intervalo':<25} | {'Marca xi':<10} | {'Frec. fi':<10} | {'Frec. hi':<10} | {'Frec. Fi':<10} | {'Frec. Hi':<10}\")",
    "print(\"-\" * 80)",
    "for i in range(k):",
    "    print(f\"{intervalos[i]:<25} | {marcas_clase[i]:10.2f} | {f_absoluta[i]:10d} | {f_relativa[i]:10.4f} | {F_acumulada[i]:10d} | {H_acumulada[i]:10.4f}\")",
    "print()",
    "",
    "# Graficar el histograma resultante con Sturges",
    "plt.figure(figsize=(9, 5))",
    "plt.hist(sample_heights, bins=limites, color='lightblue', edgecolor='black', alpha=0.8)",
    "plt.title(f'Histograma de Alturas (k={k} intervalos de Sturges)', fontweight='bold')",
    "plt.xlabel('Altura (cm)')",
    "plt.ylabel('Frecuencia absoluta')",
    "plt.grid(True, linestyle='--', alpha=0.5)",
    "plt.tight_layout()",
    "plt.show()"
])

# --- CELL 12: EXERCISES ---
add_markdown([
    "## 5. Ejercicios Resueltos",
    "",
    "### Ejercicio 1: Demostración Analítica del Sesgo en la Varianza",
    "**Enunciado:** Demostrar analíticamente que $E[S^2] = \\sigma^2$ cuando dividimos por $n-1$, y que $E[S_{\\text{sesgada}}^2] = \\frac{n-1}{n}\\sigma^2$.",
    "",
    "**Solución:**",
    "Consideremos variables aleatorias independientes e idénticamente distribuidas $X_1, X_2, ..., X_n$ con media $E[X_i] = \\mu$ y varianza $\\text{Var}(X_i) = E[(X_i - \\mu)^2] = \\sigma^2$.",
    "La media muestral es $\\bar{x} = \\frac{1}{n} \\sum X_i$, con esperanza $E[\\bar{x}] = \\mu$ y varianza $\\text{Var}(\\bar{x}) = \\frac{\\sigma^2}{n}$.",
    "",
    "Reescribimos la suma de desviaciones cuadráticas de la muestra:",
    "$$\\sum_{i=1}^n (X_i - \\bar{x})^2 = \\sum_{i=1}^n ((X_i - \\mu) - (\\bar{x} - \\mu))^2$$",
    "$$\\sum_{i=1}^n (X_i - \\bar{x})^2 = \\sum_{i=1}^n (X_i - \\mu)^2 - 2(\\bar{x} - \\mu)\\sum_{i=1}^n (X_i - \\mu) + n(\\bar{x} - \\mu)^2$$",
    "Dado que $\\sum_{i=1}^n (X_i - \\mu) = n(\\bar{x} - \\mu)$:",
    "$$\\sum_{i=1}^n (X_i - \\bar{x})^2 = \\sum_{i=1}^n (X_i - \\mu)^2 - n(\\bar{x} - \\mu)^2$$",
    "",
    "Aplicando el valor esperado a ambos lados:",
    "$$E\\left[ \\sum_{i=1}^n (X_i - \\bar{x})^2 \\right] = \\sum_{i=1}^n E[(X_i - \\mu)^2] - n E[(\\bar{x} - \\mu)^2]$$",
    "Por definición, $E[(X_i - \\mu)^2] = \\sigma^2$ y $E[(\\bar{x} - \\mu)^2] = \\text{Var}(\\bar{x}) = \\frac{\\sigma^2}{n}$:",
    "$$E\\left[ \\sum_{i=1}^n (X_i - \\bar{x})^2 \\right] = n\\sigma^2 - n\\left(\\frac{\\sigma^2}{n}\\right) = n\\sigma^2 - \\sigma^2 = (n-1)\\sigma^2$$",
    "",
    "Por tanto, para el estimador sesgado dividiendo por $n$:",
    "$$E[S_{\\text{sesgada}}^2] = E\\left[ \\frac{1}{n} \\sum_{i=1}^n (X_i - \\bar{x})^2 \\right] = \\frac{1}{n} (n-1)\\sigma^2 = \\frac{n-1}{n}\\sigma^2$$",
    "Lo cual introduce un sesgo de $-\\frac{\\sigma^2}{n}$.",
    "",
    "Para el estimador insesgado dividiendo por $n-1$:",
    "$$E[S^2] = E\\left[ \\frac{1}{n-1} \\sum_{i=1}^n (X_i - \\bar{x})^2 \\right] = \\frac{1}{n-1} (n-1)\\sigma^2 = \\sigma^2$$",
    "Lo que demuestra analíticamente que la corrección de Bessel elimina por completo el sesgo.",
    "",
    "---",
    "",
    "### Ejercicio 2: Aplicación de la Regla de Sturges",
    "**Enunciado:** Un sensor de radiación registra $n = 500$ lecturas de decaimiento en un intervalo. Determinar el número de intervalos de clase recomendados por la Regla de Sturges y el ancho del intervalo si el rango de las mediciones oscila entre $12.0\\text{ Bq}$ y $45.8\\text{ Bq}$.",
    "",
    "**Solución:**",
    "1. **Calcular k:**",
    "   $$k = 1 + \\log_2(n) = 1 + \\log_2(500) \\approx 1 + 8.965 = 9.965$$",
    "   Redondeando al entero superior inmediato para garantizar cobertura, elegimos $k = 10$ intervalos.",
    "2. **Calcular la amplitud A:**",
    "   El rango es $X_{\\text{max}} - X_{\\text{min}} = 45.8 - 12.0 = 33.8\\text{ Bq}$.",
    "   La amplitud de cada contenedor es:",
    "   $$A = \\frac{\\text{Rango}}{k} = \\frac{33.8}{10} = 3.38\\text{ Bq}$$",
    "   Por lo tanto, se construirán 10 intervalos disjuntos de amplitud $3.38\\text{ Bq}$ cada uno."
])

# --- CELL 13: SUMMARY & BIBLIOGRAPHY ---
add_markdown([
    "## 6. Resumen y Bibliografía",
    "",
    "En esta lección introductoria, hemos sentado las bases del análisis estadístico. Aprendimos que la estadística actúa como una parte fundamental del método científico, permitiéndonos resumir información poblacional y estimar parámetros a partir de muestras aleatorias.",
    "",
    "Puntos clave estudiados:",
    "- La **Inferencia Estadística** depende del muestreo representativo y de estimadores insesgados.",
    "- La **Varianza Muestral** requiere dividir entre $n-1$ (corrección de Bessel) para eliminar el sesgo sistemático de subestimar la dispersión real de la población.",
    "- Las variables se clasifican por su nivel de medición (nominal, ordinal, intervalo y razón), determinando el tipo de gráfico e indicador aritmético válido.",
    "- El agrupamiento de datos continuos se realiza mediante intervalos de clase guiados por la **Regla de Sturges** ($k = 1 + \\log_2(n)$).",
    "",
    "### Bibliografía",
    "[1] C. Salazar y S. Del Castillo, *Fundamentos básicos de estadística*, 1a ed., 2018.",
    "[2] W. Mendenhall, R. J. Beaver, y B. Beaver, *Introducción a la probabilidad y estadística*, 13a ed., Cengage Learning, 2010.",
    "[3] J. Gorgas García, N. Cardiel López, y J. Zamorano Calvo, *Estadística básica*, Universidad Complutense de Madrid, 2011.",
    "[4] C. Batanero y C. Díaz, *Estadística con proyectos*, Universidad de Granada, 2011."
])

# Guardar a archivo
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"Cuaderno generado con éxito en: {output_path}")
