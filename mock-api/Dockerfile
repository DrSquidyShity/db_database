# Basis-Image
FROM python:3.10-slim

# Arbeitsverzeichnis
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code kopieren
COPY app.py .

# Exponiere Port 5000
EXPOSE 5000

# Startbefehl
CMD ["python", "app.py"]
