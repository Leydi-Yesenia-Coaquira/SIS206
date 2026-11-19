# servicios.py
from typing import Optional
from estudiante import Estudiante


class ServicioEstudiante:
    def __init__(self, repo, estrategia) -> None:
        self._repo = repo              # cualquier repositorio
        self._estrategia = estrategia  # cualquier estrategia de promedio

    def registrar(self, e: Estudiante) -> None:
        e.ppa = self._estrategia.calcular(e.notas)
        self._repo.guardar(e)

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._repo.buscar(cod)

    def listar(self) -> list[Estudiante]:
        return self._repo.listar()