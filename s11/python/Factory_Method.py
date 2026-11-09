# Factory Method en Python — Protocol + registro dinámico
from __future__ import annotations
from typing import Protocol
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

# ── Producto abstracto ──────────────────────────────────
class ReporteAcademico(Protocol):
    def agregar_dato(self, clave: str, valor: str) -> None: ...
    def generar(self) -> str: ...
    @property
    def formato(self) -> str: ...
    @property
    def extension(self) -> str: ...

# ── Productos concretos ─────────────────────────────────
@dataclass
class ReporteTXT:
    _datos: list[tuple[str, str]] = field(default_factory=list)

    def agregar_dato(self, clave: str, valor: str) -> None:
        self._datos.append((clave, valor))

    def generar(self) -> str:
        lineas = ["=== REPORTE ACADÉMICO ==="]
        lineas += [f"{k}: {v}" for k, v in self._datos]
        return "\n".join(lineas)

    @property
    def formato(self) -> str: return "Texto plano"
    @property
    def extension(self) -> str: return ".txt"

@dataclass
class ReporteCSV:
    _datos: list[tuple[str, str]] = field(default_factory=list)

    def agregar_dato(self, clave: str, valor: str) -> None:
        self._datos.append((clave, valor))

    def generar(self) -> str:
        lineas = ["campo,valor"]
        lineas += [f"{k},{v}" for k, v in self._datos]
        return "\n".join(lineas)

    @property
    def formato(self) -> str: return "CSV"
    @property
    def extension(self) -> str: return ".csv"

# ── Creador base abstracto ──────────────────────────────
class GeneradorReporte(ABC):
    @abstractmethod
    def crear_reporte(self) -> ReporteAcademico:
        """Factory Method — subclases deciden el producto."""
        ...

    def procesar_y_guardar(self, estudiante: str, promedio: float) -> None:
        """Template Method — usa Factory Method internamente."""
        reporte = self.crear_reporte()   # ← factory method
        reporte.agregar_dato("Estudiante", estudiante)
        reporte.agregar_dato("Promedio", f"{promedio:.2f}")
        reporte.agregar_dato("Estado", "Aprobado" if promedio >= 11 else "Desaprobado")
        contenido = reporte.generar()
        archivo = f"reporte_{estudiante}{reporte.extension}"
        print(f"[{reporte.formato}] Guardando en: {archivo}")
        print(contenido)

# ── Creadores concretos ─────────────────────────────────
class GeneradorTXT(GeneradorReporte):
    def crear_reporte(self) -> ReporteTXT:
        return ReporteTXT()

class GeneradorCSV(GeneradorReporte):
    def crear_reporte(self) -> ReporteCSV:
        return ReporteCSV()

# ── Registro dinámico de fábricas ───────────────────────
class RegistroGeneradores:
    def __init__(self) -> None:
        self._registro: dict[str, type[GeneradorReporte]] = {}

    def registrar(self, fmt: str, cls: type[GeneradorReporte]) -> None:
        self._registro[fmt] = cls

    def crear(self, fmt: str) -> GeneradorReporte:
        if fmt not in self._registro:
            raise ValueError(f"Formato no registrado: {fmt}")
        return self._registro[fmt]()


if __name__ == "__main__":
    reg = RegistroGeneradores()
    reg.registrar("txt", GeneradorTXT)
    reg.registrar("csv", GeneradorCSV)

    for fmt in ["txt", "csv"]:
        gen = reg.crear(fmt)
        gen.procesar_y_guardar("Maria Quispe", 15.75)
