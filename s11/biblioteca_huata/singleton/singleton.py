# PATRON 1: SINGLETON  ->  Logger y Config
from __future__ import annotations
from pathlib import Path
from threading import Lock
from typing import Any


class SingletonMeta(type):
    _instancias: dict[type, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instancias:
                cls._instancias[cls] = super().__call__(*args, **kwargs)
        return cls._instancias[cls]


class Logger(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.entradas: list[str] = []

    def info(self, modulo: str, mensaje: str) -> None:
        entrada = f"[INFO][{modulo}] {mensaje}"
        self.entradas.append(entrada)
        print(entrada)


ENV_SIMULADO = """# Archivo .env simulado
ENTORNO=memoria
UI=tkinter
"""


class Config(metaclass=SingletonMeta):
    def __init__(self, ruta_env: str = ".env") -> None:
        archivo = Path(ruta_env)
        if not archivo.exists():
            archivo.write_text(ENV_SIMULADO, encoding="utf-8")
        self.parametros: dict[str, str] = {}
        for linea in archivo.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#"):
                clave, valor = linea.split("=", 1)
                self.parametros[clave.strip()] = valor.strip()
        self.entorno = self.parametros.get("ENTORNO", "memoria")   # memoria | archivo | bd
        self.ui = self.parametros.get("UI", "tkinter")             # tkinter | pyqt5