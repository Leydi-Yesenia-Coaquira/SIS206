# logger.py — Singleton a nivel de módulo
from datetime import datetime

_entradas: list[str] = []


def log(msg: str) -> None:
    linea = f"[LOG] {datetime.now():%H:%M:%S} {msg}"
    _entradas.append(linea)
    print(linea)


def get_entradas() -> list[str]:
    return list(_entradas)