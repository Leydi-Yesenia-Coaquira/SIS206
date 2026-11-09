# Actividad 1.2 - ConfiguracionApp Singleton en Python (metaclase)
# que carga parametros desde un archivo .env simulado
from __future__ import annotations
from threading import Lock
from typing import Any
from pathlib import Path


# Metaclase Singleton (de la guia, seccion 2.2 - Enfoque 1)
class SingletonMeta(type):
    _instancias: dict[type, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instancias:
                cls._instancias[cls] = super().__call__(*args, **kwargs)
        return cls._instancias[cls]


# Contenido del archivo .env simulado
ENV_SIMULADO = """# Archivo .env simulado
DB_URL=postgresql://localhost:5432/unap
MAX_CONEXIONES=20
DEBUG=true
"""


class ConfiguracionApp(metaclass=SingletonMeta):
    def __init__(self, ruta_env: str = ".env") -> None:
        self.parametros: dict[str, str] = {}
        self._cargar_env(ruta_env)

    def _cargar_env(self, ruta_env: str) -> None:
        archivo = Path(ruta_env)
        if not archivo.exists():                  # si no existe, se crea el .env simulado
            archivo.write_text(ENV_SIMULADO, encoding="utf-8")

        for linea in archivo.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if not linea or linea.startswith("#"):  # ignora lineas vacias y comentarios
                continue
            clave, valor = linea.split("=", 1)      # separa CLAVE=VALOR
            self.parametros[clave.strip()] = valor.strip()

        self.db_url = self.parametros.get("DB_URL", "sqlite:///app.db")
        self.max_conexiones = int(self.parametros.get("MAX_CONEXIONES", "10"))
        self.debug = self.parametros.get("DEBUG", "false").lower() == "true"


if __name__ == "__main__":
    cfg1 = ConfiguracionApp()
    cfg2 = ConfiguracionApp()

    print(f"DB_URL:         {cfg1.db_url}")
    print(f"MAX_CONEXIONES: {cfg1.max_conexiones}")
    print(f"DEBUG:          {cfg1.debug}")
    print(f"Config unica:   {cfg1 is cfg2}")   # True