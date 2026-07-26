import os
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

print("=== INICIANDO PRUEBAS DE SIMULACIÓN PARA LECCIÓN 3 ===")

# --- SIMULACIÓN 1: Ley de los Grandes Números (LGN) ---
np.random.seed(42)
mu_poblacional = 4.25
sigma_poblacional = 0.75
n_muestras = 50000

muestras = np.random.normal(loc=mu_poblacional, scale=sigma_poblacional, size=n_muestras)
medias_acumuladas = np.cumsum(muestras) / np.arange(1, n_muestras + 1)
n_puntos = np.arange(1, n_muestras + 1)
error_estandar_banda = sigma_poblacional / np.sqrt(n_puntos)

print(f"LGN - Muestra total: {n_muestras}, Media final: {medias_acumuladas[-1]:.4f} (Esperado: {mu_poblacional})")
assert np.isclose(medias_acumuladas[-1], mu_poblacional, atol=0.01)


# --- SIMULACIÓN 2: Engine de Hoja de Cálculo Artesanal ---
class HojaDeCalculoArtesanal:
    def __init__(self):
        self.datos = {}
    
    def agregar_columna(self, nombre, valores):
        self.datos[nombre] = [float(x) for x in valores]
    
    def media(self, nombre_columna):
        vals = self.datos[nombre_columna]
        return sum(vals) / len(vals)
    
    def mediana(self, nombre_columna):
        vals = sorted(self.datos[nombre_columna])
        n = len(vals)
        mid = n // 2
        if n % 2 == 0:
            return (vals[mid - 1] + vals[mid]) / 2.0
        else:
            return vals[mid]
            
    def moda(self, nombre_columna):
        vals = self.datos[nombre_columna]
        frecuencias = {}
        for x in vals:
            frecuencias[x] = frecuencias.get(x, 0) + 1
        max_freq = max(frecuencias.values())
        modas = [k for k, v in frecuencias.items() if v == max_freq]
        return modas[0] if len(modas) == 1 else modas

    def varianza_muestral(self, nombre_columna):
        vals = self.datos[nombre_columna]
        m = self.media(nombre_columna)
        n = len(vals)
        return sum((x - m) ** 2 for x in vals) / (n - 1)

    def desviacion_tipica_muestral(self, nombre_columna):
        return self.varianza_muestral(nombre_columna) ** 0.5

    def rango(self, nombre_columna):
        vals = self.datos[nombre_columna]
        return max(vals) - min(vals)
        
    def buscar_v(self, valor_buscado, col_busqueda, col_retorno):
        vals_b = self.datos[col_busqueda]
        vals_r = self.datos[col_retorno]
        for b, r in zip(vals_b, vals_r):
            if b == valor_buscado:
                return r
        return None

# Validar HojaDeCalculoArtesanal
sheet = HojaDeCalculoArtesanal()
arr_test = np.array([12.5, 15.0, 18.2, 14.8, 22.1, 15.0, 19.4, 16.3, 15.0, 21.0])
sheet.agregar_columna("ventas", arr_test)
sheet.agregar_columna("id", range(1, 11))

m_art = sheet.media("ventas")
m_np = np.mean(arr_test)
print(f"Media Artesanal: {m_art:.4f}, Numpy: {m_np:.4f}")
assert np.isclose(m_art, m_np, atol=1e-5)

med_art = sheet.mediana("ventas")
med_np = np.median(arr_test)
print(f"Mediana Artesanal: {med_art:.4f}, Numpy: {med_np:.4f}")
assert np.isclose(med_art, med_np, atol=1e-5)

var_art = sheet.varianza_muestral("ventas")
var_np = np.var(arr_test, ddof=1)
print(f"Varianza Muestral Artesanal: {var_art:.4f}, Numpy: {var_np:.4f}")
assert np.isclose(var_art, var_np, atol=1e-5)

std_art = sheet.desviacion_tipica_muestral("ventas")
std_np = np.std(arr_test, ddof=1)
print(f"Desviación Típica Artesanal: {std_art:.4f}, Numpy: {std_np:.4f}")
assert np.isclose(std_art, std_np, atol=1e-5)

bv_res = sheet.buscar_v(5, "id", "ventas")
print(f"BUSCARV ID=5 -> Ventas: {bv_res} (Esperado: 22.1)")
assert np.isclose(bv_res, 22.1, atol=1e-5)


# --- SIMULACIÓN 3: Limpieza y Filtro de Outliers (IQR vs Z-score) ---
datos_crudos = np.array([120, 130, 125, 128, 132, 129, 121, 127, 950, 124, 131, -40, 126])
q1 = np.percentile(datos_crudos, 25)
q3 = np.percentile(datos_crudos, 75)
iqr = q3 - q1
limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr
datos_depurados = datos_crudos[(datos_crudos >= limite_inferior) & (datos_crudos <= limite_superior)]
print(f"Outliers filtrados con IQR: {datos_crudos[~((datos_crudos >= limite_inferior) & (datos_crudos <= limite_superior))]}")
print(f"Media depurada: {np.mean(datos_depurados):.2f} vs Media cruda: {np.mean(datos_crudos):.2f}")


