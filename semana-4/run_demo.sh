#!/bin/bash
# Demo ejecutora one-shot para simulación SVIF (Semana 4)
# Maneja instalación de dependencias y ejecución

set -e

cd "$(dirname "$0")"

echo "🔬 SVIF Simulation Demo Runner"
echo "=============================="

# Detecta gestor de paquetes
if command -v pip3 &> /dev/null; then
    PIP=pip3
elif command -v pip &> /dev/null; then
    PIP=pip
else
    echo "❌ pip no encontrado. Instala Python 3 + pip:"
    echo "   Ubuntu/Debian: sudo apt-get install python3-pip"
    echo "   Fedora: sudo dnf install python3-pip"
    exit 1
fi

# Instala paho-mqtt si no está disponible
if ! python3 -c "import paho.mqtt" 2>/dev/null; then
    echo "📦 Instalando paho-mqtt..."
    $PIP install -q paho-mqtt || {
        echo "❌ Error instalando paho-mqtt"
        exit 1
    }
fi

# Obtiene duración (por defecto 12s)
DURACION=${1:-12}
SEMILLA=${2:-7}

# Ejecuta el simulador
python3 - "$DURACION" "$SEMILLA" << 'PYTHON_EOF'
import sys
import subprocess
import socket
import time

duracion = int(sys.argv[1]) if len(sys.argv) > 1 else 12
semilla = int(sys.argv[2]) if len(sys.argv) > 2 else 7
broker = "localhost"
port = 1883

def is_port_open(host, port, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex((host, port)) == 0

# Inicia broker MQTT con Docker
print("🚀 Iniciando broker MQTT...")
try:
    subprocess.run(["docker", "--version"], capture_output=True, check=True, timeout=2)
    try:
        subprocess.run(["docker", "stop", "svif-broker"], capture_output=True, timeout=2)
    except:
        pass

    broker_proc = subprocess.Popen(
        ["docker", "run", "-it", "--rm", "--name", "svif-broker",
         "-p", f"{port}:1883", "eclipse-mosquitto:2",
         "mosquitto", "-c", "/mosquitto-no-auth.conf"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(2)
except Exception as e:
    print(f"⚠️  Docker no disponible: {e}")
    print("   Asumiendo broker local...")
    broker_proc = None

# Espera a que el broker esté listo
for i in range(10):
    if is_port_open(broker, port):
        print(f"✓ Broker listo en {broker}:{port}")
        break
    time.sleep(0.5)
else:
    print("❌ No se puede conectar al broker MQTT")
    sys.exit(1)

# Ejecuta simulación
print(f"\n📊 Simulando SVIF por {duracion}s (semilla={semilla})...\n")
from pathlib import Path

# run_demo.sh hace `cd` a su propio directorio (semana-4/) antes de invocar
# este script, así que el repo raíz es el directorio padre del cwd.
sim_path = Path.cwd().parent / "recursos-comunes" / "herramientas" / "simular_sistema.py"

if not sim_path.exists():
    print("❌ No se encontró simular_sistema.py")
    sys.exit(1)

try:
    result = subprocess.run(
        ["python3", str(sim_path), "--broker", broker, "--port", str(port),
         "--duracion", str(duracion), "--semilla", str(semilla)],
        timeout=duracion + 10
    )
except subprocess.TimeoutExpired:
    print("❌ Simulación excedió timeout")
    result = None

# Limpieza
if broker_proc:
    try:
        subprocess.run(["docker", "stop", "svif-broker"], timeout=2, capture_output=True)
    except:
        pass

print("\n✅ Demo completada" if result and result.returncode == 0 else "\n❌ Error en simulación")
sys.exit(result.returncode if result else 1)
PYTHON_EOF
