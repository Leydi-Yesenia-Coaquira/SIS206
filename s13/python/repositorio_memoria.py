# repositorio_memoria.py — guarda todo en un diccionario (no usa archivos)
from typing import Optional
from estudiante import Estudiante


class RepositorioMemoria:
    def __init__(self) -> None:
        self._datos: dict[int, Estudiante] = {}

    def guardar(self, e: Estudiante) -> None:
        self._datos[e.codigo] = e

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._datos.get(cod)

    def listar(self) -> list[Estudiante]:
        return list(self._datos.values())

    def eliminar(self, cod: int) -> None:
        self._datos.pop(cod, None)