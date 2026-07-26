import json
import os

# Asegurar que existe la carpeta destino
output_dir = r"c:\Users\BlandskronNotebook\Documents\blandskron\licenciatura-en-fisica\06-estadistica-1\leccion-2"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "ordenacion-y-clasificacion-datos.ipynb")

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
    "# Lección 2: Ordenación y Clasificación del Registro de Datos",
    "### Módulo 6: Estadística I",
    "",
    "---",
    "",
    "Una vez recopilados los datos brutos de un estudio (mediante censos o encuestas muestrales), el siguiente paso metodológico consiste en su ordenación y clasificación para hacerlos interpretables. Este proceso se denomina **tabulación** y da origen a las tablas de distribución de frecuencias.",
    "",
    "En esta lección, estudiaremos formalmente los diferentes tipos de frecuencias (absolutas, relativas y acumuladas) y sus relaciones recursivas y algebraicas. Además, abordaremos de forma crítica un concepto fundamental donde la literatura y los medios de comunicación incurren frecuentemente en **erratas visuales graves**: la graficación de **histogramas con intervalos de amplitud desigual**. Utilizaremos simulaciones en Python para contrastar el error de usar alturas crudas frente a la formulación correcta basada en la **densidad de frecuencia**.",
    "",
    "---"
])

# --- CELL 2: OBJECTIVES ---
add_markdown([
    "## Objetivos de Aprendizaje",
    "",
    "Al finalizar esta lección, serás capaz de:",
    "1. **Diferenciar** entre encuestas censales (censo) y encuestas muestrales (muestras), analizando sus ventajas de costo y tiempo.",
    "2. **Definir y operar** con frecuencias absolutas ($n_i$), relativas ($f_i$), absolutas acumuladas ($N_i$) y relativas acumuladas ($F_i$), verificando analíticamente sus propiedades.",
    "3. **Construir** tablas de distribución de frecuencias para datos no agrupados y agrupados en intervalos de clase.",
    "4. **Identificar y corregir la errata** de graficación en histogramas de amplitud desigual, utilizando la densidad de frecuencia ($h_i = n_i / a_i$) para garantizar la proporcionalidad del área de las barras.",
    "5. **Trazar** polígonos de frecuencia acumulada (ojivas) y gráficos de series temporales utilizando la librería `Matplotlib` de acuerdo a los estándares del curso."
])

# --- CELL 3: SAMPLING AND CENSUS ---
add_markdown([
    "## 1. Origen de la Información: Censos, Muestras y Subpoblaciones",
    "",
    "El origen de la información estadística radica en la observación de una característica en una **población** o universo. Dependiendo del alcance, la recolección de datos se clasifica en:",
    "",
    "- **Censo:** Es la recogida de información sobre todos y cada uno de los elementos que integran la población. Aunque ofrece información completa y exacta, su realización acarrea altos costos económicos y largos tiempos de procesamiento.",
    "- **Encuesta Muestral:** Consiste en tomar un subconjunto representativo de la población, llamado **muestra**. La estadística provee técnicas de muestreo aleatorio para asegurar que la muestra actúe como una *réplica a escala* de la población, lo que permite estimar parámetros con un costo y tiempo significativamente menores.",
    "- **Subpoblación:** Es una parte de la población cuyos elementos comparten una característica común (ej. los pacientes de hospitales públicos dentro del total de pacientes de un país). Cabe destacar que las conclusiones obtenidas a partir de una subpoblación no pueden generalizarse a toda la población, ya que carecen de la representatividad del colectivo general."
])

# --- CELL 4: TABULATION AND PROPERTIES ---
add_markdown([
    "## 2. Presentación de Datos: Tabulación de Frecuencias",
    "",
    "Supongamos que observamos una variable cuantitativa discreta $X$ en una muestra de tamaño $N$, y que esta variable toma $k$ valores diferentes ordenados de forma creciente: $x_1 < x_2 < ... < x_k$.",
    "",
    "Para cada valor único $x_i$, definimos las siguientes **frecuencias estadísticas**:",
    "",
    "1. **Frecuencia Absoluta ($n_i$):** Es el número de observaciones en las que se presenta exactamente el valor $x_i$.",
    "2. **Frecuencia Relativa ($f_i$):** Es la proporción de observaciones que corresponden a $x_i$. Se obtiene como el cociente entre su frecuencia absoluta y el tamaño total de la muestra:",
    "   $$f_i = \\frac{n_i}{N}$$",
    "   Habitualmente se expresa en forma porcentual como $f_i \\times 100$.",
    "3. **Frecuencia Absoluta Acumulada ($N_i$):** Es el número de observaciones menores o iguales al valor $x_i$:",
    "   $$N_i = \\sum_{j=1}^i n_j$$",
    "4. **Frecuencia Relativa Acumulada ($F_i$):** Es la proporción de observaciones menores o iguales a $x_i$:",
    "   $$F_i = \\frac{N_i}{N} = \\sum_{j=1}^i f_j$$",
    "",
    "### Propiedades Fundamentales de las Frecuencias",
    "- **Suma de Absolutas:** $\\sum_{i=1}^k n_i = N$",
    "- **Suma de Relativas:** $\\sum_{i=1}^k f_i = 1$",
    "- **Acumulaciones finales:** $N_k = N$ y $F_k = 1$",
    "- **Fórmulas de Recurrencia:**",
    "  $$N_1 = n_1, \\quad N_i = N_{i-1} + n_i \\quad \\text{para } i=2, ..., k$$",
    "  $$F_1 = f_1, \\quad F_i = F_{i-1} + f_i \\quad \\text{para } i=2, ..., k$$"
])

