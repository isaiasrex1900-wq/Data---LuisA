import pandas as pd
from sqlalchemy import create_engine
import time

def ingest():
    # Configuración de conexión (debe coincidir con tu docker-compose)
    # DB_HOST debe ser el nombre del servicio en el yaml (ej: 'db')
    engine = create_engine('postgresql://user_admin:secret_password@db:5432/hackathon_db')

    files_and_tables = [
        ('teams.csv', 'team'),
        ('judges.csv', 'judges'),
        ('contestants.csv', 'contestants'),
        ('projects.csv', 'proyects') # Nota: en tu SQL escribiste 'proyects'
    ]

    print("🚀 Iniciando ingesta masiva...")
    
    for file, table in files_and_tables:
        try:
            df = pd.read_csv(file)
            # 'method=multi' mejora el rendimiento de la ingesta masiva [cite: 22]
            df.to_sql(table, engine, if_exists='append', index=False, method='multi')
            print(f"✔️ Tabla '{table}' cargada correctamente.")
        except Exception as e:
            print(f"❌ Error al cargar {table}: {e}")

if __name__ == "__main__":
    # Esperar un poco a que la DB esté lista para recibir conexiones
    time.sleep(5) 
    ingest()