# estrategias.py
class PromedioSimple:
    def calcular(self, notas: list[float]) -> float:
        if not notas:
            return 0.0
        return round(sum(notas) / len(notas), 2)