FROM python:3.10-slim

# Instalar dependencias del sistema para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar e instalar librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto de Streamlit
EXPOSE 8501

# El comando se define en el docker-compose