# --- CELL 5: CODE - TABULAR CALCULATOR ---
add_code([
    "import numpy as np",
    "from collections import Counter",
    "",
    "# 1. Definir un conjunto de datos crudos (ej. número de defectos en 40 muestras físicas)",
    "raw_data = [2, 1, 0, 1, 3, 2, 0, 0, 1, 2, 1, 0, 3, 4, 1, 2, 1, 0, 2, 1,",
    "            0, 1, 2, 3, 1, 0, 1, 2, 2, 1, 0, 2, 1, 1, 0, 3, 2, 1, 0, 1]",
    "",
    "N = len(raw_data)",
    "counts = Counter(raw_data)",
    "valores_unicos = sorted(list(counts.keys()))",
    "k = len(valores_unicos)",
    "",
    "# 2. Calcular las frecuencias a mano",
    "n_i = [counts[val] for val in valores_unicos]",
    "f_i = [n / N for n in n_i]",
    "N_i = np.cumsum(n_i)",
    "F_i = np.cumsum(f_i)",
    "",
    "# 3. Mostrar la tabla formateada en ASCII",
    "print(\"=== TABLA DE FRECUENCIAS (DATOS NO AGRUPADOS) ===\")",
    "print(f\"{'xi':<6} | {'n_i (abs)':<10} | {'f_i (rel)':<10} | {'N_i (acum)':<10} | {'F_i (rel acum)':<14}\")",
    "print(\"-\" * 60)",
    "for i in range(k):",
    "    print(f\"{valores_unicos[i]:<6d} | {n_i[i]:<10d} | {f_i[i]:<10.4f} | {N_i[i]:<10d} | {F_i[i]:<14.4f}\")",
    "print()",
    "",
    "# 4. Verificación matemática de propiedades",
    "sum_n = sum(n_i)",
    "sum_f = sum(f_i)",
    "print(\"Verificación de propiedades:\")",
    "print(f\"  Suma de n_i = {sum_n}  (Esperado: N = {N})\")",
    "print(f\"  Suma de f_i = {sum_f:.4f}  (Esperado: 1.0)\")",
    "print(f\"  N_k = {N_i[-1]}  (Esperado: N = {N})\")",
    "print(f\"  F_k = {F_i[-1]:.4f}  (Esperado: 1.0)\")",
    "",
    "assert sum_n == N",
    "assert np.isclose(sum_f, 1.0)",
    "assert N_i[-1] == N",
    "assert np.isclose(F_i[-1], 1.0)"
])

