# main_observer.py — prueba de la Actividad 1A
# Ejecutar: python main_observer.py
from repositorios import RepositorioMemoria
from observer import (RepositorioObservable, LoggerObservador,
                      ConsolaObservador, EmailObservador)
from servicios import ServicioEstudiante
from estrategias import PromedioSimple
from estudiante import Estudiante
import logger

# 1. Repositorio observable
repo_obs = RepositorioObservable(RepositorioMemoria())

# 2. Suscribir observadores
repo_obs.suscribir(ConsolaObservador())
repo_obs.suscribir(LoggerObservador())
repo_obs.suscribir(EmailObservador())   # ADICIONAL

# 3. Crear svc
calc = PromedioSimple()
svc = ServicioEstudiante(repo_obs, calc)

# 4. Registrar 2 estudiantes
svc.registrar(Estudiante(1001, "Ana Quispe", 0.0, [14.0, 18.0, 16.0]))
svc.registrar(Estudiante(1002, "Juan Mamani", 0.0, [12.0, 15.0, 10.0]))

print("\nEstudiantes en repositorio:", len(svc.listar()))
print("Entradas de log:", len(logger.get_entradas()))