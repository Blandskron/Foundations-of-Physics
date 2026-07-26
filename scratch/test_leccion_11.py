import os
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

print("=== INICIANDO PRUEBAS DEL PIPELINE MASTER CONSOLIDADO DEL MÓDULO 6 (LECCIÓN 11) ===")

class MasterPipelineEstadistica:
    """
    Pipeline Integrador Maestro del Módulo 6: Estadística I.
    Ejecuta de forma secuencial los 3 pilares del módulo:
    Pilar 1: Análisis Exploratorio Univariante y Depuración EDA
    Pilar 2: Análisis Bivariante y Series Temporales
    Pilar 3: Teoría de Probabilidad e Inferencia Distribucional
    """
    def __init__(self, data_univariante, data_bivariante_x, data_bivariante_y, serie_temporal, ipc_serie):
        self.u_data = np.array(data_univariante, dtype=float)
        self.b_x = np.array(data_bivariante_x, dtype=float)
        self.b_y = np.array(data_bivariante_y, dtype=float)
        self.serie_t = np.array(serie_temporal, dtype=float)
        self.ipc = np.array(ipc_serie, dtype=float)
        
    def ejecutar_pilar_1(self):
        # 1. Promedios
        mean_val = np.mean(self.u_data)
        median_val = np.median(self.u_data)
        g_mean = stats.gmean(self.u_data)
        h_mean = stats.hmean(self.u_data)
        
        # Desigualdad clasica H <= G <= Mean
        assert h_mean <= g_mean <= mean_val
        
        # 2. Atípicos por Tukey
        q1, q3 = np.percentile(self.u_data, [25, 75])
        iqr = q3 - q1
        valla_inf, valla_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outliers = self.u_data[(self.u_data < valla_inf) | (self.u_data > valla_sup)]
        
        # 3. Transformación simetrizadora ln(X)
        u_log = np.log(self.u_data)
        skew_orig = stats.skew(self.u_data)
        skew_log = stats.skew(u_log)
        
        return {
            "mean": mean_val, "median": median_val, "gmean": g_mean, "hmean": h_mean,
            "outliers_count": len(outliers), "skew_orig": skew_orig, "skew_log": skew_log
        }
        
    def ejecutar_pilar_2(self):
        # 1. Correlación de Pearson y Covarianza
        cov_xy = np.cov(self.b_x, self.b_y)[0, 1]
        r_xy, _ = stats.pearsonr(self.b_x, self.b_y)
        
        # 2. Selección de Esquema Estacional por Regresión de Dispersión Anual
        # Asumiendo serie de 60 meses (5 años)
        n_años = len(self.serie_t) // 12
        medias_a, stds_a = [], []
        for a in range(n_años):
            sub_y = self.serie_t[a*12 : (a+1)*12]
            medias_a.append(np.mean(sub_y))
            stds_a.append(np.std(sub_y, ddof=1))
        b1_disp, _, _, p_val, _ = stats.linregress(medias_a, stds_a)
        esquema = "Multiplicativo" if (b1_disp > 0.05 and p_val < 0.05) else "Aditivo"
        
        # 3. Deflación económica
        serie_real = (self.serie_t[-len(self.ipc):] / self.ipc) * 100.0
        
        return {
            "cov": cov_xy, "r_xy": r_xy, "b1_disp": b1_disp, "esquema": esquema,
            "serie_real_final": serie_real[-1]
        }
        
    def ejecutar_pilar_3(self):
        # 1. Teorema de Bayes (Problema 3 Urnas oficial)
        prioris = np.array([1/3, 1/3, 1/3])
        verosimilitudes = np.array([3/5, 4/6, 0/3]) # Bola blanca
        p_total = np.sum(prioris * verosimilitudes)
        posteriores = (prioris * verosimilitudes) / p_total
        
        # 2. De Moivre-Laplace con Yates B(100, 0.5) P(X = 50)
        p_exacta_binom = stats.binom.pmf(50, 100, 0.5)
        mu_norm, sigma_norm = 50.0, np.sqrt(25.0)
        p_yates = stats.norm.cdf(50.5, mu_norm, sigma_norm) - stats.norm.cdf(49.5, mu_norm, sigma_norm)
        
        return {
            "p_total_blanca": p_total, "p_u1_posterior": posteriores[0],
            "p_exacta_binom": p_exacta_binom, "p_yates": p_yates
        }

# --- EJECUCIÓN INTEGRADA DEL PIPELINE MASTER ---
np.random.seed(42)

# Datos univariantes con asimetría positiva y atípicos
d_uni = np.concatenate([np.random.lognormal(mean=1.5, sigma=0.5, size=95), [45.0, 52.0, 60.0]])

# Datos bivariantes
d_x = np.random.uniform(5, 45, 100)
d_y = 2.0 + 0.18 * d_x + np.random.normal(0, 1.2, 100)

# Serie temporal de 5 años (60 meses) multiplicativa
t_axis = np.arange(1, 61)
tend = 100.0 + 2.0 * t_axis
est_patron = np.tile([0.85, 0.9, 0.95, 1.0, 1.05, 1.15, 1.25, 1.2, 1.1, 1.0, 0.9, 0.85], 5)
s_temp = tend * est_patron + np.random.normal(0, 3, 60)

# Serie de IPC (4 años)
ipc_arr = np.array([100.0, 103.1, 108.9, 112.5])

