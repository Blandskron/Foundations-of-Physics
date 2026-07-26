import json
import os

print("=== CREANDO GENERADOR PROGRAMÁTICO DE CUADERNO PARA LECCIÓN 8 (.ipynb) CORREGIDO ===")

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
add_md(r"""# Lección 8: Introducción a la Probabilidad: Cálculo y Conceptos Básicos

**Módulo 6: Estadística I**  
*Foundations of Physics - Licenciatura en Física*

---
""")

# --- CELL 2: OBJETIVOS ---
add_md(r"""## Objetivos de Aprendizaje

1. **Comprender la Génesis Histórica y los Enfoques de la Probabilidad:** Analizar el origen del cálculo de probabilidades en los juegos de azar (correspondencia Pascal-Fermat de 1654 sobre las apuestas del Chevalier de Méré) y el desarrollo de los tres enfoques principales: Clásico / A Priori (Laplace), Frecuencial / Empírico y Subjetivo.
2. **Formular la Teoría de Conjuntos y Sucesos Aleatorios:** Definir el Espacio Muestral ($\Omega$), sucesos elementales y compuestos, suceso imposible ($\emptyset$), suceso seguro ($\Omega$), contrarios ($A^c$), incompatibles ($A \cap B = \emptyset$) y exhaustivos ($\bigcup A_i = \Omega$).
3. **Operar con Eventos y Demostrar las Leyes de De Morgan:** Aplicar operaciones de unión, intersección, complemento, diferencia, diferencia simétrica y demostrar formalmente las Leyes de De Morgan:
   $$(A \cup B)^c = A^c \cap B^c, \quad (A \cap B)^c = A^c \cup B^c$$
4. **Dominar la Axiomatización de Kolmogorov (1933):** Fundamentar el cálculo probabilístico sobre los 3 Axiomas de Kolmogorov ($P(A) \ge 0$, $P(\Omega) = 1$, $P(\bigcup A_i) = \sum P(A_i)$) y sus teoremas derivados.
5. **Aplicar los Teoremas Fundamentales de Probabilidad:** Resolver problemas probabilísticos complejos utilizando la Regla General de la Adición, la Probabilidad Compuesta o Regla del Producto ($P(A \cap B) = P(A) P(B \mid A)$) y evaluar la independencia estocástica.
6. **Desarrollar el Teorema de la Probabilidad Total y el Teorema de Bayes:** Calcular probabilidades en sistemas exhaustivos e incompatibles de sucesos ($P(B) = \sum P(B \mid A_i) P(A_i)$) e implementar la actualización de probabilidades a posteriori mediante el Teorema de Bayes ($P(A_j \mid B) = \frac{P(B \mid A_j) P(A_j)}{P(B)}$).
""")

# --- CELL 3: SECCIÓN 1 (TEORÍA) ---
add_md(r"""---

## 1. Introducción a la Probabilidad y Enfoques Conceptuales

El origen formal del cálculo de probabilidades se remonta a 1654, cuando el aristócrata Antoine Gombaud, conocido como el **Chevalier de Méré**, consultó al matemático Blaise Pascal (1623–1662) sobre un problema de reparto equitativo de apuestas en un juego de dados interrumpido antes de su finalización. Pascal inició una célebre correspondencia con Pierre de Fermat (1601–1665), sentando las bases matemáticas del análisis de azar.

En el II Congreso Internacional de Matemáticos (1900), David Hilbert planteó como uno de sus 23 problemas la fundamentación axiomática de la probabilidad. En 1933, el matemático ruso A. N. Kolmogorov (1903–1987) formalizó la teoría moderna basada en la teoría de la medida.

### 1.1. Los Tres Enfoques Conceptuales de la Probabilidad

1. **Enfoque Clásico o A Priori (Laplace):**
   Supone equiprobabilidad de los resultados muestrales. Si un experimento presenta $x$ resultados favorables al evento $A$ y $z$ resultados desfavorables de un total $N = x + z$ mutuamente excluyentes:

   $$P(A) = \frac{\text{Casos Favorables}}{\text{Casos Posibles}} = \frac{x}{x + z}$$

   *Ejemplo:* En una caja con 9 piedras rojas y 15 verdes, $P(\text{Roja}) = \frac{9}{9+15} = \frac{9}{24} = 0.375$ ($37.5\%$).

2. **Enfoque Frecuencial o Empírico:**
   Basado en la observación repetida de un experimento aleatorio en las mismas condiciones. La probabilidad es el límite de la frecuencia relativa a largo plazo:

   $$P(A) = \lim_{N \to \infty} \frac{n_A}{N}$$

   *Ejemplo:* Si 9 de cada 50 vehículos no usan cinturón, $P(\text{Sin Cinturón}) = \frac{9}{50} = 0.18$ ($18\%$).

3. **Enfoque Subjetivo:**
   Cuantifica el grado de creencia personal sobre la ocurrencia de un evento único no repetible (ej. el resultado de un partido de fútbol o una elección política) basado en la evidencia disponible.
""")

