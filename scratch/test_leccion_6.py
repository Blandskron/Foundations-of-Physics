import os
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

print("=== INICIANDO PRUEBAS DE SIMULACIÓN PARA LECCIÓN 6 ===")

# --- SIMULACIÓN 1: Tabla de Contingencia y Distribuciones Marginales/Condicionales ---
# Matriz de frecuencias 3x3 de ejemplo (Nivel de Estudios X vs Nivel de Ingresos Y)
x_vals = np.array([1, 2, 3]) # 1: Primaria, 2: Secundaria, 3: Universidad
y_vals = np.array([10, 25, 50]) # 10k, 25k, 50k €

tabla_freq = np.array([
    [50, 20, 10], # Total Primaria: 80
    [30, 60, 30], # Total Secundaria: 120
    [10, 40, 100] # Total Universidad: 150
])
N_total = np.sum(tabla_freq) # 350

n_i_dot = np.sum(tabla_freq, axis=1) # Frecuencias marginales X: [80, 120, 150]
n_dot_j = np.sum(tabla_freq, axis=0) # Frecuencias marginales Y: [90, 120, 140]

f_ij = tabla_freq / N_total
f_i_dot = n_i_dot / N_total
f_dot_j = n_dot_j / N_total

# Medias Marginales
media_x = np.sum(x_vals * f_i_dot)
media_y = np.sum(y_vals * f_dot_j)

# Varianzas Marginales
var_x = np.sum((x_vals - media_x)**2 * f_i_dot)
var_y = np.sum((y_vals - media_y)**2 * f_dot_j)
std_x = np.sqrt(var_x)
std_y = np.sqrt(var_y)

# Medias Condicionales X | Y=y_j
media_x_dado_y = np.array([np.sum(x_vals * (tabla_freq[:, j] / n_dot_j[j])) for j in range(len(y_vals))])

# Prueba del Teorema de la Esperanza Total: Media(X) = Suma( Media(X|Y=yj) * f_dot_j )
esperanza_total_x = np.sum(media_x_dado_y * f_dot_j)

print(f"Marginales X - Media: {media_x:.4f}, Varianza: {var_x:.4f}")
print(f"Marginales Y - Media: {media_y:.4f}, Varianza: {var_y:.4f}")
print(f"Medias Condicionales X|Y: {media_x_dado_y.round(4).tolist()}")
print(f"Esperanza Total X: {esperanza_total_x:.4f} == Media X: {media_x:.4f}")
assert np.isclose(esperanza_total_x, media_x, atol=1e-10)


# --- SIMULACIÓN 2: Chi-Cuadrado y Contingencia de Pearson ---
chi2_scipy, p_val, dof, expected = stats.chi2_contingency(tabla_freq)

# Cálculo artesanal de Chi-Cuadrado
expected_art = np.outer(n_i_dot, n_dot_j) / N_total
chi2_art = np.sum((tabla_freq - expected_art)**2 / expected_art)
c_contingencia_art = np.sqrt(chi2_art / (N_total + chi2_art))

print(f"Chi2 Artesanal: {chi2_art:.4f} == SciPy: {chi2_scipy:.4f}")
print(f"Coeficiente de Contingencia C: {c_contingencia_art:.4f}")
assert np.isclose(chi2_art, chi2_scipy, atol=1e-5)


# --- SIMULACIÓN 3: Covarianza, Correlación de Pearson e Incorrelación No Lineal ---
# Cómputo de Covarianza S_XY artesanal
cov_xy_art = np.sum(np.outer(x_vals - media_x, y_vals - media_y) * f_ij)
r_xy_art = cov_xy_art / (std_x * std_y)

print(f"Covarianza S_XY: {cov_xy_art:.4f}")
print(f"Correlación r_XY: {r_xy_art:.4f}")

# Prueba de Incorrelación (S_XY = 0) en relación parabólica determinista Y = X^2
x_parabola = np.array([-2, -1, 0, 1, 2])
y_parabola = x_parabola**2 # Y = {4, 1, 0, 1, 4}

cov_parabola = np.mean((x_parabola - np.mean(x_parabola)) * (y_parabola - np.mean(y_parabola)))
r_parabola, _ = stats.pearsonr(x_parabola, y_parabola)

print(f"Parábola Y=X^2 - Covarianza: {cov_parabola:.5e}, Correlación Pearson: {r_parabola:.5e}")
assert np.isclose(cov_parabola, 0, atol=1e-10)
assert np.isclose(r_parabola, 0, atol=1e-10)


# --- SIMULACIÓN 4: Correlación Espuria y Variable Confusora ---
np.random.seed(42)
n_muestras = 200
temperatura = np.random.normal(loc=30, scale=5, size=n_muestras) # Variable confusora Z

ventas_helados = 2.0 * temperatura + np.random.normal(loc=0, scale=2, size=n_muestras) # Variable X
ahogamientos = 1.5 * temperatura + np.random.normal(loc=0, scale=3, size=n_muestras)    # Variable Y

r_espuria, _ = stats.pearsonr(ventas_helados, ahogamientos)
print(f"Correlación Espuria (Helados vs Ahogamientos): r = {r_espuria:.4f} (Muy alta por factor Temperatura)")
assert r_espuria > 0.85


# --- GENERACIÓN GRÁFICA DE VERIFICACIÓN ---
fig, axs = plt.subplots(1, 2, figsize=(13, 5))

# Plot 1: Parábola determinista sin correlación lineal
axs[0].scatter(x_parabola, y_parabola, color='#e74c3c', s=100, zorder=3)
axs[0].plot(np.linspace(-2.2, 2.2, 100), np.linspace(-2.2, 2.2, 100)**2, 'r--', label=r'Relación Cuadrática $Y=X^2$')
axs[0].axhline(np.mean(y_parabola), color='blue', ls=':', label=r'Media de Y ($\bar{y}=1.6$)')
axs[0].axvline(np.mean(x_parabola), color='green', ls=':', label=r'Media de X ($\bar{x}=0$)')
axs[0].set_title(f'Dependencia Funcional Perfecta con $r_{{XY}} = {r_parabola:.1f}$', fontweight='bold')
axs[0].set_xlabel('Variable X')
axs[0].set_ylabel('Variable Y')
axs[0].legend()
axs[0].grid(True, ls='--', alpha=0.5)

# Plot 2: Correlación Espuria por Variable Confusora
sc = axs[1].scatter(ventas_helados, ahogamientos, c=temperatura, cmap='viridis', s=40, alpha=0.8)
cbar = plt.colorbar(sc, ax=axs[1])
cbar.set_label('Temperatura Exterior (°C)')
axs[1].set_title(f'Correlación Espuria ($r_{{XY}} = {r_espuria:.2f}$)', fontweight='bold')
axs[1].set_xlabel('Ventas de Helados (k€)')
axs[1].set_ylabel('Incidentes en Playas')
axs[1].grid(True, ls='--', alpha=0.5)

plt.tight_layout()
os.makedirs("scratch", exist_ok=True)
plt.savefig("scratch/test_figura_leccion_6.png", dpi=150)
plt.close()

print("=== PRUEBAS Y GENERACIÓN DE GRÁFICOS PARA LECCIÓN 6 COMPLETADAS EXITOSAMENTE ===")
