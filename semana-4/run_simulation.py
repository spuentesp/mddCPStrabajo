#!/usr/bin/env python3
"""
Ejecutor de simulación SVIF con verbosidad detallada.
One-shot: verifica dependencias, inicia broker, ejecuta y valida.

Uso:
    python3 run_simulation.py                    # 12s, Docker automático
    python3 run_simulation.py --duracion 20      # 20 segundos
    python3 run_simulation.py --semilla 42       # reproducible
    python3 run_simulation.py --no-docker        # broker manual
"""
import argparse
import subprocess
import sys
import time
import socket
from pathlib import Path


def log(level, msg):
    """Log con nivel."""
    symbols = {"INFO": "ℹ️ ", "OK": "✓ ", "WARN": "⚠️ ", "ERROR": "❌", "DEBUG": "🔍", "STEP": "📍"}
    print(f"{symbols.get(level, '•')} {msg}")


def log_section(title):
    """Log de sección."""
    print(f"\n{'=' * 60}")
    print(f"🔬 {title}")
    print(f"{'=' * 60}\n")


class DependencyManager:
    """Maneja instalación de dependencias."""

    @staticmethod
    def check_python_version():
        """Verifica Python >= 3.8."""
        version = sys.version_info
        log("DEBUG", f"Python version: {version.major}.{version.minor}.{version.micro}")
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            log("ERROR", f"Python 3.8+ requerido (tienes {version.major}.{version.minor})")
            return False
        log("OK", f"Python {version.major}.{version.minor} ✓")
        return True

    @staticmethod
    def check_paho_mqtt():
        """Verifica si paho-mqtt está instalado."""
        log("DEBUG", "Verificando paho-mqtt...")
        try:
            import paho.mqtt.client
            log("OK", "paho-mqtt está instalado")
            return True
        except ImportError as e:
            log("WARN", f"paho-mqtt NO está instalado: {e}")
            return False

    @staticmethod
    def detect_package_manager():
        """Detecta gestor de paquetes disponible."""
        log("DEBUG", "Detectando gestor de paquetes...")
        managers = [
            ("pip3", ["pip3", "--version"]),
            ("pip", ["pip", "--version"]),
            ("pacman", ["pacman", "--version"]),
            ("apt", ["apt", "--version"]),
            ("dnf", ["dnf", "--version"]),
        ]

        available = []
        for name, cmd in managers:
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=2)
                if result.returncode == 0:
                    available.append(name)
                    log("DEBUG", f"  {name}: disponible")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass

        return available

    @staticmethod
    def try_install_paho_mqtt():
        """Intenta instalar paho-mqtt."""
        log("STEP", "Intentando instalar paho-mqtt...")

        managers = DependencyManager.detect_package_manager()

        if not managers:
            log("ERROR", "No se encontró ningún gestor de paquetes")
            return False

        strategies = []
        if "pip3" in managers:
            strategies.append(("pip3 install --user paho-mqtt", ["pip3", "install", "--user", "paho-mqtt"]))
        if "pip" in managers:
            strategies.append(("pip install --user paho-mqtt", ["pip", "install", "--user", "paho-mqtt"]))
        if "pacman" in managers:
            # Primero intenta sin sudo
            strategies.append(("pacman -S python-paho-mqtt (sin sudo)", ["pacman", "-S", "python-paho-mqtt", "--noconfirm"]))
            strategies.append(("pacman -S python-paho-mqtt (con sudo)", ["sudo", "pacman", "-S", "python-paho-mqtt", "--noconfirm"]))
        if "apt" in managers:
            strategies.append(("apt install python3-paho-mqtt (con sudo)", ["sudo", "apt", "install", "-y", "python3-paho-mqtt"]))

        log("DEBUG", f"Estrategias disponibles: {len(strategies)}")
        for i, (desc, cmd) in enumerate(strategies, 1):
            log("DEBUG", f"  {i}. {desc}")

        for desc, cmd in strategies:
            log("DEBUG", f"Intentando: {desc}")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    log("OK", f"✓ Instalado: {desc}")
                    time.sleep(1)
                    return DependencyManager.check_paho_mqtt()
                else:
                    err_msg = result.stderr[:150] if result.stderr else result.stdout[:150]
                    log("DEBUG", f"  Salida: {err_msg}")
            except subprocess.TimeoutExpired:
                log("WARN", f"  Timeout: {desc}")
            except PermissionError:
                log("WARN", f"  Permiso denegado: {desc}")
            except Exception as e:
                log("DEBUG", f"  Error: {e}")

        return False


