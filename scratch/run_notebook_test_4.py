import json
import sys

nb_path = r"06-estadistica-1\leccion-4\medidas-resumen-datos-1.ipynb"

print(f"=== EJECUTANDO PRUEBA INTEGRAL DEL CUADERNO: {nb_path} ===")

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

global_env = {}

for idx, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code":
        code = "".join(cell["source"])
        print(f"--- Ejecutando Celda de Código #{idx + 1} ---")
        try:
            exec(code, global_env)
        except Exception as e:
            print(f"ERROR EN CELDA {idx + 1}: {e}")
            sys.exit(1)

print("=== TODAS LAS CELDAS DE CÓDIGO SE EJECUTARON EXITOSAMENTE EN LA LECCIÓN 4 ===")
