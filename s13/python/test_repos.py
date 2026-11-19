# test_repos.py — prueba de sustitucion LSP
import os
import tempfile
import pytest
from servicios import ServicioEstudiante
from estrategias import PromedioSimple
from estudiante import Estudiante
from repositorios import (RepositorioMemoria,
                          RepositorioJSON, RepositorioCSV, RepositorioSQLite)

# Carpeta temporal que funciona en Windows y Linux (en vez de "/tmp")
TMP = tempfile.gettempdir()
RUTA_JSON = os.path.join(TMP, "t.json")
RUTA_CSV = os.path.join(TMP, "t.csv")
RUTA_DB = os.path.join(TMP, "t.db")


# ADICIONAL: repositorio falso que cuenta cuantas veces se llamo guardar()
class MockRepositorio:
    def __init__(self) -> None:
        self._datos = {}
        self.llamadas_guardar = 0

    def guardar(self, e):
        self.llamadas_guardar += 1
        self._datos[e.codigo] = e

    def buscar(self, cod):
        return self._datos.get(cod)

    def listar(self):
        return list(self._datos.values())

    def eliminar(self, cod):
        self._datos.pop(cod, None)


@pytest.mark.parametrize("RepoClass,kwargs,cleanup", [
    (RepositorioMemoria, {}, None),
    (RepositorioJSON, {"ruta": RUTA_JSON}, RUTA_JSON),
    (RepositorioCSV, {"ruta": RUTA_CSV}, RUTA_CSV),
    (RepositorioSQLite, {"ruta": RUTA_DB}, RUTA_DB),
    (MockRepositorio, {}, None),
])
def test_servicio_con_cualquier_repo(RepoClass, kwargs, cleanup):
    # empezar limpio (por si quedo un archivo de una ejecucion anterior)
    if cleanup and os.path.exists(cleanup):
        os.remove(cleanup)

    repo = RepoClass(**kwargs)
    svc = ServicioEstudiante(repo, PromedioSimple())
    e1 = Estudiante(1001, "Ana", 0.0, [15.0, 18.0, 14.0])
    e2 = Estudiante(1002, "Juan", 0.0, [10.0, 12.0, 14.0])
    svc.registrar(e1)
    svc.registrar(e2)
    assert svc.buscar(1001).nombre == "Ana"
    assert svc.buscar(1002) is not None
    assert len(repo.listar()) == 2

    # Solo para el Mock: verificar que guardar() se llamo 2 veces
    if isinstance(repo, MockRepositorio):
        assert repo.llamadas_guardar == 2

    # SQLite: cerrar la conexion antes de borrar (necesario en Windows)
    if hasattr(repo, "cerrar"):
        repo.cerrar()
    if cleanup and os.path.exists(cleanup):
        os.remove(cleanup)

# Respuesta: ServicioEstudiante NO cambio ninguna linea.
# Funciona igual con Memoria, JSON, CSV, SQLite y el Mock porque solo
# depende de los metodos guardar/buscar/listar, no de como se guardan
# los datos. Eso es el Principio de Sustitucion de Liskov (LSP).