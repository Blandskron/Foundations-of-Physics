import os
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

print("=== INICIANDO PRUEBAS DE SIMULACIÓN PARA LECCIÓN 7 ===")

# --- SIMULACIÓN 1: Selección de Esquema (Aditivo vs Multiplicativo) ---
np.random.seed(42)
t_axis = np.arange(1, 61) # 5 años (60 meses)
tendencia_teorica = 100.0 + 1.5 * t_axis

# Componente estacional multiplicativa (patrón mensual)
patron_estacional = np.array([0.85, 0.90, 0.95, 1.00, 1.05, 1.15, 1.25, 1.20, 1.10, 1.00, 0.90, 0.85])
estacionalidad_mult = np.tile(patron_estacional, 5)

y_multiplicativa = tendencia_teorica * estacionalidad_mult + np.random.normal(0, 3, 60)

# Cómputo de Medias y Desviaciones Típicas Anuales
medias_anuales = []
stds_anuales = []
for a in range(5):
    sub_y = y_multiplicativa[a*12 : (a+1)*12]
    medias_anuales.append(np.mean(sub_y))
    stds_anuales.append(np.std(sub_y, ddof=1))

b1_disp, b0_disp, r_disp, _, _ = stats.linregress(medias_anuales, stds_anuales)

print("=== CRITERIO DE SELECCIÓN DE ESQUEMA (REGRESIÓN DE DISPERSIÓN) ===")
print(f"• Medias Anuales: {np.round(medias_anuales, 2).tolist()}")
print(f"• Desviaciones Anuales: {np.round(stds_anuales, 2).tolist()}")
print(f"• Pendiente b1: {b1_disp:.4f} (Positiva -> Indica Esquema Multiplicativo)")
assert b1_disp > 0.05


# --- SIMULACIÓN 2: Medias Móviles y Alisado Exponencial ---
# Medias Móviles Centradas de orden 12 (MM12)
def medias_moviles_centradas_12(y):
    n = len(y)
    mm = np.full(n, np.nan)
    for t in range(6, n - 6):
        # Filtro ponderado: 0.5 en extremos, 1 en el centro
        ventana = y[t-6 : t+7]
        pesos = np.array([0.5] + [1.0]*11 + [0.5])
        mm[t] = np.sum(ventana * pesos) / 12.0
    return mm

# Alisado Exponencial Simple (alpha = 0.3)
def alisado_exponencial(y, alpha=0.3):
    n = len(y)
    me = np.zeros(n)
    me[0] = y[0]
    for t in range(1, n):
        me[t] = alpha * y[t] + (1 - alpha) * me[t-1]
    return me

mm12_vals = medias_moviles_centradas_12(y_multiplicativa)
me_vals = alisado_exponencial(y_multiplicativa, alpha=0.3)

print("=== EXTRACCIÓN DE TENDENCIA (MEDIAS MÓVILES Y ALISADO) ===")
print(f"• MM12 t=30: {mm12_vals[30]:.2f} (Tendencia real t=30: {tendencia_teorica[29]:.2f})")
print(f"• Alisado Exponencial t=30: {me_vals[30]:.2f}")
assert np.isclose(mm12_vals[30], tendencia_teorica[29], atol=10.0)


# --- SIMULACIÓN 3: Números Índices Compuestos (Laspeyres, Paasche, Fisher) ---
# 5 Bienes en Período Base (0) y Período Actual (t)
p0 = np.array([2.5, 10.0, 1.2, 5.0, 15.0])
q0 = np.array([100,  20, 150, 40,  10])

pt = np.array([3.0, 12.0, 1.5, 4.8, 18.0]) # Precios aumentaron
qt = np.array([90,   18, 160, 45,   8]) # Cantidades ajustadas por consumidor

