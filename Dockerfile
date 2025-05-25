# Usar una imagen base de Python 3.12
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de dependencias
COPY requirements.txt ./

# Instalar las dependencias
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiar el código fuente
COPY src/ ./src/
COPY main.py ./

# Exponer el puerto que usará FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["fastapi", "run", "main.py", "--port", "8000"]
