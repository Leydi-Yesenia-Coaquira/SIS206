# estudiante.py — Clase Estudiante con Python 3.12 + dataclass
import json
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Estudiante:
    codigo: int
    nombre: str
    ppa: float
    ciclo: int
    notas: list[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.codigo <= 0:
            raise ValueError("Codigo debe ser positivo")
        if not self.nombre.strip():
            raise ValueError("Nombre no puede estar vacio")
        if not (0.0 <= self.ppa <= 20.0):
            raise ValueError("PPA debe estar entre 0 y 20")

    def agregar_nota(self, nota: float) -> None:
        if not (0.0 <= nota <= 20.0):
            raise ValueError(f"Nota {nota} fuera de rango")
        self.notas.append(nota)

    def calcular_promedio(self) -> Optional[float]:
        if not self.notas:
            return None
        return sum(self.notas) / len(self.notas)

    def __str__(self) -> str:
        return f"[{self.codigo}] {self.nombre} — PPA: {self.ppa} — Ciclo: {self.ciclo}"


if __name__ == "__main__":
    e = Estudiante(1001, "Ana Quispe", 15.5, 3)

    # 5 notas distintas, promedio con 2 decimales
    for nota in [14.0, 16.5, 12.0, 18.0, 15.25]:
        e.agregar_nota(nota)
    print(e)
    print(f"Promedio semestral: {e.calcular_promedio():.2f}")

    # 3 casos de prueba con assert (codigo, nombre y ppa invalidos)
    def lanza_error(**datos) -> bool:
        try:
            Estudiante(**datos)
        except ValueError:
            return True
        return False

    assert lanza_error(codigo=-1, nombre="Luis", ppa=12.0, ciclo=1), "codigo invalido no detectado"
    assert lanza_error(codigo=1002, nombre="   ", ppa=12.0, ciclo=1), "nombre vacio no detectado"
    assert lanza_error(codigo=1003, nombre="Rosa", ppa=25.0, ciclo=1), "ppa fuera de rango no detectado"
    print("Los 3 asserts pasaron correctamente")

    # ADICIONAL: serializacion a JSON
    print(json.dumps(asdict(e), ensure_ascii=False))