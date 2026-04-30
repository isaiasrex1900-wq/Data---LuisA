FROM python:3.10-slim

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2 y DuckDB
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY analitycs
COPY dashboard


# EXPORE el puerto 8501 (el que usa Streamlit por defecto)
EXPOSE 8501

# Mantener el contenedor vivo para ejecutar scripts manualmente
# O puedes cambiarlo para que arranque el dashboard directamente
CMD ["tail", "-f", "/dev/null"]