# --- CELL 6: BINNED DATA & UNEQUAL HISTOGRAMS ---
add_markdown([
    "## 3. Datos Agrupados en Intervalos: Amplitudes Desiguales",
    "",
    "Cuando el número de datos es muy grande o la variable es de naturaleza continua, se clasifican los datos en $k$ intervalos de clase $[L_{i-1}, L_i)$, donde $L_{i-1}$ es el límite inferior y $L_i$ es el límite superior.",
    "",
    "Para cada intervalo, definimos adicionalmente:",
    "1. **Amplitud del Intervalo ($a_i$):** Es la longitud del intervalo:",
    "   $$a_i = L_i - L_{i-1}$$",
    "2. **Marca de Clase ($x_i$):** Es el punto medio del intervalo, el cual actúa como su representante en cálculos de medias y momentos:",
    "   $$x_i = \\frac{L_{i-1} + L_i}{2}$$",
    "",
    "---",
    "",
    "### Caso Crítico: La Errata de los Histogramas con Amplitudes Desiguales",
    "**La Errata Común:** En muchos medios de comunicación e incluso en textos técnicos introductorios, al construir un histograma para datos con intervalos de **ancho desigual** (amplitudes $a_i$ diferentes), se representa directamente la frecuencia absoluta $n_i$ (o la relativa $f_i$) en el eje vertical como la **altura** de la barra.",
    "",
    "**El Error Físico-Visual:** La característica que define a un histograma correcto es que **el área de cada rectángulo debe ser proporcional a la frecuencia del intervalo**. Si los anchos $a_i$ son desiguales y usamos la frecuencia cruda como altura $h_i = n_i$, el área resultante es:",
    "$$\\text{Área} = a_i \\cdot n_i$$",
    "Esto distorsiona completamente la representación. Una barra con el doble de ancho que otra parecerá tener el doble de datos incluso si contienen exactamente la misma cantidad, creando un grave sesgo de interpretación visual.",
    "",
    "**La Formulación Correcta (Densidad de Frecuencia):**",
    "Para corregir esta distorsión, la altura de cada rectángulo debe ser la **densidad de frecuencia** $h_i$:",
    "$$h_i = \\frac{n_i}{a_i} \\quad \\text{o} \\quad h_i = \\frac{f_i}{a_i}$$",
    "",
    "De esta manera, el área del rectángulo es:",
    "$$\\text{Área} = a_i \\cdot h_i = a_i \\cdot \\left(\\frac{n_i}{a_i}\\right) = n_i$$",
    "Así, el área coincide exactamente con la frecuencia, preservando la proporcionalidad física del gráfico.",
    "",
    "### Validación Computacional",
    "Simularemos un experimento de decaimiento radioactivo y agruparemos los datos en intervalos de amplitudes desiguales (anchos mayores en los extremos donde los datos son escasos). Graficaremos el histograma incorrecto (frecuencias crudas como alturas) y el correcto (densidades de frecuencia como alturas) para ilustrar la distorsión del perfil de distribución."
])

# --- CELL 7: CODE - UNEQUAL BINS PLOTS ---
add_code([
    "import numpy as np",
    "import matplotlib.pyplot as plt",
    "",
    "# 1. Generar datos experimentales continuos (tiempos de decaimiento con distribución exponencial)",
    "np.random.seed(42)",
    "decays = np.random.exponential(scale=10.0, size=500)",
    "",
    "# 2. Definir intervalos de clase con amplitudes desiguales",
    "# Los intervalos se ensanchan a medida que disminuye la densidad de datos",
    "limites_desiguales = [0, 2, 5, 10, 20, 50]  # Amplitudes: 2, 3, 5, 10, 30",
    "k_desigual = len(limites_desiguales) - 1",
    "",
    "# Calcular frecuencias absolutas y amplitudes",
    "n_desigual = []",
    "amplitudes = []",
    "for i in range(k_desigual):",
    "    lim_inf = limites_desiguales[i]",
    "    lim_sup = limites_desiguales[i+1]",
    "    count = np.sum((decays >= lim_inf) & (decays < lim_sup))",
    "    n_desigual.append(count)",
    "    amplitudes.append(lim_sup - lim_inf)",
    "",
    "n_desigual = np.array(n_desigual)",
    "amplitudes = np.array(amplitudes)",
    "",
    "# Calcular alturas correctas (densidad de frecuencia)",
    "h_correcto = n_desigual / amplitudes",
    "",
    "# 3. Graficar comparativa",
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))",
    "",
    "# Gráfico Izquierdo: Histogramas Erróneo (Altura = Frecuencia)",
    "# Para ilustrar el error, dibujamos barras con el ancho correspondiente pero la altura cruda",
    "centros_barras = [limites_desiguales[i] + amplitudes[i]/2 for i in range(k_desigual)]",
    "ax1.bar(centros_barras, n_desigual, width=amplitudes, color='tomato', edgecolor='black', alpha=0.7)",
    "ax1.set_title('Histograma Erróneo (Altura = Frecuencia)', fontweight='bold', color='red')",
    "ax1.set_xlabel('Tiempo de decaimiento (s)')",
    "ax1.set_ylabel('Frecuencia absoluta (n_i)')",
    "ax1.grid(True, linestyle='--', alpha=0.5)",
    "",
    "# Gráfico Derecho: Histograma Correcto (Altura = Densidad de Frecuencia)",
    "# En matplotlib, pasamos density=False pero especificamos las alturas calculadas",
    "ax2.bar(centros_barras, h_correcto, width=amplitudes, color='royalblue', edgecolor='black', alpha=0.7)",
    "ax2.set_title('Histograma Correcto (Altura = Densidad)', fontweight='bold', color='blue')",
    "ax2.set_xlabel('Tiempo de decaimiento (s)')",
    "ax2.set_ylabel('Densidad de frecuencia (n_i / a_i)')",
    "ax2.grid(True, linestyle='--', alpha=0.5)",
    "",
    "plt.tight_layout()",
    "plt.show()",
    "",
    "# Mostrar las discrepancias de áreas",
    "print(\"=== COMPARATIVA DE ÁREAS ===\")",
    "for i in range(k_desigual):",
    "    area_erronea = amplitudes[i] * n_desigual[i]",
    "    area_correcta = amplitudes[i] * h_correcto[i]",
    "    print(f\"Intervalo {i+1} [{limites_desiguales[i]:>2}, {limites_desiguales[i+1]:>2}) | Ancho: {amplitudes[i]:>2} | Frec: {n_desigual[i]:>3} | Área Gráfico Erróneo: {area_erronea:>5.1f} | Área Gráfico Correcto: {area_correcta:>5.1f}\")"
])

