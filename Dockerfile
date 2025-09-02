# ====== Base slim (producción) ======
FROM python:3.11-slim-bookworm

# Ajustes de entorno para prod / headless
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    MPLBACKEND=Agg

WORKDIR /app

# Dependencias del sistema necesarias para WeasyPrint (Cairo/Pango/GDK) y fuentes
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 \
    libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    fonts-dejavu fontconfig \
  && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Copiar código
COPY . /app

# Usuario no root (buena práctica en contenedores)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Cloud Run escucha el puerto definido en $PORT (8080 por defecto)
EXPOSE 8080

# ⚠️ IMPORTANTE: ajuste el módulo según su entrypoint real:
#  - si su app está en app/main.py      →  "app.main:app"
#  - si su app está en init_fastapi.py  →  "init_fastapi:app"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
