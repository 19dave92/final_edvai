import os
import pickle

"""
DIRECTORIO_ACTUAL = os.getcwd() #getcwd: ruta al DIRECTORIO Actual (FINAL_EDVAI)
RUTA_MODELO = os.path.join(DIRECTORIO_ACTUAL + "/model/modelo_proyecto_final.pkl")

with open(RUTA_MODELO, 'rb') as f:
    # Lo cargamos para usarlo en otro momento. 
    model = pickle.load(f)
"""

ruta_modelo = os.path.join("model", "modelo_proyecto_final.pkl")

if os.path.exists(ruta_modelo):
    print("Encontrado!", ruta_modelo)
else:
    print("No se encontró", ruta_modelo)