# --- CELL 8: OGIVE AND TIME SERIES ---
add_markdown([
    "## 4. Polígonos de Frecuencia Acumulada (Ojiva) y Series Temporales",
    "",
    "### 4.1 La Ojiva (Polígono de Frecuencias Acumuladas)",
    "Para visualizar la distribución acumulativa de los datos agrupados, se utiliza la **Ojiva**. Es un gráfico de líneas que conecta los puntos correspondientes a los **límites superiores de cada intervalo** con sus respectivas frecuencias acumuladas ($N_i$ o $F_i$). El gráfico se inicia en el límite inferior del primer intervalo con una frecuencia acumulada de cero.",
    "",
    "### 4.2 Series Temporales",
    "Cuando las observaciones se realizan secuencialmente a lo largo del tiempo (ej. mediciones diarias de radiación solar, evolución de la temperatura de un sensor), los datos se denominan **series temporales** o cronológicas. En este caso, el eje horizontal representa el tiempo ($t$) y los puntos se conectan mediante líneas para visualizar tendencias y oscilaciones."
])

# --- CELL 9: CODE - OGIVE AND TIME SERIES PLOTS ---
add_code([
    "# 1. Graficación de la Ojiva (Polígono de Frecuencia Relativa Acumulada)",
    "F_desigual = np.cumsum(n_desigual) / len(decays)",
    "# Añadir el punto inicial (limite inferior del primer intervalo con F = 0)",
    "x_ojiva = [limites_desiguales[0]] + limites_desiguales[1:]",
    "y_ojiva = [0.0] + list(F_desigual)",
    "",
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5))",
    "",
    "ax1.plot(x_ojiva, y_ojiva, 'o-', color='purple', linewidth=2.5, markersize=8, label='Ojiva (Acumulada)')",
    "ax1.fill_between(x_ojiva, y_ojiva, color='purple', alpha=0.15)",
    "ax1.set_title('Ojiva de Frecuencias Relativas Acumuladas', fontweight='bold')",
    "ax1.set_xlabel('Tiempo de decaimiento (s)')",
    "ax1.set_ylabel('Frecuencia Relativa Acumulada (F_i)')",
    "ax1.set_ylim(-0.05, 1.05)",
    "ax1.grid(True, linestyle='--', alpha=0.5)",
    "ax1.legend(frameon=True)",
    "",
    "# 2. Graficación de una Serie Temporal (ej. flujo magnético en un experimento durante 12 meses)",
    "meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']",
    "flujo_magnetico = [12.4, 12.8, 14.1, 13.9, 15.6, 16.2, 15.8, 14.9, 13.5, 12.9, 13.1, 13.8]",
    "",
    "ax2.plot(meses, flujo_magnetico, 's-', color='teal', linewidth=2.5, markersize=6, label='Flujo medido (Wb)')",
    "ax2.set_title('Serie Temporal: Evolución del Flujo Magnético', fontweight='bold')",
    "ax2.set_xlabel('Mes')",
    "ax2.set_ylabel('Flujo Magnético (Wb)')",
    "ax2.set_ylim(10.0, 18.0)",
    "ax2.grid(True, linestyle='--', alpha=0.5)",
    "ax2.legend(frameon=True)",
    "",
    "plt.tight_layout()",
    "plt.show()"
])

