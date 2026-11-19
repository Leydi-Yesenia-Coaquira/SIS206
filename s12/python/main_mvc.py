# main_mvc.py — wiring MVC completo (Actividad 3A)
# Ejecutar: python main_mvc.py
from repositorios import RepositorioMemoria
from observer import RepositorioObservable, ConsolaObservador, LoggerObservador
from servicios import ServicioEstudiante
from estrategias import PromedioSimple, PromedioModerado
from estudiante import Estudiante
import logger

# 1. Modelo
repo_base = RepositorioMemoria()
repo_obs = RepositorioObservable(repo_base)

# 2. Vista (observadora)
vista = ConsolaObservador()
log_obs = LoggerObservador()
repo_obs.suscribir(vista)
repo_obs.suscribir(log_obs)

# 3. Controlador
svc = ServicioEstudiante(repo_obs, PromedioSimple())

# 4. Usar el sistema
estudiantes = [
    Estudiante(1001, "Ana Quispe", 0.0, [14.0, 18.0, 16.0]),
    Estudiante(1002, "Juan Mamani", 0.0, [12.0, 15.0, 10.0]),
    Estudiante(1003, "Rosa Quispe", 0.0, [18.0, 20.0, 19.0]),
    Estudiante(1004, "Luis Condori", 0.0, [5.0, 5.0, 5.0]),   # AGREGADO: 4° estudiante
]

print("=== Con PromedioSimple ===")
for e in estudiantes:
    svc.registrar(e)

# AGREGADO: cambiar la estrategia a PromedioModerado y registrar de nuevo
print("\n=== Con PromedioModerado ===")
svc.set_estrategia(PromedioModerado())
for e in estudiantes:
    svc.registrar(e)

print("\nEntradas de log:", len(logger.get_entradas()))