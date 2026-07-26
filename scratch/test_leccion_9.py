import os
import numpy as np
import matplotlib.pyplot as plt

print("=== INICIANDO PRUEBAS DE SIMULACIÓN PARA LECCIÓN 9 ===")

# --- SIMULACIÓN 1: Mapeo de Variable Aleatoria (Lanzamiento de 3 Monedas) ---
np.random.seed(42)
n_simulaciones = 100000
lanzamientos = np.random.choice([0, 1], size=(n_simulaciones, 3)) # 0: Cruz, 1: Cara
x_caras = np.sum(lanzamientos, axis=1)

prob_empirica_caras = [np.mean(x_caras == k) for k in range(4)]
prob_teorica_caras = [1/8, 3/8, 3/8, 1/8]

print("=== VARIABLE ALEATORIA X: NÚMERO DE CARAS EN 3 MONEDAS ===")
for k in range(4):
    print(f"• P(X = {k}): Empírica = {prob_empirica_caras[k]:.4f} | Teórica = {prob_teorica_caras[k]:.4f}")
    assert np.isclose(prob_empirica_caras[k], prob_teorica_caras[k], atol=0.005)

media_monedas_teorica = np.sum(np.arange(4) * np.array(prob_teorica_caras)) # 1.5
var_monedas_teorica = np.sum((np.arange(4)**2) * np.array(prob_teorica_caras)) - media_monedas_teorica**2 # 0.75

assert np.isclose(media_monedas_teorica, 1.5)
assert np.isclose(var_monedas_teorica, 0.75)


# --- SIMULACIÓN 2: Clase VariableAleatoriaDiscreta y Ejemplo de las Edades (pág. 9) ---
class VariableAleatoriaDiscreta:
    def __init__(self, x_vals, p_vals):
        self.x = np.array(x_vals, dtype=float)
        self.p = np.array(p_vals, dtype=float)
        # Normalización por seguridad
        self.p = self.p / np.sum(self.p)
        
    def esperanza(self):
        return np.sum(self.x * self.p)
        
    def varianza(self):
        mu = self.esperanza()
        return np.sum((self.x - mu)**2 * self.p)
        
    def desviacion_tipica(self):
        return np.sqrt(self.varianza())
        
    def funcion_acumulada(self, x_eval):
        return np.sum(self.p[self.x <= x_eval])

# Datos empíricos de las edades (Tabla 5, pág. 9)
edades = [12, 13, 14, 15, 16, 17, 18]
frecuencias_edades = [9, 25, 27, 16, 12, 8, 3]

va_edades = VariableAleatoriaDiscreta(edades, np.array(frecuencias_edades)/100.0)

mu_edades = va_edades.esperanza()
var_edades = va_edades.varianza()
sigma_edades = va_edades.desviacion_tipica()

print("\n=== VERIFICACIÓN DEL EJEMPLO DE EDADES (PÁG. 9 DEL PDF) ===")
print(f"• Media Esperanza \mu:      {mu_edades:.2f} años (PDF: 14.33)")
print(f"• Varianza \sigma^2:        {var_edades:.4f} (PDF: 2.34)")
print(f"• Desviación Típica \sigma: {sigma_edades:.2f} años (PDF: 1.53)")

assert np.isclose(mu_edades, 14.33, atol=0.01)
assert np.isclose(sigma_edades, 1.53, atol=0.01)


# --- SIMULACIÓN 3: Dado Asimétrico (Tabla 6, pág. 9) ---
dado_x = [1, 5, 6]
dado_p = [1/6, 2/6, 3/6]

va_dado = VariableAleatoriaDiscreta(dado_x, dado_p)
mu_dado = va_dado.esperanza()
var_dado = va_dado.varianza()

print("\n=== DADO ASIMÉTRICO (TABLA 6, PÁG. 9) ===")
print(f"• P(X=1) = {va_dado.p[0]:.4f}, P(X=5) = {va_dado.p[1]:.4f}, P(X=6) = {va_dado.p[2]:.4f}")
print(f"• Esperanza E[X]: {mu_dado:.4f} (Esperado: 29/6 = {29/6:.4f})")
print(f"• Varianza Var(X): {var_dado:.4f}")

assert np.isclose(mu_dado, 29/6)


# --- GENERACIÓN GRÁFICA DE VERIFICACIÓN ---
fig, axs = plt.subplots(1, 2, figsize=(13, 5))

# Plot 1: Función de Masa ( Bastones) del Dado Asimétrico
axs[0].stem(dado_x, dado_p, linefmt='b-', markerfmt='bo', basefmt='r-')
axs[0].set_title('Función de Masa p(x) (Dado Asimétrico)', fontweight='bold')
axs[0].set_xlabel('Valor de la Variable X')
axs[0].set_ylabel('Probabilidad P(X = x)')
axs[0].set_xticks(dado_x)
axs[0].grid(True, ls='--', alpha=0.5)

# Plot 2: Función de Distribución Acumulada Escalonada F(x) de las Edades
x_grid = np.linspace(11, 19, 500)
f_grid = [va_edades.funcion_acumulada(x_i) for x_i in x_grid]

axs[1].step(x_grid, f_grid, where='post', color='#e74c3c', lw=2.5)
axs[1].set_title('Función de Distribución Acumulada Escalonada F(x)', fontweight='bold')
axs[1].set_xlabel('Edad (x)')
axs[1].set_ylabel('Probabilidad Acumulada F(x) = P(X <= x)')
axs[1].axhline(0.5, color='black', ls='--', alpha=0.6, label='Mediana (F(Me) = 0.5)')
axs[1].legend()
axs[1].grid(True, ls='--', alpha=0.5)

plt.tight_layout()
os.makedirs("scratch", exist_ok=True)
plt.savefig("scratch/test_figura_leccion_9.png", dpi=150)
plt.close()

print("=== PRUEBAS Y GENERACIÓN DE GRÁFICOS PARA LECCIÓN 9 COMPLETADAS EXITOSAMENTE ===")
