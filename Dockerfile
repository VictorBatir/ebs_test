FROM python:3.12-slim

WORKDIR /app

# Copiază fișierele requirements.txt și instalează dependențele
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expune portul pe care aplicația Django va rula
EXPOSE 8000

# Comanda pentru a porni aplicația Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]