class BrokerManager:
    """Maneja broker MQTT."""

    def __init__(self, broker="localhost", port=1883, use_docker=True):
        self.broker = broker
        self.port = port
        self.use_docker = use_docker
        self.docker_container = None
        self.broker_ready = False

    def is_docker_available(self):
        """Verifica si Docker está disponible."""
        log("DEBUG", "Verificando Docker...")
        try:
            result = subprocess.run(["docker", "--version"],
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                log("OK", f"Docker disponible: {result.stdout.strip()}")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        log("WARN", "Docker NO disponible")
        return False

    def is_port_open(self, timeout=1):
        """Verifica si el puerto MQTT está abierto."""
        log("DEBUG", f"Verificando conexión a {self.broker}:{self.port}...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((self.broker, self.port))
                is_open = result == 0
                log("DEBUG", f"  Resultado: {'ABIERTO' if is_open else 'CERRADO'}")
                return is_open
        except Exception as e:
            log("DEBUG", f"  Error de socket: {e}")
            return False

    def start_broker_docker(self):
        """Inicia broker con Docker."""
        log("STEP", f"Iniciando broker MQTT en Docker ({self.broker}:{self.port})...")

        # Limpia contenedor anterior
        log("DEBUG", "Limpiando contenedor anterior (si existe)...")
        try:
            result = subprocess.run(["docker", "stop", "svif-mosquitto-sim"],
                                  capture_output=True, timeout=3)
            if result.returncode == 0:
                log("DEBUG", "  Contenedor anterior detenido")
        except Exception as e:
            log("DEBUG", f"  No había contenedor anterior: {e}")

        # Inicia nuevo contenedor
        log("DEBUG", "Iniciando nuevo contenedor...")
        cmd = [
            "docker", "run", "--rm",
            "--name", "svif-mosquitto-sim",
            "-p", f"{self.port}:1883",
            "eclipse-mosquitto:2",
            "mosquitto", "-c", "/mosquitto-no-auth.conf"
        ]

        log("DEBUG", f"Comando: {' '.join(cmd)}")

        try:
            self.docker_container = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            log("DEBUG", f"  Proceso iniciado (PID={self.docker_container.pid})")
            time.sleep(1.5)

            if self.docker_container.poll() is not None:
                stdout, stderr = self.docker_container.communicate(timeout=1)
                log("ERROR", f"Contenedor falló al iniciar")
                log("DEBUG", f"  stdout: {stdout[:200]}")
                log("DEBUG", f"  stderr: {stderr[:200]}")
                return False

            log("OK", "Contenedor iniciado")
            return True
        except Exception as e:
            log("ERROR", f"Excepción al iniciar Docker: {e}")
            return False

    def wait_for_broker(self, timeout=15):
        """Espera a que el broker esté disponible."""
        log("STEP", f"Esperando broker (max {timeout}s)...")
        start = time.time()
        attempt = 0

        while time.time() - start < timeout:
            attempt += 1
            if self.is_port_open(timeout=1):
                elapsed = time.time() - start
                log("OK", f"Broker disponible (intento {attempt}, {elapsed:.1f}s)")
                self.broker_ready = True
                return True

            time.sleep(0.5)
            if attempt % 4 == 0:  # Log cada 2 segundos
                log("DEBUG", f"  Intento {attempt}... (elapsed: {time.time()-start:.1f}s)")

        log("ERROR", f"Broker NO respondió después de {timeout}s")
        return False

    def start(self):
        """Inicia el broker (Docker o manual)."""
        log_section("FASE 1: Iniciar Broker MQTT")

        if not self.use_docker:
            log("INFO", "Modo manual: asumiendo broker en localhost:1883")
            return self.wait_for_broker()

        if not self.is_docker_available():
            log("WARN", "Docker no disponible, asumiendo broker manual...")
            self.use_docker = False
            return self.wait_for_broker()

        if not self.start_broker_docker():
            log("WARN", "Docker falló, intentando broker manual...")
            self.use_docker = False
            return self.wait_for_broker()

        return self.wait_for_broker()

    def stop(self):
        """Detiene el broker."""
        if self.docker_container and self.use_docker:
            log("DEBUG", "Deteniendo contenedor Docker...")
            try:
                self.docker_container.terminate()
                self.docker_container.wait(timeout=2)
                log("OK", "Contenedor detenido")
            except Exception as e:
                log("WARN", f"Error deteniendo contenedor: {e}")
                try:
                    subprocess.run(["docker", "stop", "svif-mosquitto-sim"],
                                 timeout=2, capture_output=True)
                except Exception:
                    pass


class SimulationExecutor:
    """Ejecuta la simulación."""

    def __init__(self, broker, port, duracion, semilla):
        self.broker = broker
        self.port = port
        self.duracion = duracion
        self.semilla = semilla
        self.process = None

    def find_simulator(self):
        """Encuentra simular_sistema.py."""
        log("DEBUG", "Buscando simular_sistema.py...")

        paths = [
            Path(__file__).parent.parent / "recursos-comunes" / "herramientas" / "simular_sistema.py",
            Path.home() / "mddCPStrabajo" / "recursos-comunes" / "herramientas" / "simular_sistema.py",
        ]

        for p in paths:
            log("DEBUG", f"  Verificando: {p}")
            if p.exists():
                log("OK", f"Encontrado: {p}")
                return p

        # Busca en árbol
        log("DEBUG", "Buscando en árbol de directorios...")
        try:
            result = subprocess.run(
                ["find", str(Path(__file__).parent), "-name", "simular_sistema.py", "-type", "f"],
                capture_output=True, text=True, timeout=5
            )
            if result.stdout.strip():
                p = Path(result.stdout.strip().split("\n")[0])
                log("OK", f"Encontrado (búsqueda): {p}")
                return p
        except Exception as e:
            log("DEBUG", f"  Error en búsqueda: {e}")

        log("ERROR", "simular_sistema.py NO encontrado")
        return None

    def run(self):
        """Ejecuta la simulación."""
        log_section("FASE 2: Ejecutar Simulación")

        sim_path = self.find_simulator()
        if not sim_path:
            return False

        log("INFO", f"Duración: {self.duracion}s")
        log("INFO", f"Semilla: {self.semilla}")
        log("INFO", f"Broker: {self.broker}:{self.port}")

        cmd = [
            "python3", str(sim_path),
            "--broker", self.broker,
            "--port", str(self.port),
            "--duracion", str(self.duracion),
            "--semilla", str(self.semilla)
        ]

        log("DEBUG", f"Comando: {' '.join(cmd)}")
        print()  # Línea en blanco

        try:
            self.process = subprocess.run(
                cmd,
                timeout=self.duracion + 15
            )

            if self.process.returncode == 0:
                log("OK", "Simulación completada sin errores")
                return True
            else:
                log("ERROR", f"Simulación finalizó con código {self.process.returncode}")
                return False

        except subprocess.TimeoutExpired:
            log("ERROR", f"Simulación excedió timeout ({self.duracion + 15}s)")
            return False
        except KeyboardInterrupt:
            log("WARN", "Simulación cancelada por usuario")
            return False
        except Exception as e:
            log("ERROR", f"Excepción: {e}")
            return False


class SimulationRunner:
    """Orquesta todo el flujo."""

    def __init__(self, broker="localhost", port=1883, use_docker=True,
                 duracion=12, semilla=7):
        self.broker = broker
        self.port = port
        self.use_docker = use_docker
        self.duracion = duracion
        self.semilla = semilla
        self.broker_mgr = BrokerManager(broker, port, use_docker)
        self.exec_mgr = SimulationExecutor(broker, port, duracion, semilla)

    def run(self):
        """Ejecuta flujo completo."""
        print(f"\n{'=' * 60}")
        print("🔬 SVIF Simulation Runner — MDD4CPS Semana 4")
        print(f"{'=' * 60}\n")

        # Fase 0: Verificar dependencias
        log_section("FASE 0: Verificar Dependencias")

        if not DependencyManager.check_python_version():
            return False

        if not DependencyManager.check_paho_mqtt():
            log("WARN", "Intentando instalar paho-mqtt...")
            if not DependencyManager.try_install_paho_mqtt():
                log("ERROR", "No se pudo instalar paho-mqtt")
                log("INFO", "Opciones manuales:")
                print("  1. pip install --user paho-mqtt")
                print("  2. pip3 install --user paho-mqtt")
                print("  3. sudo pacman -S python-paho-mqtt")
                print("  4. sudo apt install python3-paho-mqtt")
                return False
            log("OK", "paho-mqtt instalado exitosamente")

        # Fase 1: Broker
        try:
            if not self.broker_mgr.start():
                return False

            # Fase 2: Simulación
            if not self.exec_mgr.run():
                return False

            log_section("RESULTADO FINAL")
            log("OK", "✅ Simulación completada EXITOSAMENTE")
            return True

        except KeyboardInterrupt:
            log("WARN", "Cancelado por usuario (Ctrl+C)")
            return False
        finally:
            log_section("LIMPIEZA")
            self.broker_mgr.stop()
            log("OK", "Recursos limpios")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--broker", default="localhost",
                       help="Host MQTT (default: localhost)")
    parser.add_argument("--port", type=int, default=1883,
                       help="Puerto MQTT (default: 1883)")
    parser.add_argument("--no-docker", action="store_false", dest="use_docker",
                       help="No usar Docker (broker debe estar corriendo)")
    parser.add_argument("--duracion", type=int, default=12,
                       help="Duración en segundos (default: 12)")
    parser.add_argument("--semilla", type=int, default=7,
                       help="Semilla para reproducibilidad (default: 7)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbosidad extra (ya está por defecto)")

    args = parser.parse_args()

    runner = SimulationRunner(
        broker=args.broker,
        port=args.port,
        use_docker=args.use_docker,
        duracion=args.duracion,
        semilla=args.semilla
    )

    success = runner.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
