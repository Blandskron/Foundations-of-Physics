import os
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

print("=== INICIANDO PRUEBAS DE SIMULACIÓN PARA LECCIÓN 4 ===")

# --- PROMEDIOS Y PROPIEDADES ---
datos = np.array([10.5, 12.0, 14.5, 15.0, 15.0, 18.0, 20.5, 22.0, 25.0])
pesos = np.array([1, 2, 1, 3, 2, 1, 2, 1, 1])

# 1. Media Aritmética simple
media_art = np.mean(datos)
# 2. Media Ponderada
media_pond = np.sum(datos * pesos) / np.sum(pesos)

# 3. Propiedades de la Media
# P1: Suma de desviaciones respecto a la media es cero
suma_desv = np.sum(datos - media_art)
print(f"P1 - Suma de desviaciones respecto a la media: {suma_desv:.5e} (Esperado: 0)")
assert np.isclose(suma_desv, 0, atol=1e-10)

# P2: Cambio de origen
c_orig = 5.0
assert np.isclose(np.mean(datos + c_orig), media_art + c_orig, atol=1e-10)

# P3: Cambio de escala
c_esc = 2.5
assert np.isclose(np.mean(datos * c_esc), media_art * c_esc, atol=1e-10)

# P4: Descomponibilidad
sub1 = np.array([10.5, 12.0, 14.5])
sub2 = np.array([15.0, 15.0, 18.0, 20.5, 22.0, 25.0])
media_comb = (len(sub1) * np.mean(sub1) + len(sub2) * np.mean(sub2)) / len(datos)
assert np.isclose(media_comb, media_art, atol=1e-10)

# 4. Mediana
mediana_val = np.median(datos)

# 5. Moda
moda_val = stats.mode(datos, keepdims=True).mode[0]

# 6. Media Geométrica
m_geom = stats.gmean(datos)
m_geom_art = np.exp(np.mean(np.log(datos)))
assert np.isclose(m_geom, m_geom_art, atol=1e-5)

# 7. Media Armónica
m_arm = stats.hmean(datos)
m_arm_art = len(datos) / np.sum(1.0 / datos)
assert np.isclose(m_arm, m_arm_art, atol=1e-5)

# Desigualdad fundamental H <= G <= Media
print(f"Desigualdad Promedios: H ({m_arm:.4f}) <= G ({m_geom:.4f}) <= X_bar ({media_art:.4f})")
assert m_arm <= m_geom <= media_art

# --- CUANTILES Y DATOS AGRUPADOS ---
q1 = np.percentile(datos, 25)
q2 = np.percentile(datos, 50)
q3 = np.percentile(datos, 75)
iqr_val = q3 - q1

# --- DISPERSIÓN ---
var_pob = np.var(datos, ddof=0)
std_pob = np.std(datos, ddof=0)
cv_pearson = std_pob / abs(media_art)

# Minimización del Error Cuadrático Medio en c = media
c_vals = np.linspace(media_art - 10, media_art + 10, 100)
ecm_vals = [np.mean((datos - c)**2) for c in c_vals]
c_opt = c_vals[np.argmin(ecm_vals)]
print(f"Minimización ECM: c óptimo gráfico = {c_opt:.4f} vs Media real = {media_art:.4f}")
assert np.isclose(c_opt, media_art, atol=0.2)

# --- VARIABLE TIPIFICADA (Z-SCORE) ---
z_scores = (datos - media_art) / std_pob
print(f"Z-Score - Media de Z: {np.mean(z_scores):.5e}, Varianza de Z: {np.var(z_scores):.4f}")
assert np.isclose(np.mean(z_scores), 0, atol=1e-10)
assert np.isclose(np.var(z_scores), 1, atol=1e-10)

# --- MEDIDAS DE FORMA ---
asimetria_pearson = (media_art - moda_val) / std_pob
curtosis_fisher = stats.kurtosis(datos, fisher=True)

print(f"Forma - Asimetría Pearson: {asimetria_pearson:.4f}, Curtosis Fisher: {curtosis_fisher:.4f}")

# --- RECTIFICACIÓN Y GENERACIÓN GRÁFICA DE PRUEBA ---
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Boxplot con Tukey fences
axs[0].boxplot(datos, vert=True, patch_artist=True, boxprops=dict(facecolor='#3498db', color='black'))
axs[0].set_title('Diagrama de Cajas (Boxplot)', fontweight='bold')
axs[0].set_ylabel('Valores de la Variable')
axs[0].grid(True, ls='--', alpha=0.5)

# Plot 2: Parábola de Minimización del Error Cuadrático Medio
axs[1].plot(c_vals, ecm_vals, color='#e74c3c', lw=2, label=r'$f(c) = \frac{1}{N}\sum (x_i - c)^2$')
axs[1].axvline(media_art, color='black', ls='--', label=r'Mínimo en $c = \bar{x}$')
axs[1].set_title('Propiedad de Mínimos Cuadrados de la Media', fontweight='bold')
axs[1].set_xlabel('Constante $c$')
axs[1].set_ylabel('Suma Cuadrática Media')
axs[1].legend()
axs[1].grid(True, ls='--', alpha=0.5)

plt.tight_layout()
os.makedirs("scratch", exist_ok=True)
plt.savefig("scratch/test_figura_leccion_4.png", dpi=150)
plt.close()

print("=== PRUEBAS Y GENERACIÓN DE GRÁFICOS PARA LECCIÓN 4 COMPLETADAS ===")