# --- CELL 4: SECCIÓN 1 (CÓDIGO) ---
add_code(r"""import numpy as np
import matplotlib.pyplot as plt

# Simulación de Monte Carlo del Problema del Chevalier de Méré (1654)
# Apuesta 1: Obtener al menos un 6 en 4 lanzamientos de un dado.
# Apuesta 2: Obtener al menos un doble 6 en 24 lanzamientos de dos dados.

np.random.seed(42)
n_simulaciones = 100000

# Apuesta 1
dados_4 = np.random.randint(1, 7, size=(n_simulaciones, 4))
exito1 = np.any(dados_4 == 6, axis=1)
p1_empirica = np.mean(exito1)
p1_teorica = 1.0 - (5.0 / 6.0)**4

# Apuesta 2
d1 = np.random.randint(1, 7, size=(n_simulaciones, 24))
d2 = np.random.randint(1, 7, size=(n_simulaciones, 24))
exito2 = np.any((d1 == 6) & (d2 == 6), axis=1)
p2_empirica = np.mean(exito2)
p2_teorica = 1.0 - (35.0 / 36.0)**24

print("=== RESOLUCIÓN HISTÓRICA DEL PROBLEMA DEL CHEVALIER DE MÉRÉ (1654) ===")
print(f"• Apuesta 1 (1 seis en 4 dados):  Empírica = {p1_empirica:.4f} | Teórica = {p1_teorica:.4f} (> 0.50 -> Rentable)")
print(f"• Apuesta 2 (Doble 6 en 24 dados): Empírica = {p2_empirica:.4f} | Teórica = {p2_teorica:.4f} (< 0.50 -> Pérdida)")

assert np.isclose(p1_empirica, p1_teorica, atol=0.005)
assert np.isclose(p2_empirica, p2_teorica, atol=0.005)
print("\n[VERIFICACIÓN] Las simulaciones de Monte Carlo confirman los cálculos analíticos de Pascal y Fermat.")
""")

# --- CELL 5: SECCIÓN 2 (TEORÍA) ---
add_md(r"""---

## 2. Conceptos Básicos y Teoría de Conjuntos

* **Experimento Determinista:** Aquel cuyo resultado exacto se conoce de antemano bajo condiciones iniciales fijas.
* **Experimento Aleatorio:** Aquel cuyo resultado específico no se puede predecir con certeza antes de su ejecución, pero cuyos posibles resultados son conocidos y el experimento es repetible.
* **Espacio Muestral ($\Omega$):** Conjunto de todos los posibles resultados elementales de una experiencia aleatoria.
  - *Discreto Finito:* Lanzamiento de un dado ($\Omega = \{1, 2, 3, 4, 5, 6\}$).
  - *Discreto Infinito:* Número de lanzamientos hasta obtener la primera cara.
  - *Continuo:* Intervalos continuos de la recta real (medición de tiempos, distancias o masa).

### 2.1. Operaciones entre Conjuntos y Leyes de De Morgan

Dado un Espacio Muestral $\Omega$ y eventos $A, B \subseteq \Omega$:

1. **Unión ($A \cup B$):** Ocurre $A$, ocurre $B$ o ocurren ambos simultáneamente.
2. **Intersección ($A \cap B$):** Ocurren $A$ y $B$ simultáneamente.
3. **Complementario ($A^c$ o $\bar{A}$):** Ocurre si y solo si no ocurre $A$. $A \cup A^c = \Omega, A \cap A^c = \emptyset$.
4. **Diferencia ($A \setminus B$):** Ocurre $A$ pero no ocurre $B$ ($A \setminus B = A \cap B^c$).

#### Leyes de De Morgan:
1. Complemento de la Unión:
   $$(A \cup B)^c = A^c \cap B^c$$
2. Complemento de la Intersección:
   $$(A \cap B)^c = A^c \cup B^c$$
""")