# Cómputo de Índices Ponderados
laspeyres = (np.sum(pt * q0) / np.sum(p0 * q0)) * 100.0
paasche   = (np.sum(pt * qt) / np.sum(p0 * qt)) * 100.0
fisher    = np.sqrt(laspeyres * paasche)
indice_valor = (np.sum(pt * qt) / np.sum(p0 * q0)) * 100.0

print("=== CALCULADORA DE ÍNDICES COMPUESTOS PONDERADOS ===")
print(f"• Índice de Laspeyres (L^P): {laspeyres:.2f}")
print(f"• Índice de Paasche (P^P):   {paasche:.2f}")
print(f"• Índice de Fisher (F^P):    {fisher:.2f}")
print(f"• Índice de Valor (IV):      {indice_valor:.2f}")

# Verificación de la relación Paasche <= Fisher <= Laspeyres (Efecto Sustitución)
assert paasche <= fisher <= laspeyres
print("[VERIFICACIÓN] Se satisface la ordenación Paasche <= Fisher <= Laspeyres.")


# --- SIMULACIÓN 4: IPC y Deflación de Series Económicas ---
ipc_base = 100.0
ipc_serie = np.array([100.0, 102.5, 106.0, 110.2]) # Inflación acumulada
salario_nominal = np.array([1500.0, 1530.0, 1560.0, 1600.0]) # Aumentos nominales

salario_real = (salario_nominal / ipc_serie) * 100.0

print("=== DEFLACIÓN DE SALARIOS A PRECIOS CONSTANTES ===")
for t in range(4):
    print(f"• Año {t}: Nominal = {salario_nominal[t]:.2f}€ | IPC = {ipc_serie[t]:.1f} | Real (Constante) = {salario_real[t]:.2f}€")

# El poder adquisitivo real en t=3 disminuyó respecto a t=0 a pesar del aumento nominal
assert salario_real[-1] < salario_real[0]
print("[CONCLUSIÓN] La deflación revela una pérdida real del poder adquisitivo a pesar del incremento nominal.")


# --- GENERACIÓN GRÁFICA DE VERIFICACIÓN ---
fig, axs = plt.subplots(1, 2, figsize=(13, 5))

# Plot 1: Serie Temporal Descompuesta y Tendencia MM12 / Alisado
axs[0].plot(t_axis, y_multiplicativa, color='#3498db', alpha=0.5, label='Serie Original $Y_t$')
axs[0].plot(t_axis, mm12_vals, color='#e74c3c', lw=2.5, label='Tendencia $MM_{12}$')
axs[0].plot(t_axis, me_vals, color='#2ecc71', ls='--', lw=2, label=r'Alisado Exponencial ($\alpha=0.3$)')
axs[0].set_title('Extracción de la Tendencia en Serie Temporal', fontweight='bold')
axs[0].set_xlabel('Mes $t$')
axs[0].set_ylabel('Valor de la Variable')
axs[0].legend()
axs[0].grid(True, ls='--', alpha=0.5)

# Plot 2: Salario Nominal vs Salario Real Deflactado
anios = [2020, 2021, 2022, 2023]
axs[1].plot(anios, salario_nominal, marker='o', color='#2ecc71', lw=2, label='Salario Nominal (€ Corrientes)')
axs[1].plot(anios, salario_real, marker='s', color='#e74c3c', lw=2, label='Salario Real (€ Constantes Base 2020)')
axs[1].set_title('Efecto de la Deflación por el IPC sobre el Poder Adquisitivo', fontweight='bold')
axs[1].set_xlabel('Año')
axs[1].set_ylabel('Euros (€)')
axs[1].legend()
axs[1].grid(True, ls='--', alpha=0.5)

plt.tight_layout()
os.makedirs("scratch", exist_ok=True)
plt.savefig("scratch/test_figura_leccion_7.png", dpi=150)
plt.close()

print("=== PRUEBAS Y GENERACIÓN DE GRÁFICOS PARA LECCIÓN 7 COMPLETADAS EXITOSAMENTE ===")