# --- SIMULACIÓN 4: Representación Gráfica (Los 4 gráficos del tema) ---
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Gráfico 1: Evolución del Comercio Electrónico (2013-2019)
anios_g1 = [2013, 2014, 2015, 2016, 2017, 2018, 2019]
ventas_g1 = [145000, 160000, 185000, 215000, 248000, 275000, 307000]
compras_g1 = [140000, 152000, 170000, 192000, 218000, 240000, 260000]

axs[0, 0].plot(anios_g1, ventas_g1, marker='o', color='#1f77b4', linewidth=2.5, label='Volumen de ventas')
axs[0, 0].plot(anios_g1, compras_g1, marker='s', color='#ff7f0e', linewidth=2.5, label='Volumen de compras')
axs[0, 0].set_title('Gráfico 1: Volumen de compras y ventas por comercio electrónico (M€)', fontsize=11, fontweight='bold')
axs[0, 0].set_xlabel('Año')
axs[0, 0].set_ylabel('Millones de Euros (€)')
axs[0, 0].grid(True, ls='--', alpha=0.6)
axs[0, 0].legend()

# Gráfico 2: Inmersión de las TIC en el mercado laboral (2019 vs 2020)
categorias_g2 = ['Empleados TIC', 'Uso internet', 'Uso ordenador']
v2019 = [17.4, 53.5, 60.0]
v2020 = [18.4, 57.1, 65.0]
y_pos = np.arange(len(categorias_g2))
height = 0.35

axs[0, 1].barh(y_pos - height/2, v2019, height, label='2019', color='#3498db')
axs[0, 1].barh(y_pos + height/2, v2020, height, label='2020', color='#e74c3c')
axs[0, 1].set_yticks(y_pos)
axs[0, 1].set_yticklabels(categorias_g2)
axs[0, 1].set_xlabel('Porcentaje (%)')
axs[0, 1].set_title('Gráfico 2: Inmersión de las TIC en el mercado laboral', fontsize=11, fontweight='bold')
axs[0, 1].grid(True, ls='--', alpha=0.6)
axs[0, 1].legend()

# Gráfico 3: Distribución de las ventas por comercio electrónico (2019)
etiquetas_g3 = ['España\n(81.1%)', 'Europa\n(14.5%)', 'Otros países\n(4.4%)']
porcentajes_g3 = [81.1, 14.5, 4.4]
colores_g3 = ['#2ecc71', '#3498db', '#9b59b6']
explode_g3 = (0.05, 0, 0)

axs[1, 0].pie(porcentajes_g3, labels=etiquetas_g3, autopct='%1.1f%%', startangle=140, colors=colores_g3, explode=explode_g3, wedgeprops=dict(width=0.6, edgecolor='w'))
axs[1, 0].set_title('Gráfico 3: Distribución de ventas por comercio electrónico', fontsize=11, fontweight='bold')

# Gráfico 4: Uso de ordenadores por la población (2006-2018)
anios_g4 = [2006, 2008, 2010, 2012, 2014, 2016, 2018]
u_12m = [65, 69, 72, 75, 78, 80, 83]
u_3m = [58, 62, 66, 70, 73, 76, 79]
u_alguna = [68, 72, 75, 78, 81, 83, 86]
u_nunca = [37, 32, 28, 24, 20, 18, 16]

axs[1, 1].scatter(anios_g4, u_12m, color='#2980b9', label='Uso últimos 12 meses', marker='o')
axs[1, 1].plot(anios_g4, u_12m, color='#2980b9', ls='--', alpha=0.7)
axs[1, 1].scatter(anios_g4, u_3m, color='#d35400', label='Uso últimos 3 meses', marker='s')
axs[1, 1].plot(anios_g4, u_3m, color='#d35400', ls='--', alpha=0.7)
axs[1, 1].scatter(anios_g4, u_alguna, color='#27ae60', label='Alguna vez han utilizado', marker='^')
axs[1, 1].plot(anios_g4, u_alguna, color='#27ae60', ls='--', alpha=0.7)
axs[1, 1].scatter(anios_g4, u_nunca, color='#7f8c8d', label='Nunca han utilizado', marker='x')
axs[1, 1].plot(anios_g4, u_nunca, color='#7f8c8d', ls=':', alpha=0.7)

axs[1, 1].set_title('Gráfico 4: Uso de ordenadores por la población (2006-2018)', fontsize=11, fontweight='bold')
axs[1, 1].set_xlabel('Año')
axs[1, 1].set_ylabel('Porcentaje de la Población (%)')
axs[1, 1].grid(True, ls='--', alpha=0.6)
axs[1, 1].legend(fontsize=8)

plt.tight_layout()
os.makedirs("scratch", exist_ok=True)
plt.savefig("scratch/test_figura_leccion_3.png", dpi=150)
plt.close()

print("=== PRUEBAS Y GENERACIÓN DE GRÁFICOS COMPLETADAS CON ÉXITO ===")