# --- CELL 6: SECCIÓN 2 (CÓDIGO) ---
add_code(r"""import numpy as np

# Motor analítico de Álgebra de Conjuntos en Python
omega = set(range(1, 11)) # Espacio Muestral \Omega = {1, 2, ..., 10}

A = {2, 3, 5, 7}       # Evento A: Primos menores o iguales a 10
B = {2, 4, 6, 8, 10}   # Evento B: Pares menores o iguales a 10

A_c = omega - A
B_c = omega - B

# Operaciones algebraicas
union_AB = A | B
inter_AB = A & B
diff_AB = A - B
diff_sim = A ^ B

# Verificación analítica de las Leyes de De Morgan
de_morgan_1_left = omega - union_AB
de_morgan_1_right = A_c & B_c

de_morgan_2_left = omega - inter_AB
de_morgan_2_right = A_c | B_c

print("=== OPERACIONES DE CONJUNTOS Y LEYES DE DE MORGAN ===")
print(f"• Espacio Muestral \\Omega: {omega}")
print(f"• Evento A (Primos):    {A}")
print(f"• Evento B (Pares):     {B}")
print(f"• Unión A U B:          {union_AB}")
print(f"• Intersección A \\cap B:  {inter_AB}")
print(f"• Diferencia A - B:     {diff_AB}")
print(f"• Ley 1 De Morgan (A U B)^c: {de_morgan_1_left} == A^c \\cap B^c: {de_morgan_1_right}")
print(f"• Ley 2 De Morgan (A \\cap B)^c: {de_morgan_2_left} == A^c U B^c: {de_morgan_2_right}")

assert de_morgan_1_left == de_morgan_1_right
assert de_morgan_2_left == de_morgan_2_right
print("\n[VERIFICACIÓN] Demostración exitosa de las Leyes de De Morgan.")
""")

# --- CELL 7: SECCIÓN 3 (TEORÍA) ---
add_md(r"""---

## 3. Axiomas de Kolmogorov y Teoremas Fundamentales

En 1933, Andrey Kolmogorov formalizó la probabilidad como una función de conjunto $P: \mathcal{F} \to \mathbb{R}$ que asigna un número real a cada evento del espacio muestral $\Omega$ satisfaciendo tres axiomas fundamentales.

### 3.1. Los Tres Axiomas de Kolmogorov (1933)

1. **Axioma de No-Negatividad:**  
   Para todo evento $A \subseteq \Omega$:
   $$P(A) \ge 0$$

2. **Axioma de Certidumbre (Normalización):**  
   Para el espacio muestral seguro $\Omega$:
   $$P(\Omega) = 1$$

3. **Axioma de Aditividad ($\sigma$-aditividad):**  
   Si $A_1, A_2, \dots$ es una secuencia de eventos mutuamente excluyentes dos a dos ($A_i \cap A_j = \emptyset, \forall i \ne j$):
   $$P\left( \bigcup_{i=1}^\infty A_i \right) = \sum_{i=1}^\infty P(A_i)$$

---

### 3.2. Teoremas Derivados Fundamentales

* **Probabilidad del Evento Imposible:** $P(\emptyset) = 0$.
* **Acotamiento:** $0 \le P(A) \le 1, \quad \forall A \subseteq \Omega$.
* **Probabilidad del Complemento:**
  $$P(A^c) = 1 - P(A)$$
* **Regla General de la Adición (Eventos no excluyentes):**
  $$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$
""")

# --- CELL 8: SECCIÓN 3 (CÓDIGO) ---
add_code(r"""import numpy as np

# Verificación computacional del Teorema de la Adición General: P(A U B) = P(A) + P(B) - P(A \cap B)
# Lanzamiento de un dado equilibrado: A = {Par} = {2, 4, 6}, B = {Mayor que 3} = {4, 5, 6}

omega_dado = {1, 2, 3, 4, 5, 6}
A_par = {2, 4, 6}
B_mayor3 = {4, 5, 6}

p_A = len(A_par) / len(omega_dado) # 3/6 = 0.5
p_B = len(B_mayor3) / len(omega_dado) # 3/6 = 0.5

inter_AB = A_par & B_mayor3 # {4, 6}
p_inter_AB = len(inter_AB) / len(omega_dado) # 2/6 = 0.3333

union_AB = A_par | B_mayor3 # {2, 4, 5, 6}
p_union_empirica = len(union_AB) / len(omega_dado) # 4/6 = 0.6667

# Aplicación del Teorema de la Adición
p_union_teorica = p_A + p_B - p_inter_AB

print("=== VERIFICACIÓN DEL TEOREMA GENERAL DE LA ADICIÓN ===")
print(f"• P(A) [Pares]:        {p_A:.4f}")
print(f"• P(B) [> 3]:          {p_B:.4f}")
print(f"• P(A AND B):          {p_inter_AB:.4f}")
print(f"• P(A U B) Teórica:   {p_union_teorica:.4f} == Empírica: {p_union_empirica:.4f}")

assert np.isclose(p_union_teorica, p_union_empirica)
print("[VERIFICACIÓN] Se satisface el Teorema General de la Adición de Kolmogorov.")
""")

