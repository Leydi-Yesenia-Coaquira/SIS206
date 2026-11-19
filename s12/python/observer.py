# observer.py
from typing import Protocol
from estudiante import Estudiante
import logger as Logger

class IObservador(Protocol):
    def on_guardado(self, e: Estudiante) -> None: ...

class LoggerObservador:
    def on_guardado(self, e: Estudiante) -> None:
        Logger.log(f"Guardado: [{e.codigo}] {e.nombre}")

class ConsolaObservador:
    def on_guardado(self, e: Estudiante) -> None:
        print(f">> Vista: {e}")

# ADICIONAL
class EmailObservador:
    def on_guardado(self, e: Estudiante) -> None:
        print(f"Enviando correo a {e.nombre}")

class RepositorioObservable:
    def __init__(self, repo) -> None:
        self._repo = repo
        self._obs: list[IObservador] = []
    def suscribir(self, o: IObservador) -> None:
        self._obs.append(o)
    def guardar(self, e: Estudiante) -> None:
        self._repo.guardar(e)
        for o in self._obs:
            o.on_guardado(e)
    def buscar(self, cod: int):
        return self._repo.buscar(cod)
    def listar(self):
        return self._repo.listar()
