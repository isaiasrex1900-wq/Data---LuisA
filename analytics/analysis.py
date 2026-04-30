import duckdb
import pandas as pd
import os

def run_analytics():
    # Crear carpeta de salida si no existe
    os.makedirs('analytics/output', exist_ok=True)
    
    # Conectar a DuckDB
    con = duckdb.connect()
    
    # 1. Cargar los nuevos CSVs (asegúrate que los nombres coincidan con generate_data.py)
    try:
        contestants = pd.read_csv('contestants.csv')
        teams = pd.read_csv('teams.csv')
        
        # Registrar los DataFrames en DuckDB para usarlos como tablas SQL
        con.register('contestants', contestants)
        con.register('team', teams)
        
        # 2. Consulta OLAP: Distribución de participantes por equipo (Requisito Track A)
        # Usamos tus nuevos nombres: tem_id y con_id
        query = """
        SELECT t.tem_name as equipo, COUNT(c.con_id) as total_participantes
        FROM team t
        LEFT JOIN contestants c ON t.tem_id = c.tem_id
        GROUP BY t.tem_name
        ORDER BY total_participantes DESC
        """
        
        result = con.execute(query).df()
        
        # 3. Guardar a formato Parquet (Requisito indispensable para la evaluación)
        result.to_parquet('analytics/output/distribucion_participantes.parquet')
        
        print("-O- Análisis completado. Archivo Parquet generado en analytics/output/")
        
    except FileNotFoundError:
        print("-X- Error: No se encontraron los archivos CSV. Ejecuta primero generate_data.py")

if __name__ == "__main__":
    run_analytics()