# --- CELL 9: SECCIÓN 4 (TEORÍA) ---
add_md(r"""---

## 4. Probabilidad Compuesta, Probabilidad Total y Teorema de Bayes

### 4.1. Probabilidad Condicionada y Regla de la Multiplicación

La **probabilidad condicionada** de $B$ dado que ha ocurrido $A$ ($P(A) > 0$) se define como:

$$P(B \mid A) = \frac{P(A \cap B)}{P(A)}$$

Por consiguiente, la **probabilidad compuesta** o regla del producto es:

$$P(A \cap B) = P(A) \cdot P(B \mid A) = P(B) \cdot P(A \mid B)$$

#### Independencia Estocástica:
Dos eventos $A$ y $B$ son **estocásticamente independientes** si y solo si la ocurrencia de uno no altera la probabilidad del otro:

$$P(A \cap B) = P(A) \cdot P(B) \iff P(B \mid A) = P(B)$$

---

### 4.2. Teorema de la Probabilidad Total

Sea $A_1, A_2, \dots, A_n$ una partición completa del espacio muestral $\Omega$ (sucesos mutuamente excluyentes $A_i \cap A_j = \emptyset$ y colectivamente exhaustivos $\bigcup_{i=1}^n A_i = \Omega$) con $P(A_i) > 0$. Para cualquier evento $B \subseteq \Omega$:

$$P(B) = \sum_{i=1}^n P(B \cap A_i) = \sum_{i=1}^n P(B \mid A_i) \cdot P(A_i)$$

---

### 4.3. Teorema de Bayes (Actualización de Probabilidades a Posteriori)

Bajo las mismas hipótesis del Teorema de la Probabilidad Total, la probabilidad a posteriori del suceso causa $A_j$ dado que se ha observado el evento efecto $B$ satisface:

$$P(A_j \mid B) = \frac{P(B \mid A_j) \cdot P(A_j)}{P(B)} = \frac{P(B \mid A_j) \cdot P(A_j)}{\sum_{i=1}^n P(B \mid A_i) \cdot P(A_i)}$$

#### Ejemplo Oficial de las 3 Urnas:
Se disponen tres urnas con la siguiente composición:
- **Urna 1 ($U_1$):** 3 bolas Blancas (B), 2 Rojas (R) $\implies P(B \mid U_1) = 3/5$.
- **Urna 2 ($U_2$):** 4 bolas Blancas (B), 2 Rojas (R) $\implies P(B \mid U_2) = 4/6$.
- **Urna 3 ($U_3$):** 0 bolas Blancas (B), 3 Rojas (R) $\implies P(B \mid U_3) = 0$.

Se elige una urna al azar ($P(U_1) = P(U_2) = P(U_3) = 1/3$) y se extrae una bola que resulta ser **Blanca ($B$)**.

1. **Probabilidad Total de Blanca:**
   $$P(B) = \frac{3}{5}\cdot\frac{1}{3} + \frac{4}{6}\cdot\frac{1}{3} + 0\cdot\frac{1}{3} = \frac{1}{5} + \frac{2}{9} + 0 = \frac{19}{45} \approx 0.4222$$

2. **Probabilidades a Posteriori (Bayes):**
   - $P(U_1 \mid B) = \frac{\frac{3}{5} \cdot \frac{1}{3}}{\frac{19}{45}} = \frac{9}{19} \approx 0.4737$
   - $P(U_2 \mid B) = \frac{\frac{4}{6} \cdot \frac{1}{3}}{\frac{19}{45}} = \frac{10}{19} \approx 0.5263$
   - $P(U_3 \mid B) = 0$
""")

