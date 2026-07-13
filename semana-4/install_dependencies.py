#!/usr/bin/env python3
"""
Script para instalar dependencias de SVIF Simulation.
Intenta múltiples métodos y proporciona instrucciones detalladas.
"""
import subprocess
import sys
import os


def run_cmd(cmd, desc=""):
    """Ejecuta comando y retorna si fue exitoso."""
    print(f"  🔍 Intentando: {desc or ' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"  ✓ Éxito: {desc}")
            return True
        else:
            err = result.stderr[:80] if result.stderr else result.stdout[:80]
            print(f"    ⚠️  Error: {err}")
            return False
    except subprocess.TimeoutExpired:
        print(f"    ⏱️  Timeout")
        return False
    except Exception as e:
        print(f"    ❌ Excepción: {e}")
        return False


def main():
    print("=" * 60)
    print("🔧 Instalador de Dependencias — SVIF Simulation")
    print("=" * 60)

    print("\n📦 Intentando instalar paho-mqtt...\n")

    strategies = [
        (["python3", "-m", "pip", "install", "--user", "paho-mqtt"],
         "python3 -m pip install --user paho-mqtt"),

        (["python3", "-m", "pip", "install", "paho-mqtt"],
         "python3 -m pip install paho-mqtt"),

        (["pip3", "install", "--user", "paho-mqtt"],
         "pip3 install --user paho-mqtt"),

        (["pip", "install", "--user", "paho-mqtt"],
         "pip install --user paho-mqtt"),
    ]

    # Intenta stratégias sin privilegios
    for cmd, desc in strategies:
        if run_cmd(cmd, desc):
            print("\n✅ paho-mqtt instalado correctamente")
            return 0

    # Si todo falla, proporciona instrucciones
    print("\n" + "=" * 60)
    print("❌ No se pudo instalar automáticamente")
    print("=" * 60)

    print("\n📋 OPCIONES DE INSTALACIÓN MANUAL:\n")

    print("Opción 1: pip (sin sudo):")
    print("  pip3 install --user paho-mqtt")
    print("  # O:")
    print("  python3 -m pip install --user paho-mqtt\n")

    print("Opción 2: gestor de paquetes del sistema (requiere sudo):")
    print("  # Arch/Manjaro:")
    print("  sudo pacman -S python-paho-mqtt")
    print("  # Ubuntu/Debian:")
    print("  sudo apt install python3-paho-mqtt")
    print("  # Fedora:")
    print("  sudo dnf install python3-paho-mqtt\n")

    print("Opción 3: entorno virtual (recomendado si no tienes permisos):")
    print("  python3 -m venv venv")
    print("  source venv/bin/activate")
    print("  pip install paho-mqtt")
    print("  # Luego ejecuta el simulador dentro del venv\n")

    print("=" * 60)
    print("\nℹ️  Una vez instalado, ejecuta:")
    print("  python3 run_simulation.py\n")

    return 1


if __name__ == "__main__":
    sys.exit(main())
