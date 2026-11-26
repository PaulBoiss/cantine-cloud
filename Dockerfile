# syntax=docker/dockerfile:1

# Étape 1 : installer les dépendances (outils de build absents de l'image finale)
FROM python:3.12-slim@sha256:191083cdf6c7bda8c76158983163ead5d5cf7b77cf3033e805bb0f5296f51b4b AS build
WORKDIR /build
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Étape 2 : l'image finale, minimale, sans secret, sans root
FROM python:3.12-slim@sha256:191083cdf6c7bda8c76158983163ead5d5cf7b77cf3033e805bb0f5296f51b4b
RUN useradd --create-home --uid 10001 cantine
WORKDIR /srv
COPY --from=build /install /usr/local
COPY --chown=10001:10001 app/ ./app/
USER 10001
ENV DB_PATH=/tmp/cantine.db
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')"]
# Forme exec : gunicorn est le PID 1 et reçoit le SIGTERM de docker stop
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.app:app"]