# --- CELL 10: SECCIÓN 4 (CÓDIGO) ---
add_code(r"""import numpy as np
import matplotlib.pyplot as plt

class SistemaBayesiano:
    # Calculadora bayesiana genérica para evaluar la Probabilidad Total 
    # y actualizar las distribuciones a posteriori según el Teorema de Bayes.
    def __init__(self, prioris, verosimilitudes):
        self.prioris = np.array(prioris, dtype=float)
        self.verosimilitudes = np.array(verosimilitudes, dtype=float)
        
    def probabilidad_total(self):
        return np.sum(self.prioris * self.verosimilitudes)
        
    def posteriores(self):
        p_total = self.probabilidad_total()
        return (self.prioris * self.verosimilitudes) / p_total

# Replicación exacta del problema de las 3 Urnas de la lección
prioris = [1/3, 1/3, 1/3]
verosimilitudes_blanca = [3/5, 4/6, 0/3]

bayes_3urnas = SistemaBayesiano(prioris, verosimilitudes_blanca)

p_b_total = bayes_3urnas.probabilidad_total()
posteriores = bayes_3urnas.posteriores()

print("=== CALCULADORA BAYESIANA (PROBLEMA DE LAS 3 URNAS) ===")
print(f"• Probabilidad Total P(Blanca): {p_b_total:.4f} (Esperado: 19/45 = {19/45:.4f})")
print(f"• P(Urna 1 | Blanca):            {posteriores[0]:.4f} (Esperado: 9/19 = {9/19:.4f})")
print(f"• P(Urna 2 | Blanca):            {posteriores[1]:.4f} (Esperado: 10/19 = {10/19:.4f})")
print(f"• P(Urna 3 | Blanca):            {posteriores[2]:.4f} (Esperado: 0.0)")

assert np.isclose(p_b_total, 19/45, atol=1e-5)
assert np.isclose(posteriores[0], 9/19, atol=1e-5)

# Visualización del Diagrama de Barras de Actualización Bayesiana
labels = ['Urna 1', 'Urna 2', 'Urna 3']
x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x - width/2, prioris, width, label='Prioris $P(U_i)$', color='#3498db')
ax.bar(x + width/2, posteriores, width, label='Posteriores $P(U_i \mid B)$', color='#2ecc71')

ax.set_title('Actualización Bayesiana tras observar "Bola Blanca"', fontsize=12, fontweight='bold')
ax.set_ylabel('Probabilidad')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.grid(True, ls='--', alpha=0.5)

plt.tight_layout()
plt.show()
""")

# --- CELL 11: RESUMEN ---
add_md(r"""---

## 5. Resumen

En esta lección hemos fundamentado los pilares analíticos de la **teoría matemática de la probabilidad**:

### Puntos Clave:
1. **Orígenes y Enfoques:** Se contextualizó el origen histórico (cartas Pascal-Fermat de 1654) y se formalizaron los enfoques Clásico / A Priori (Laplace), Frecuencial / Empírico y Subjetivo.
2. **Teoría de Conjuntos:** Se definieron las operaciones algebraicas ($\cup, \cap, \setminus, A^c$) y se demostraron las **Leyes de De Morgan** ($(A \cup B)^c = A^c \cap B^c$).
3. **Axiomas de Kolmogorov (1933):** Se estudió el marco axiomático ($P(A) \ge 0, P(\Omega)=1, P(\bigcup A_i)=\sum P(A_i)$) y sus teoremas derivados (adición general, probabilidad del complemento).
4. **Probabilidad Total y Bayes:** Se implementó el Teorema de la Probabilidad Total ($P(B) = \sum P(B \mid A_i) P(A_i)$) y el **Teorema de Bayes** ($P(A_j \mid B) = \frac{P(B \mid A_j)P(A_j)}{P(B)}$) para la actualización de hipótesis a posteriori.
""")

# --- CELL 12: BIBLIOGRAFÍA ---
add_md(r"""---

## 6. Bibliografía

1. **Carot Sánchez, T. (2014).** *Introducción a la estadística y a las probabilidades.* Editorial Universitat Politècnica de València.
2. **Casparri, M. T. (2018).** *Introducción a la probabilidad y a la estadística.* Editorial Eudeba.
3. **Huertas Sánchez, A., & Manzano Arjona, M. (2002).** *Teoría de conjuntos.* Grupo Editorial Iberoamérica.
4. **Ivorra Castillo, C.** *Teoría de conjuntos.* Universitat de València.
5. **Montes Suay, F. (2007).** *Introducción a la probabilidad.* Universitat de València.
6. **Rincón, L. (2006).** *Una introducción a la probabilidad y estadística.* Universidad Nacional Autónoma de México (UNAM).
""")

# Guardar cuaderno en la carpeta leccion-8
target_dir = os.path.join("06-estadistica-1", "leccion-8")
os.makedirs(target_dir, exist_ok=True)
output_path = os.path.join(target_dir, "introduccion-probabilidad-calculo-conceptos.ipynb")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"=== CUADERNO GENERADO EXITOSAMENTE EN: {output_path} ===")
