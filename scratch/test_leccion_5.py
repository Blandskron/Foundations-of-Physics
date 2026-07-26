import os
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

print("=== INICIANDO PRUEBAS DE SIMULACIÓN PARA LECCIÓN 5 ===")

# --- SIMULACIÓN 1: Detector de Tukey y Barreras de Boxplot ---
datos = np.array([12, 15, 18, 19, 20, 21, 22, 23, 25, 28, 45, 65]) # Contiene atípico moderado (45) y extremo (65)
q1, q3 = np.percentile(datos, [25, 75])
rq = q3 - q1

lim_int_inf = q1 - 1.5 * rq
lim_int_sup = q3 + 1.5 * rq
lim_ext_inf = q1 - 3.0 * rq
lim_ext_sup = q3 + 3.0 * rq

atipicos_moderados = datos[((datos < lim_int_inf) & (datos >= lim_ext_inf)) | ((datos > lim_int_sup) & (datos <= lim_ext_sup))]
atipicos_extremos = datos[(datos < lim_ext_inf) | (datos > lim_ext_sup)]

print(f"Tukey - Q1: {q1:.1f}, Q3: {q3:.1f}, RQ: {rq:.1f}")
print(f"Tukey - Barreras Interiores: [{lim_int_inf:.1f}, {lim_int_sup:.1f}]")
print(f"Tukey - Barreras Exteriores:  [{lim_ext_inf:.1f}, {lim_ext_sup:.1f}]")
print(f"Tukey - Atípicos Moderados: {atipicos_moderados.tolist()}")
print(f"Tukey - Atípicos Extremos:  {atipicos_extremos.tolist()}")

assert 45 in atipicos_moderados
assert 65 in atipicos_extremos


# --- SIMULACIÓN 2: Test de Grubbs para Detección de Outliers ---
def test_grubbs(x, alpha=0.05):
    n = len(x)
    mean_x = np.mean(x)
    std_x = np.std(x, ddof=1)
    abs_dev = np.abs(x - mean_x)
    max_idx = np.argmax(abs_dev)
    g_stat = abs_dev[max_idx] / std_x
    
    t_crit = stats.t.ppf(1 - alpha / (2 * n), df=n - 2)
    g_crit = ((n - 1) / np.sqrt(n)) * np.sqrt(t_crit**2 / (n - 2 + t_crit**2))
    
    is_outlier = g_stat > g_crit
    return is_outlier, x[max_idx], g_stat, g_crit

es_outlier, val_outlier, g_calc, g_critico = test_grubbs(datos)
print(f"Grubbs - Valor máx: {val_outlier}, G_calc: {g_calc:.4f}, G_crit: {g_critico:.4f}, ¿Outlier?: {es_outlier}")
assert es_outlier and val_outlier == 65


# --- SIMULACIÓN 3: Caso Empírico OCDE (1985) - Inflación en 24 países ---
ocde_data = np.array([2.2, 7.6, 2.9, 4.6, 4.1, 3.9, 7.4, 3.2, 5.1, 5.3, 20.1, 2.3, 5.5, 32.7, 9.1, 1.7, 3.2, 5.8, 16.3, 15.9, 5.9, 6.7, 3.4, 40.5])
ocde_log = np.log(ocde_data)

skew_orig = stats.skew(ocde_data)
skew_log = stats.skew(ocde_log)

print(f"OCDE (1985) - Asimetría Original: {skew_orig:.4f} (Fuertemente positiva)")
print(f"OCDE (1985) - Asimetría Logarítmica: {skew_log:.4f} (Simetrizada cerca de 0)")

assert skew_orig > 1.5
assert abs(skew_log) < 0.8



# --- SIMULACIÓN 4: Teorema del Cambio de Variable (Continuas) ---
np.random.seed(42)
u_samples = np.random.uniform(0, 1, size=50000)
y_samples = u_samples**2 # Y = X^2

# Densidad analítica f_Y(y) = 1 / (2 * sqrt(y))
y_grid = np.linspace(0.01, 0.99, 200)
fy_analitica = 1.0 / (2.0 * np.sqrt(y_grid))

# Histograma empírico para verificación
counts, bin_edges = np.histogram(y_samples, bins=50, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
fy_empirica = 1.0 / (2.0 * np.sqrt(bin_centers))

error_cambio_var = np.mean(np.abs(counts - fy_empirica))
print(f"Cambio de Variable - Error Absoluto Medio Empírico vs Analítico: {error_cambio_var:.4f}")
assert error_cambio_var < 0.15


# --- GENERACIÓN GRÁFICA DE VERIFICACIÓN ---
fig, axs = plt.subplots(2, 2, figsize=(12, 9))

# Panel 1: Boxplot con Tukey fences y atípicos
axs[0, 0].boxplot(datos, orientation='horizontal', patch_artist=True, boxprops=dict(facecolor='#3498db', alpha=0.7))
axs[0, 0].axvline(lim_int_sup, color='orange', linestyle='--', label=r'Límite Interior ($1.5 \cdot RQ$)')
axs[0, 0].axvline(lim_ext_sup, color='red', linestyle=':', label=r'Límite Exterior ($3 \cdot RQ$)')
axs[0, 0].set_title('Clasificación de Atípicos (Tukey)', fontweight='bold')
axs[0, 0].legend(fontsize=8)
axs[0, 0].grid(True, ls='--', alpha=0.5)

# Panel 2: Histograma OCDE Original vs Log
axs[0, 1].hist(ocde_data, bins=10, alpha=0.6, color='red', label=f'Original ($g_1={skew_orig:.2f}$)')
axs[0, 1].set_title('Distribución de Inflación OCDE 1985', fontweight='bold')
axs[0, 1].set_xlabel('Tasa de Inflación (%)')
axs[0, 1].legend()
axs[0, 1].grid(True, ls='--', alpha=0.5)

# Panel 3: Histograma Log-Transformado
axs[1, 0].hist(ocde_log, bins=10, alpha=0.6, color='green', label=fr'Transformado $\ln(X)$ ($g_1={skew_log:.2f}$)')
axs[1, 0].set_title('Simetrización mediante Transformación Logarítmica', fontweight='bold')
axs[1, 0].set_xlabel(r'$\ln(\text{Inflación})$')
axs[1, 0].legend()

axs[1, 0].grid(True, ls='--', alpha=0.5)

# Panel 4: Teorema del Cambio de Variable
axs[1, 1].hist(y_samples, bins=50, density=True, alpha=0.5, color='purple', label='Simulación Empírica $Y=X^2$')
axs[1, 1].plot(y_grid, fy_analitica, 'r-', lw=2, label=r'Densidad Analítica $f_Y(y) = \frac{1}{2\sqrt{y}}$')
axs[1, 1].set_title(r'Teorema del Cambio de Variable: $Y = X^2$', fontweight='bold')
axs[1, 1].set_xlabel('$y$')
axs[1, 1].set_ylabel('$f_Y(y)$')
axs[1, 1].legend()
axs[1, 1].grid(True, ls='--', alpha=0.5)

plt.tight_layout()
os.makedirs("scratch", exist_ok=True)
plt.savefig("scratch/test_figura_leccion_5.png", dpi=150)
plt.close()

print("=== PRUEBAS Y GENERACIÓN DE GRÁFICOS PARA LECCIÓN 5 COMPLETADAS EXITOSAMENTE ===")
