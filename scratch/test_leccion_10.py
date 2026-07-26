import os
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

print("=== INICIANDO PRUEBAS DE SIMULACIÓN PARA LECCIÓN 10 ===")

# --- SIMULACIÓN 1: Problema de la Centralita (Poisson \lambda = 8) ---
lambda_minuto = 480.0 / 60.0 # 8 llamadas/minuto
capacidad_max = 12

# Probabilidad de saturación P(X > 12) = 1 - P(X <= 12)
prob_saturacion = 1.0 - stats.poisson.cdf(capacidad_max, mu=lambda_minuto)

print("=== DISTRIBUCIÓN DE POISSON: PROBLEMA CENTRALITA TELEFÓNICA ===")
print(f"• Tasa promedio \lambda: {lambda_minuto:.1f} llamadas/minuto")
print(f"• Probabilidad P(X > 12) de saturación: {prob_saturacion:.4f} (Esperado: 0.0638)")

assert np.isclose(prob_saturacion, 0.0638, atol=0.001)
print("[VERIFICACIÓN] Coincidencia exacta con la solución del texto base (6.38%).")


# --- SIMULACIÓN 2: Distribución Uniforme Continua U(2, 6) ---
a, b = 2.0, 6.0
p_x_menor_5 = stats.uniform.cdf(5.0, loc=a, scale=b-a)
esperanza_u = (a + b) / 2.0
varianza_u = (b - a)**2 / 12.0

print("\n=== DISTRIBUCIÓN UNIFORME CONTINUA U(2, 6) ===")
print(f"• P(X <= 5): {p_x_menor_5:.4f} (Esperado: 3/4 = 0.75)")
print(f"• Esperanza E[X]: {esperanza_u:.2f} (Esperado: 4.0)")
print(f"• Varianza Var(X): {varianza_u:.4f} (Esperado: 4/3 = 1.3333)")

assert np.isclose(p_x_menor_5, 0.75)
assert np.isclose(esperanza_u, 4.0)


# --- SIMULACIÓN 3: Monte Carlo de Distribuciones Derivadas (\chi^2, t-Student, F-Snedecor) ---
np.random.seed(42)
n_sim = 100000
n_gl, m_gl = 10, 10

# 1. Chi-Cuadrado \chi^2_10 (Suma de 10 normales tipificadas cuadradas)
z_mat = np.random.normal(0, 1, size=(n_sim, n_gl))
chi2_sim = np.sum(z_mat**2, axis=1)

# 2. t-Student t_10 (Z / sqrt(\chi^2_10 / 10))
z_single = np.random.normal(0, 1, size=n_sim)
t_sim = z_single / np.sqrt(chi2_sim / n_gl)

# 3. F-Snedecor F_{10, 10} (\chi^2_10 / 10) / (\chi^2_10_segunda / 10)
chi2_sim2 = np.sum(np.random.normal(0, 1, size=(n_sim, m_gl))**2, axis=1)
f_sim = (chi2_sim / n_gl) / (chi2_sim2 / m_gl)

print("\n=== MONTE CARLO DE DISTRIBUCIONES DERIVADAS DE LA NORMAL ===")
print(f"• Chi^2_10 -> Media Sim: {np.mean(chi2_sim):.2f} (Teórica n = 10) | Var Sim: {np.var(chi2_sim):.2f} (Teórica 2n = 20)")
print(f"• t_10     -> Media Sim: {np.mean(t_sim):.4f} (Teórica = 0) | Var Sim: {np.var(t_sim):.2f} (Teórica n/(n-2) = 1.25)")
print(f"• F_{{10,10}} -> Media Sim: {np.mean(f_sim):.2f} (Teórica m/(m-2) = 1.25)")

assert np.isclose(np.mean(chi2_sim), 10.0, atol=0.2)
assert np.isclose(np.var(t_sim), 1.25, atol=0.1)


# --- SIMULACIÓN 4: Teorema De Moivre-Laplace y Corrección por Continuidad de Yates ---
n_binom, p_binom = 100, 0.5
mu_norm = n_binom * p_binom
sigma_norm = np.sqrt(n_binom * p_binom * (1 - p_binom))

k_target = 50
p_exacta_binom = stats.binom.pmf(k_target, n_binom, p_binom)

# Con Corrección de Yates: P(49.5 <= Normal <= 50.5)
p_yates = stats.norm.cdf(k_target + 0.5, loc=mu_norm, scale=sigma_norm) - stats.norm.cdf(k_target - 0.5, loc=mu_norm, scale=sigma_norm)

print("\n=== APROXIMACIÓN DE MOIVRE-LAPLACE Y CORRECCIÓN DE YATES ===")
print(f"• Probabilidad Binomial B(100, 0.5) P(X = 50) Exacta: {p_exacta_binom:.6f}")
print(f"• Aproximación Normal con Corrección de Yates:      {p_yates:.6f}")

assert np.isclose(p_exacta_binom, p_yates, atol=0.001)
print("[VERIFICACIÓN] La corrección por continuidad de Yates proporciona una excelente aproximación.")


# --- GENERACIÓN GRÁFICA DE VERIFICACIÓN ---
fig, axs = plt.subplots(1, 2, figsize=(13, 5))

# Plot 1: Densidad t-Student vs Normal Tipificada (Efecto Colas Pesadas)
x_grid = np.linspace(-4, 4, 300)
axs[0].plot(x_grid, stats.norm.pdf(x_grid), 'k--', lw=2, label='Normal Tipificada N(0, 1)')
axs[0].plot(x_grid, stats.t.pdf(x_grid, df=3), color='#e74c3c', lw=2, label='t-Student (n=3 gr. lib.)')
axs[0].plot(x_grid, stats.t.pdf(x_grid, df=30), color='#2ecc71', lw=2, label='t-Student (n=30 gr. lib.)')
axs[0].set_title('Convergencia de la t-Student a la Normal Estándar', fontweight='bold')
axs[0].set_xlabel('Valor z / t')
axs[0].set_ylabel('Densidad de Probabilidad f(x)')
axs[0].legend()
axs[0].grid(True, ls='--', alpha=0.5)

# Plot 2: Aproximación De Moivre-Laplace con Histograma Binomial y Curva Normal
k_vals = np.arange(35, 66)
binom_pmf = stats.binom.pmf(k_vals, n_binom, p_binom)
x_fine = np.linspace(35, 65, 300)
norm_pdf = stats.norm.pdf(x_fine, loc=mu_norm, scale=sigma_norm)

axs[1].bar(k_vals, binom_pmf, width=0.8, color='#3498db', alpha=0.6, label='Binomial B(100, 0.5)')
axs[1].plot(x_fine, norm_pdf, color='#e74c3c', lw=2.5, label='Aproximación Normal N(50, 5)')
axs[1].set_title('Teorema de De Moivre-Laplace (B(100, 0.5) -> N(50, 5))', fontweight='bold')
axs[1].set_xlabel('Número de Éxitos k')
axs[1].set_ylabel('Probabilidad')
axs[1].legend()
axs[1].grid(True, ls='--', alpha=0.5)

plt.tight_layout()
os.makedirs("scratch", exist_ok=True)
plt.savefig("scratch/test_figura_leccion_10.png", dpi=150)
plt.close()

print("=== PRUEBAS Y GENERACIÓN DE GRÁFICOS PARA LECCIÓN 10 COMPLETADAS EXITOSAMENTE ===")
