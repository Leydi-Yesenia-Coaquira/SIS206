# PATRON 2: FACTORY METHOD  ->  repositorios (memoria / archivo / BD segun entorno)
from __future__ import annotations
import json
import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path

from singleton import Config, Logger


# ── Producto abstracto ──────────────────────────────────
class Repositorio(ABC):
    @abstractmethod
    def guardar(self, codigo: str, titulo: str) -> None: ...

    @abstractmethod
    def listar(self) -> list[tuple[str, str]]: ...


# ── Productos concretos ─────────────────────────────────
class RepositorioMemoria(Repositorio):
    def __init__(self) -> None:
        self._libros: dict[str, str] = {}

    def guardar(self, codigo: str, titulo: str) -> None:
        self._libros[codigo] = titulo

    def listar(self) -> list[tuple[str, str]]:
        return list(self._libros.items())


class RepositorioArchivo(Repositorio):
    def __init__(self, ruta: str = "libros.json") -> None:
        self.ruta = Path(ruta)

    def guardar(self, codigo: str, titulo: str) -> None:
        datos = json.loads(self.ruta.read_text(encoding="utf-8")) if self.ruta.exists() else {}
        datos[codigo] = titulo
        self.ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")

    def listar(self) -> list[tuple[str, str]]:
        if not self.ruta.exists():
            return []
        return list(json.loads(self.ruta.read_text(encoding="utf-8")).items())


class RepositorioBD(Repositorio):
    def __init__(self, ruta: str = "biblioteca.db") -> None:
        self.con = sqlite3.connect(ruta)
        self.con.execute("CREATE TABLE IF NOT EXISTS libros (codigo TEXT PRIMARY KEY, titulo TEXT)")

    def guardar(self, codigo: str, titulo: str) -> None:
        self.con.execute("INSERT OR REPLACE INTO libros VALUES (?, ?)", (codigo, titulo))
        self.con.commit()

    def listar(self) -> list[tuple[str, str]]:
        return self.con.execute("SELECT codigo, titulo FROM libros").fetchall()


# ── Creador base (Factory Method) ───────────────────────
class FabricaRepositorio(ABC):
    @abstractmethod
    def crear_repositorio(self) -> Repositorio:
        """Factory Method: cada subclase decide que repositorio crear."""

    def preparar(self) -> Repositorio:
        repo = self.crear_repositorio()
        Logger().info("Factory", f"Repositorio creado: {type(repo).__name__}")
        return repo


# ── Creadores concretos ─────────────────────────────────
class FabricaMemoria(FabricaRepositorio):
    def crear_repositorio(self) -> Repositorio:
        return RepositorioMemoria()


class FabricaArchivo(FabricaRepositorio):
    def crear_repositorio(self) -> Repositorio:
        return RepositorioArchivo()


class FabricaBD(FabricaRepositorio):
    def crear_repositorio(self) -> Repositorio:
        return RepositorioBD()


# ── Registro: entorno -> fabrica ────────────────────────
FABRICAS = {"memoria": FabricaMemoria, "archivo": FabricaArchivo, "bd": FabricaBD}


def fabrica_para(entorno: str | None = None) -> FabricaRepositorio:
    entorno = entorno or Config().entorno       # si no se indica, lo lee del .env
    if entorno not in FABRICAS:
        raise ValueError(f"Entorno no soportado: {entorno}")
    return FABRICAS[entorno]()