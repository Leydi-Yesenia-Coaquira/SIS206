# servicios.py — Controlador
from estudiante import Estudiante
from estrategias import IEstrategiaCalculo


class ServicioEstudiante:
    def __init__(self, repo, estrategia: IEstrategiaCalculo) -> None:
        self._repo = repo
        self._estrategia = estrategia

    def set_estrategia(self, estrategia: IEstrategiaCalculo) -> None:
        self._estrategia = estrategia

    def registrar(self, e: Estudiante) -> None:
        e.ppa = self._estrategia.calcular(e.notas)  # calcula el PPA
        self._repo.guardar(e)                        # guarda y notifica

    def buscar(self, cod: int):
        return self._repo.buscar(cod)

    def listar(self):
        return self._repo.listar()