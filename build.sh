#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos
python manage.py collectstatic --no-input

# Ejecutar migraciones
python manage.py migrate

# Poblar la base de datos si SEED_DB está activo
if [ "$SEED_DB" = "True" ] || [ "$SEED_DB" = "true" ]; then
    echo "Poblando base de datos con datos iniciales (seed)..."
    python seed_db.py
fi
