import pandas as pd
import numpy as np
import re

# 1. Cargar el archivo CSV
df = pd.read_csv('datos_sucios.csv')
print("--- DATOS ORIGINALES (SUCIOS) ---")
print(df)
print("\n" + "="*60 + "\n")

# Copia para no alterar el original
df_clean = df.copy()

# 2. Limpieza de nombres (Espacios en blanco adicionales)
# Trim de espacios al inicio/final y colapsar múltiples espacios internos a uno solo
df_clean['nombre'] = df_clean['nombre'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)

# 3. Tratamiento de valores faltantes y tipos incorrectos en 'edad'
# Convertir 'veinticinco' a NaN y luego a numérico
df_clean['edad'] = df_clean['edad'].replace('veinticinco', np.nan)
df_clean['edad'] = pd.to_numeric(df_clean['edad'], errors='coerce')

# 4. Manejo de duplicados
# Eliminar duplicados exactos (ej. fila de Lucía Méndez)
df_clean = df_clean.drop_duplicates()

# Eliminar duplicados en el ID (ej. María Gómez con ID 2)
# Al ordenar, la fila con edad numérica (25) se priorizará sobre la que tenía NaN
df_clean = df_clean.sort_values(by=['id', 'edad'], na_position='first')
df_clean = df_clean.drop_duplicates(subset=['id'], keep='last')

# 5. Corrección de IDs faltantes o inválidos
# El registro de Ana Ruiz tiene ID nulo. Le asignaremos el ID 4 (que está libre)
df_clean.loc[df_clean['nombre'] == 'Ana Ruiz', 'id'] = 4.0
df_clean['id'] = df_clean['id'].astype(int)

# 6. Limpieza y estandarización de 'salario'
# Remover '$', comas y espacios en blanco, y convertir 'N/A' a NaN
df_clean['salario'] = df_clean['salario'].astype(str).str.replace('$', '', regex=False)
df_clean['salario'] = df_clean['salario'].str.replace(',', '', regex=False)
df_clean['salario'] = df_clean['salario'].str.strip()
df_clean['salario'] = df_clean['salario'].replace('N/A', np.nan)
df_clean['salario'] = pd.to_numeric(df_clean['salario'], errors='coerce')

# 7. Tratamiento de anomalías y outliers en 'edad'
# Luis Fernández tiene edad -5 (edad negativa imposible) -> Reemplazar por NaN o valor absoluto
df_clean.loc[df_clean['edad'] < 0, 'edad'] = np.nan
# Pedro Pascal tiene edad 120 (outlier/error de entrada) -> Limitar a NaN o valor razonable
df_clean.loc[df_clean['edad'] > 100, 'edad'] = np.nan

# 8. Estandarización de fechas ('fecha_registro')
# Convertir a formato homogéneo YYYY-MM-DD
df_clean['fecha_registro'] = pd.to_datetime(df_clean['fecha_registro'], format='mixed', errors='coerce')

# 9. Validación y limpieza de correos electrónicos ('email')
# Limpiar espacios
df_clean['email'] = df_clean['email'].astype(str).str.strip()

# Función para validar estructura de email
def validar_email(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(patron, email):
        return email
    return np.nan  # Marcar como nulo o inválido los incorrectos

df_clean['email'] = df_clean['email'].apply(validar_email)

# Ordenar por ID para mejor presentación
df_clean = df_clean.sort_values(by='id').reset_index(drop=True)

print("--- DATOS LIMPIOS ---")
print(df_clean)

# Guardar el archivo limpio
df_clean.to_csv('datos_limpios.csv', index=False)
print("\n¡Datos limpios guardados exitosamente en 'datos_limpios.csv'!")
