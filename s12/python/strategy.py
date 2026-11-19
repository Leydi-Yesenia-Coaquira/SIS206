# strategy.py — Actividad 2A
from estrategias import (IEstrategiaCalculo, PromedioSimple,
                         PromedioModerado, PromedioGeometrico)
import logger as Logger   # AGREGADO: faltaba en la guía


class ContextoCalculo:
    def __init__(self, est: IEstrategiaCalculo) -> None:
        self._est = est

    def set_estrategia(self, est: IEstrategiaCalculo) -> None:
        Logger.log(f"Estrategia cambiada a {type(est).__name__}")
        self._est = est

    def calcular(self, notas: list[float]) -> float:
        return self._est.calcular(notas)


# Test de intercambiabilidad (ejemplo de la guía):
notas = [10.0, 15.0, 18.0, 20.0, 12.0]
ctx = ContextoCalculo(PromedioSimple())
ppa_simple = ctx.calcular(notas)          # = 15.0
ctx.set_estrategia(PromedioModerado())
ppa_mod = ctx.calcular(notas)             # descarta 10 y 20 -> 15.0
print(f"Simple={ppa_simple:.1f}  Moderado={ppa_mod:.1f}")

# Notas con un extremo muy bajo: aquí SÍ hay diferencia
notas2 = [5.0, 15.0, 16.0, 17.0, 20.0]
ctx.set_estrategia(PromedioSimple())
s2 = ctx.calcular(notas2)
ctx.set_estrategia(PromedioModerado())
m2 = ctx.calcular(notas2)
print(f"Simple={s2:.1f}  Moderado={m2:.1f}  Diferencia={m2 - s2:.1f}")

# ADICIONAL: PromedioGeometrico
ctx.set_estrategia(PromedioGeometrico())
print(f"Geometrico={ctx.calcular(notas):.2f}")