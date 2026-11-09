# Actividad 2 - Factory Method: generador de boletas de notas
# (basado en el codigo de la guia, seccion 3.2)
from __future__ import annotations
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


# ── Producto abstracto ──────────────────────────────────
class BoletaNotas(Protocol):
    def agregar_nota(self, curso: str, nota: float) -> None: ...
    def generar(self) -> str: ...
    @property
    def extension(self) -> str: ...


# ── Productos concretos ─────────────────────────────────
@dataclass
class BoletaTXT:
    _notas: list[tuple[str, float]] = field(default_factory=list)

    def agregar_nota(self, curso: str, nota: float) -> None:
        self._notas.append((curso, nota))

    def generar(self) -> str:
        lineas = ["=== BOLETA DE NOTAS ==="]
        lineas += [f"{c}: {n:.2f}" for c, n in self._notas]
        return "\n".join(lineas)

    @property
    def extension(self) -> str: return ".txt"


@dataclass
class BoletaCSV:
    _notas: list[tuple[str, float]] = field(default_factory=list)

    def agregar_nota(self, curso: str, nota: float) -> None:
        self._notas.append((curso, nota))

    def generar(self) -> str:
        lineas = ["curso,nota"]
        lineas += [f"{c},{n:.2f}" for c, n in self._notas]
        return "\n".join(lineas)

    @property
    def extension(self) -> str: return ".csv"


@dataclass
class BoletaHTML:
    _notas: list[tuple[str, float]] = field(default_factory=list)

    def agregar_nota(self, curso: str, nota: float) -> None:
        self._notas.append((curso, nota))

    def generar(self) -> str:
        filas = "".join(f"<tr><td>{c}</td><td>{n:.2f}</td></tr>\n" for c, n in self._notas)
        return ("<table border='1'>\n<tr><th>Curso</th><th>Nota</th></tr>\n"
                + filas + "</table>")

    @property
    def extension(self) -> str: return ".html"


# ── Creador base ────────────────────────────────────────
class GeneradorBoleta(ABC):
    @abstractmethod
    def crear_boleta(self) -> BoletaNotas:
        """Factory Method — cada subclase decide que boleta crear."""
        ...

    def generar_y_enviar(self, estudiante: str, notas: dict[str, float]) -> None:
        """Template Method — mismos pasos para cualquier formato."""
        boleta = self.crear_boleta()                 # 1. crear (factory method)
        for curso, nota in notas.items():            # 2. agregar notas
            boleta.agregar_nota(curso, nota)
        contenido = boleta.generar()                 # 3. generar
        archivo = f"boleta_{estudiante}{boleta.extension}"
        Path(archivo).write_text(contenido, encoding="utf-8")   # 4. guardar
        print(f"Enviando {archivo}:")                # 5. enviar (simulado)
        print(contenido + "\n")


# ── Creadores concretos ─────────────────────────────────
class GeneradorTXT(GeneradorBoleta):
    def crear_boleta(self) -> BoletaTXT:
        return BoletaTXT()


class GeneradorCSV(GeneradorBoleta):
    def crear_boleta(self) -> BoletaCSV:
        return BoletaCSV()


class GeneradorHTML(GeneradorBoleta):
    def crear_boleta(self) -> BoletaHTML:
        return BoletaHTML()


# ── Registro: nombre -> clase ───────────────────────────
class RegistroGeneradores:
    def __init__(self) -> None:
        self._registro: dict[str, type[GeneradorBoleta]] = {}

    def registrar(self, nombre: str, clase: type[GeneradorBoleta]) -> None:
        self._registro[nombre] = clase

    def crear(self, nombre: str) -> GeneradorBoleta:
        if nombre not in self._registro:
            raise ValueError(f"Formato no registrado: {nombre}")
        return self._registro[nombre]()


# ── Archivo de configuracion JSON ───────────────────────
CONFIG_JSON = {
    "formatos": ["txt", "csv", "html"],
    "estudiante": "2023001",
    "notas": {"POO II": 16.5, "Estructuras Discretas": 14.0, "Calculo": 12.75}
}


if __name__ == "__main__":
    ruta = Path("config.json")
    if not ruta.exists():                       # si no existe, se crea el JSON
        ruta.write_text(json.dumps(CONFIG_JSON, indent=2), encoding="utf-8")
    config = json.loads(ruta.read_text(encoding="utf-8"))

    reg = RegistroGeneradores()
    reg.registrar("txt", GeneradorTXT)
    reg.registrar("csv", GeneradorCSV)
    reg.registrar("html", GeneradorHTML)

    # Prueba: itera los 3 formatos leidos del JSON
    for fmt in config["formatos"]:
        gen = reg.crear(fmt)
        gen.generar_y_enviar(config["estudiante"], config["notas"])