# --- CELL 10: EXERCISES ---
add_markdown([
    "## 5. Ejercicios Resueltos",
    "",
    "### Ejercicio 1: Tabulación Manual de Calificaciones",
    "**Enunciado:** A partir de las calificaciones de 20 alumnos en un examen de laboratorio: `5, 7, 6, 8, 5, 9, 7, 8, 6, 10, 5, 7, 8, 6, 9, 8, 7, 5, 6, 7`. Construir la tabla de distribución de frecuencias y calcular la proporción de alumnos con nota menor o igual a 8.",
    "",
    "**Solución:**",
    "1. **Identificar valores únicos:** Los valores ordenados son $x_1=5, x_2=6, x_3=7, x_4=8, x_5=9, x_6=10$.",
    "2. **Contar frecuencias absolutas ($n_i$):**",
    "   - $n(5) = 4$, $n(6) = 4$, $n(7) = 5$, $n(8) = 4$, $n(9) = 2$, $n(10) = 1$. Total $N = 20$.",
    "3. **Calcular frecuencias acumuladas ($N_i$):**",
    "   - $N(5) = 4$, $N(6) = 8$, $N(7) = 13$, $N(8) = 17$, $N(9) = 19$, $N(10) = 20$.",
    "4. **Calcular frecuencias relativas acumuladas ($F_i$):**",
    "   - $F(5) = 0.20$, $F(6) = 0.40$, $F(7) = 0.65$, $F(8) = 0.85$, $F(9) = 0.95$, $F(10) = 1.00$.",
    "",
    "La proporción de alumnos con nota menor o igual a 8 es la frecuencia relativa acumulada $F(8) = 0.85$, lo que equivale al $85\\%$ de los alumnos.",
    "",
    "---",
    "",
    "### Ejercicio 2: Construcción de Histograma con Amplitud Desigual",
    "**Enunciado:** Se miden los tiempos de reacción en un experimento y se agrupan en tres intervalos: $[0, 2)$ con 10 observaciones, $[2, 4)$ con 20 observaciones, y $[4, 10)$ con 15 observaciones. Determinar las alturas de los rectángulos correspondientes para graficar el histograma de densidad correcto.",
    "",
    "**Solución:**",
    "1. **Calcular amplitudes ($a_i$):**",
    "   - $a_1 = 2 - 0 = 2$.",
    "   - $a_2 = 4 - 2 = 2$.",
    "   - $a_3 = 10 - 4 = 6$.",
    "2. **Calcular densidades de frecuencia como alturas ($h_i = n_i / a_i$):**",
    "   - $h_1 = \\frac{10}{2} = 5.0$.",
    "   - $h_2 = \\frac{20}{2} = 10.0$.",
    "   - $h_3 = \\frac{15}{6} = 2.5$.",
    "3. **Verificación de áreas:**",
    "   - Área 1: $2 \\times 5.0 = 10$ (frecuencia del primer intervalo).",
    "   - Área 2: $2 \\times 10.0 = 20$ (frecuencia del segundo intervalo).",
    "   - Área 3: $6 \\times 2.5 = 15$ (frecuencia del tercer intervalo).",
    "   El área total es $10 + 20 + 15 = 45$, que coincide exactamente con el tamaño total de la muestra."
])

# --- CELL 11: SUMMARY & BIBLIOGRAPHY ---
add_markdown([
    "## 6. Resumen y Bibliografía",
    "",
    "En esta lección, hemos estudiado los métodos para ordenar y presentar registros de datos procedentes de censos y muestras.",
    "",
    "Puntos clave estudiados:",
    "- La **tabulación** organiza los datos en tablas de distribución de frecuencias para simplificar su análisis.",
    "- Las **frecuencias relativas** miden la proporción ($f_i$) y acumulada ($F_i$), esenciales para la interpretación probabilística.",
    "- Al graficar **histogramas de intervalos de amplitud desigual**, es obligatorio utilizar la **densidad de frecuencia** ($h_i = n_i / a_i$) como altura para evitar la distorsión del perfil visual.",
    "- La **Ojiva** es la representación gráfica de las frecuencias acumuladas y describe de forma continua la acumulación de datos.",
    "",
    "### Bibliografía",
    "[1] M. L. Berenson, D. M. Levine, y T. C. Krehbiel, *Basic Business Statistics: Concepts and Applications*, 12a ed., Pearson International, 2012.",
    "[2] R. Pérez, C. Caso, M. J. Río, y A. J. López, *Introducción a la Estadística Económica*, Universidad de Oviedo, 2011.",
    "[3] W. Mendenhall, R. J. Beaver, y B. Beaver, *Introducción a la probabilidad y estadística*, 13a ed., Cengage Learning, 2010."
])

# Guardar a archivo
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"Cuaderno de Lección 2 generado con éxito en: {output_path}")
