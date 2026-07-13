#!/bin/bash
# Demo ultra-simple: una línea para demostraciones rápidas
# Uso: ./demo.sh [duracion_segundos] [semilla]

DURACION=${1:-10}
SEMILLA=${2:-7}

cd "$(dirname "$0")" || exit 1
python3 run_simulation.py --duracion "$DURACION" --semilla "$SEMILLA"
