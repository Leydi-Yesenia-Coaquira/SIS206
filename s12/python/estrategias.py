# estrategias.py — Strategy para el cálculo del PPA
from typing import Protocol


class IEstrategiaCalculo(Protocol):
    def calcular(self, notas: list[float]) -> float: ...


class PromedioSimple:
    def calcular(self, notas: list[float]) -> float:
        return sum(notas) / len(notas) if notas else 0.0


class PromedioModerado:
    """Descarta la nota más baja y la más alta (si hay al menos 3 notas)."""
    def calcular(self, notas: list[float]) -> float:
        if len(notas) < 3:
            return PromedioSimple().calcular(notas)
        n = sorted(notas)[1:-1]
        return sum(n) / len(n)


# ADICIONAL
class PromedioGeometrico:
    """Raíz n-ésima del producto de las notas."""
    def calcular(self, notas: list[float]) -> float:
        if not notas:
            return 0.0
        producto = 1.0
        for n in notas:
            producto *= n
        return producto ** (1 / len(notas))