master = MasterPipelineEstadistica(d_uni, d_x, d_y, s_temp, ipc_arr)

res1 = master.ejecutar_pilar_1()
res2 = master.ejecutar_pilar_2()
res3 = master.ejecutar_pilar_3()

print("=== RESULTADOS DEL PIPELINE MASTER CONSOLIDADO (MÓDULO 6) ===")
print("\n--- PILAR 1: DESCRIPTIVA Y EDA ---")
print(f"• Media: {res1['mean']:.2f} | Mediana: {res1['median']:.2f} | Geométrica: {res1['gmean']:.2f} | Armónica: {res1['hmean']:.2f}")
print(f"• Atípicos Tukey detectados: {res1['outliers_count']}")
print(f"• Asimetría Original: {res1['skew_orig']:.2f} -> Tras ln(X): {res1['skew_log']:.2f} (Simetrizado)")

print("\n--- PILAR 2: BIVARIANTE Y TEMPORAL ---")
print(f"• Correlación Pearson r_XY: {res2['r_xy']:.4f}")
print(f"• Regresión Dispersión Pendiente b1: {res2['b1_disp']:.4f} -> Esquema: {res2['esquema']}")
print(f"• Valor Deflactado Final: {res2['serie_real_final']:.2f}")

print("\n--- PILAR 3: PROBABILIDAD E INFERENCIA ---")
print(f"• Probabilidad Total Blanca: {res3['p_total_blanca']:.4f} (Esperado 19/45 = {19/45:.4f})")
print(f"• Bayes P(U1 | Blanca):     {res3['p_u1_posterior']:.4f} (Esperado 9/19 = {9/19:.4f})")
print(f"• Binomial B(100, 0.5) P(X=50) Exacta: {res3['p_exacta_binom']:.6f} == Yates: {res3['p_yates']:.6f}")

assert res1['hmean'] <= res1['gmean'] <= res1['mean']
assert res2['esquema'] == "Multiplicativo"
assert np.isclose(res3['p_total_blanca'], 19/45, atol=1e-5)
assert np.isclose(res3['p_u1_posterior'], 9/19, atol=1e-5)
assert np.isclose(res3['p_exacta_binom'], res3['p_yates'], atol=0.001)

# --- GENERACIÓN DE LA FIGURA DE RECORRIDO INTEGRAL ---
fig, axs = plt.subplots(2, 2, figsize=(13, 10))

# 1. EDA: Histograma original vs Log-transformado
axs[0, 0].hist(d_uni, bins=15, color='#e74c3c', alpha=0.6, label=f'Original (Asimetría={res1["skew_orig"]:.2f})')
axs[0, 0].set_title('Pilar I: Depuración EDA y Simetrización por ln(X)', fontweight='bold')
axs[0, 0].set_xlabel('Valor X')
axs[0, 0].set_ylabel('Frecuencia')
axs[0, 0].legend()
axs[0, 0].grid(True, ls='--', alpha=0.5)

# 2. Bivariante: Scatter Plot de datos cuadráticos e incorrelación
x_quad = np.linspace(-3, 3, 50)
y_quad = x_quad**2
axs[0, 1].scatter(x_quad, y_quad, color='#9b59b6', s=40, label=r'Parábola $Y=X^2$ ($r_{XY}=0$)')
axs[0, 1].set_title('Pilar II: Dependencia Funcional sin Correlación Lineal', fontweight='bold')
axs[0, 1].set_xlabel('X')
axs[0, 1].set_ylabel('Y')
axs[0, 1].legend()
axs[0, 1].grid(True, ls='--', alpha=0.5)

# 3. Series Temporales: Descomposición y Tendencia MM12
axs[1, 0].plot(t_axis, s_temp, color='#3498db', alpha=0.5, label='Serie Observada')
axs[1, 0].set_title('Pilar II: Análisis Temporal y Tendencia', fontweight='bold')
axs[1, 0].set_xlabel('Mes')
axs[1, 0].set_ylabel('Valor')
axs[1, 0].legend()
axs[1, 0].grid(True, ls='--', alpha=0.5)

# 4. Probabilidad: Actualización Bayesiana 3 Urnas
urnas = ['U1 (3B, 2R)', 'U2 (4B, 2R)', 'U3 (0B, 3R)']
x_u = np.arange(3)
axs[1, 1].bar(x_u - 0.15, [1/3, 1/3, 1/3], width=0.3, label='Priori P(U_i)', color='#3498db')
axs[1, 1].bar(x_u + 0.15, [9/19, 10/19, 0], width=0.3, label='Posterior P(U_i | B)', color='#2ecc71')
axs[1, 1].set_title('Pilar III: Actualización Bayesiana (3 Urnas)', fontweight='bold')
axs[1, 1].set_xticks(x_u)
axs[1, 1].set_xticklabels(urnas)
axs[1, 1].set_ylabel('Probabilidad')
axs[1, 1].legend()
axs[1, 1].grid(True, ls='--', alpha=0.5)

plt.tight_layout()
os.makedirs("scratch", exist_ok=True)
plt.savefig("scratch/test_figura_leccion_11.png", dpi=150)
plt.close()

print("\n=== PIPELINE MASTER INTEGRADO EJECUTADO Y VERIFICADO EXITOSAMENTE AL 100% ===")
