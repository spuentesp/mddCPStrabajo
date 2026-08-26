# Instalación de Dependencias — SVIF Simulation

## Problema

Tu sistema no tiene `pip` instalado. Python está disponible pero sin el gestor de paquetes.

## Soluciones

### ✅ Opción 1: Instalar pip (recomendado)

```bash
# Arch/Manjaro
sudo pacman -S python-pip

# Ubuntu/Debian  
sudo apt install python3-pip

# Fedora
sudo dnf install python3-pip

# Después instala paho-mqtt
pip install --user paho-mqtt
```

### ✅ Opción 2: Instalar con el gestor del sistema

Más simple, pero menos flexible. Solo instala paho-mqtt sin pip:

```bash
# Arch/Manjaro
sudo pacman -S python-paho-mqtt

# Ubuntu/Debian
sudo apt install python3-paho-mqtt

# Fedora
sudo dnf install python3-paho-mqtt
```

### ✅ Opción 3: Entorno Virtual (sin sudo)

Si no tienes acceso a sudo, crea un entorno virtual:

```bash
cd mddCPStrabajo/semana-4

# Crea entorno virtual
python3 -m venv venv

# Activa
source venv/bin/activate

# Instala dentro del venv
python3 -m pip install paho-mqtt

# Ahora ejecuta la simulación
python3 run_simulation.py

# Cuando termines, desactiva:
deactivate
```

---

## ¿Ya instalaste?

Verifica que funcione:

```bash
python3 -c "import paho.mqtt.client; print('✓ paho-mqtt OK')"
```

Si ves `✓ paho-mqtt OK`, ejecuta:

```bash
cd mddCPStrabajo/semana-4
python3 run_simulation.py
```
