import os
import numpy as np
import matplotlib.pyplot as plt

print("=== INICIANDO PRUEBAS DE SIMULACIÓN PARA LECCIÓN 8 ===")

# --- SIMULACIÓN 1: Problema del Chevalier de Méré (1654) ---
np.random.seed(42)
n_simulaciones = 100000

# Apuesta 1: Al menos un 6 en 4 lanzamientos de 1 dado
dado_4 = np.random.randint(1, 7, size=(n_simulaciones, 4))
exito_apuesta1 = np.any(dado_4 == 6, axis=1)
prob1_empirica = np.mean(exito_apuesta1)
prob1_teorica = 1.0 - (5.0 / 6.0)**4

# Apuesta 2: Al menos un doble 6 en 24 lanzamientos de 2 dados
dados_24_d1 = np.random.randint(1, 7, size=(n_simulaciones, 24))
dados_24_d2 = np.random.randint(1, 7, size=(n_simulaciones, 24))
doble_6 = (dados_24_d1 == 6) & (dados_24_d2 == 6)
exito_apuesta2 = np.any(doble_6, axis=1)
prob2_empirica = np.mean(exito_apuesta2)
prob2_teorica = 1.0 - (35.0 / 36.0)**24

print("=== PROBLEMA HISTÓRICO DEL CHEVALIER DE MÉRÉ (1654) ===")
print(f"• Apuesta 1 (1 seis en 4 dados):  Empírica = {prob1_empirica:.4f} | Teórica = {prob1_teorica:.4f} (> 0.50 -> Rentable)")
print(f"• Apuesta 2 (Doble seis en 24):   Empírica = {prob2_empirica:.4f} | Teórica = {prob2_teorica:.4f} (< 0.50 -> Pérdida)")

assert np.isclose(prob1_empirica, prob1_teorica, atol=0.005)
assert np.isclose(prob2_empirica, prob2_teorica, atol=0.005)


# --- SIMULACIÓN 2: Verificación de las Leyes de De Morgan ---
omega = set(range(1, 11))
a = {2, 3, 5, 7}       # Números primos del 1 al 10
b = {2, 4, 6, 8, 10}   # Números pares del 1 al 10

a_c = omega - a
b_c = omega - b

# Ley de De Morgan 1: (A U B)^c == A^c ∩ B^c
left_1 = omega - (a | b)
right_1 = a_c & b_c
print(f"\nDe Morgan 1 - (A U B)^c: {left_1} == A^c AND B^c: {right_1}")
assert left_1 == right_1

# Ley de De Morgan 2: (A ∩ B)^c == A^c U B^c
left_2 = omega - (a & b)
right_2 = a_c | b_c
print(f"De Morgan 2 - (A AND B)^c: {left_2} == A^c OR B^c: {right_2}")

assert left_2 == right_2


# --- SIMULACIÓN 3: Teorema de la Probabilidad Total y Teorema de Bayes ---
class SistemaBayesiano:
    def __init__(self, prioris, verosimilitudes):
        self.prioris = np.array(prioris)
        self.verosimilitudes = np.array(verosimilitudes)
        
    def probabilidad_total(self):
        return np.sum(self.prioris * self.verosimilitudes)
        
    def posteriores(self):
        p_total = self.probabilidad_total()
        return (self.prioris * self.verosimilitudes) / p_total

# Problema oficial de las 3 Urnas:
# Prioris: P(U1) = 1/3, P(U2) = 1/3, P(U3) = 1/3
prioris_urnas = [1/3, 1/3, 1/3]
# Verosimilitudes de bola blanca B: P(B|U1)=3/5, P(B|U2)=4/6, P(B|U3)=0/3
verosimilitudes_b = [3/5, 4/6, 0/3]

bayes_urnas = SistemaBayesiano(prioris_urnas, verosimilitudes_b)
p_b_total = bayes_urnas.probabilidad_total()
posteriores_urnas = bayes_urnas.posteriores()

print("\n=== PROBABILIDAD TOTAL Y TEOREMA DE BAYES (3 URNAS) ===")
print(f"• Probabilidad Total P(Blanca): {p_b_total:.4f} (Esperado: 19/45 = {19/45:.4f})")
print(f"• Posterior P(U1 | Blanca):    {posteriores_urnas[0]:.4f} (Esperado: 9/19 = {9/19:.4f})")
print(f"• Posterior P(U2 | Blanca):    {posteriores_urnas[1]:.4f} (Esperado: 10/19 = {10/19:.4f})")
print(f"• Posterior P(U3 | Blanca):    {posteriores_urnas[2]:.4f} (Esperado: 0.0)")

assert np.isclose(p_b_total, 19/45, atol=1e-5)
assert np.isclose(posteriores_urnas[0], 9/19, atol=1e-5)
assert np.isclose(posteriores_urnas[1], 10/19, atol=1e-5)
assert np.isclose(posteriores_urnas[2], 0.0, atol=1e-5)


# --- GENERACIÓN GRÁFICA DE VERIFICACIÓN ---
fig, axs = plt.subplots(1, 2, figsize=(13, 5))

# Plot 1: Convergencia de Monte Carlo para la Apuesta 1 del Méré
n_pasos = np.logspace(1, 5, 100, dtype=int)
medias_conv = [np.mean(exito_apuesta1[:n]) for n in n_pasos]

axs[0].plot(n_pasos, medias_conv, color='#1f77b4', lw=2, label='Frecuencia Relativa Empírica')
axs[0].axhline(prob1_teorica, color='red', ls='--', lw=2, label=f'Probabilidad Teórica ({prob1_teorica:.4f})')
axs[0].axhline(0.50, color='black', ls=':', label='Umbral del 50%')
axs[0].set_xscale('log')
axs[0].set_title('Convergencia Frecuencial (Problema Chevalier de Méré)', fontweight='bold')
axs[0].set_xlabel('Número de Simulaciones $N$ (Escala Log)')
axs[0].set_ylabel('Probabilidad Estimada')
axs[0].legend()
axs[0].grid(True, which='both', ls='--', alpha=0.5)

# Plot 2: Probabilidades a Priori vs a Posteriori en el Teorema de Bayes
urnas_labels = ['Urna 1', 'Urna 2', 'Urna 3']
x_bar = np.arange(len(urnas_labels))
width = 0.35

axs[1].bar(x_bar - width/2, prioris_urnas, width, label='Prioris P(U_i)', color='#3498db')
axs[1].bar(x_bar + width/2, posteriores_urnas, width, label='Posteriores P(U_i | Blanca)', color='#2ecc71')
axs[1].set_xticks(x_bar)
axs[1].set_xticklabels(urnas_labels)
axs[1].set_title('Actualización Bayesiana de Probabilidades tras observar "Bola Blanca"', fontweight='bold')
axs[1].set_ylabel('Probabilidad')
axs[1].legend()
axs[1].grid(True, ls='--', alpha=0.5)

plt.tight_layout()
os.makedirs("scratch", exist_ok=True)
plt.savefig("scratch/test_figura_leccion_8.png", dpi=150)
plt.close()

print("=== PRUEBAS Y GENERACIÓN DE GRÁFICOS PARA LECCIÓN 8 COMPLETADAS EXITOSAMENTE ===")
