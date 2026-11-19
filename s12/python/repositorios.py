# repositorios.py — Repositorio en memoria
from estudiante import Estudiante


class RepositorioMemoria:
    def __init__(self) -> None:
        self._datos: dict[int, Estudiante] = {}

    def guardar(self, e: Estudiante) -> None:
        self._datos[e.codigo] = e

    def buscar(self, cod: int) -> Estudiante | None:
        return self._datos.get(cod)

    def listar(self) -> list[Estudiante]:
        return list(self._datos.values())