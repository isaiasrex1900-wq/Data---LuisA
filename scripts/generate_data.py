import pandas as pd
from faker import Faker
import random

fake = Faker()

def generate_data(n_teams=10, n_contestants=40, n_judges=5):
    # 1. Generar Equipos (tem_id: T001, T002...)
    teams = []
    team_ids = [f"T{i:03}" for i in range(1, n_teams + 1)]
    for tid in team_ids:
        teams.append({
            'tem_id': tid,
            'tem_name': fake.company()
        })
    
    # 2. Generar Concursantes (con_id: C001...)
    contestants = []
    for i in range(1, n_contestants + 1):
        contestants.append({
            'con_id': f"C{i:03}",
            'con_name': fake.name(),
            'cell': fake.phone_number(),
            'tem_id': random.choice(team_ids)
        })

    # 3. Generar Jueces (jd_id: J001...)
    judges = []
    judge_ids = [f"J{i:03}" for i in range(1, n_judges + 1)]
    for jid in judge_ids:
        judges.append({
            'jd_id': jid,
            'jd_name': fake.name(),
            'tem_id': random.choice(team_ids)
        })

    # 4. Generar Proyectos (pro_id: P001...)
    projects = []
    for i, tid in enumerate(team_ids):
        projects.append({
            'pro_id': f"P{i+1:03}",
            'pro_name': f"Project {fake.word().capitalize()}",
            'tem_id': tid,
            'status': 'Idea' # Estado inicial requerido para el historial [cite: 47]
        })

    # Guardar a CSV
    pd.DataFrame(teams).to_csv('teams.csv', index=False)
    pd.DataFrame(contestants).to_csv('contestants.csv', index=False)
    pd.DataFrame(judges).to_csv('judges.csv', index=False)
    pd.DataFrame(projects).to_csv('projects.csv', index=False)
    
    print(" Archivos CSV generados con éxito.")

if __name__ == "__main__":
    generate_data()