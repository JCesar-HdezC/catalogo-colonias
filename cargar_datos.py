import pandas as pd
import sqlite3
import os

# Leer el Excel
excel_path = os.path.join(os.path.dirname(__file__), 'COLONIAS.xlsx')
df = pd.read_excel(excel_path)

# Crear/conectar a la base de datos
db_path = os.path.join(os.path.dirname(__file__), 'colonias.db')
conn = sqlite3.connect(db_path)

# Guardar el DataFrame en SQLite
df.to_sql('colonias', conn, if_exists='replace', index=False)

print(f"✓ Base de datos creada con {len(df)} registros")
print(f"✓ Estados únicos: {df['edo'].nunique()}")
print(f"✓ Municipios únicos: {df['mun'].nunique()}")

conn.close()
