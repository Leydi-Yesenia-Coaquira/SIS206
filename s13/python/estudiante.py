# estudiante.py
from dataclasses import dataclass, field


@dataclass
class Estudiante:
    codigo: int
    nombre: str
    ppa: float = 0.0
    notas: list[float] = field(default_factory=list)