# solid_s10.py — Refactorización SRP + DIP (Semana 10)
# Ejecutar: python solid_s10.py
from dataclasses import dataclass, field
from typing import Optional, Protocol, Sequence


# ─── 1. Solo datos ───────────────────────────────────────────
@dataclass
class Estudiante:
    codigo: int
    nombre: str
    ppa: float = 0.0
    notas: list[float] = field(default_factory=list)


# ─── 2. Solo cálculo ────────────────────────────────────────
class IEstrategiaCalculo(Protocol):
    def calcular(self, notas: Sequence[float]) -> float: ...


class PromedioSimple:
    def calcular(self, notas: Sequence[float]) -> float:
        return sum(notas) / len(notas) if notas else 0.0


# ADICIONAL: descarta la nota más alta y la más baja antes de promediar
class PromedioModerado:
    def calcular(self, notas: Sequence[float]) -> float:
        if len(notas) <= 2:
            return 0.0
        ordenadas = sorted(notas)
        centrales = ordenadas[1:-1]          # quita la primera (menor) y la última (mayor)
        return sum(centrales) / len(centrales)


# ─── 3. Solo persistencia (Protocol = interfaz DIP) ─────────
class IRepositorioEstudiante(Protocol):
    def guardar(self, e: Estudiante) -> None: ...
    def buscar(self, cod: int) -> Optional[Estudiante]: ...
    def listar(self) -> list[Estudiante]: ...


# Implementación en memoria (útil para tests)
class RepositorioMemoria:
    def __init__(self) -> None:
        self._datos: dict[int, Estudiante] = {}

    def guardar(self, e: Estudiante) -> None:
        self._datos[e.codigo] = e

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._datos.get(cod)

    def listar(self) -> list[Estudiante]:
        return list(self._datos.values())


# ─── 4. Orquestación ────────────────────────────────────────
class ServicioEstudiante:
    def __init__(self, repo: IRepositorioEstudiante,
                 calc: IEstrategiaCalculo) -> None:
        self._repo = repo
        self._calc = calc

    def registrar(self, e: Estudiante) -> None:
        e.ppa = self._calc.calcular(e.notas)
        self._repo.guardar(e)

    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._repo.buscar(cod)


# ─── Programa principal ─────────────────────────────────────
if __name__ == "__main__":
    # Crear el servicio con RepositorioMemoria + PromedioSimple
    repo = RepositorioMemoria()
    svc = ServicioEstudiante(repo, PromedioSimple())

    # Registrar 3 estudiantes con notas distintas
    svc.registrar(Estudiante(1001, "Ana Quispe",   notas=[14, 20, 16, 18, 12]))
    svc.registrar(Estudiante(1002, "Luis Mamani",  notas=[11, 13, 15]))
    svc.registrar(Estudiante(1003, "Rosa Condori", notas=[17, 18, 19, 14]))

    # Verificar con buscar() que el PPA se calculó correctamente
    print("=== PromedioSimple ===")
    for cod in (1001, 1002, 1003):
        e = svc.buscar(cod)
        print(f"[{e.codigo}] {e.nombre:<13} notas={e.notas}  PPA={e.ppa:.2f}")

    assert svc.buscar(1001).ppa == 16.0   # (14+20+16+18+12)/5
    assert svc.buscar(1002).ppa == 13.0   # (11+13+15)/3
    assert svc.buscar(1003).ppa == 17.0   # (17+18+19+14)/4
    assert svc.buscar(9999) is None       # código que no existe
    print("✔ Los 3 PPA son correctos\n")

    # ─── ACTIVIDAD 2B — OCP ─────────────────────────────────
    # Se crea svc2 con la nueva estrategia. ServicioEstudiante NO se toca.
    print("=== Actividad 2B: PromedioModerado vs PromedioSimple ===")
    repo2 = RepositorioMemoria()
    svc2 = ServicioEstudiante(repo2, PromedioModerado())

    # Registrar los mismos estudiantes con las mismas notas
    for e_orig in repo.listar():
        copia = Estudiante(e_orig.codigo, e_orig.nombre, notas=list(e_orig.notas))
        svc2.registrar(copia)

    # Comparar el PPA de ambas estrategias
    print(f"{'Estudiante':<14} {'Notas':<22} {'Simple':>7} {'Moderado':>9}")
    for cod in (1001, 1002, 1003):
        s = svc.buscar(cod)
        m = svc2.buscar(cod)
        print(f"{s.nombre:<14} {str(s.notas):<22} {s.ppa:>7.2f} {m.ppa:>9.2f}")

    assert svc2.buscar(1001).ppa == 16.0  # descarta 12 y 20 → (14+16+18)/3
    assert svc2.buscar(1002).ppa == 13.0  # descarta 11 y 15 → 13/1
    assert svc2.buscar(1003).ppa == 17.5  # descarta 14 y 19 → (17+18)/2
    print("✔ PromedioModerado correcto")

    # ¿ServicioEstudiante cambió?
    # NO. La clase ServicioEstudiante no se modificó en ninguna línea.
    # Solo se creó una nueva clase (PromedioModerado) y se pasó al
    # constructor ServicioEstudiante(repo2, PromedioModerado()).
    # Esto cumple el Principio Abierto/Cerrado (OCP) la clase está
    # ABIERTA a extensión (acepta nuevas estrategias de cálculo) pero
    # CERRADA a modificación (su código fuente no cambia).
    # Funciona porque ServicioEstudiante depende de la interfaz
    # IEstrategiaCalculo (Protocol) y no de una clase concreta (DIP).