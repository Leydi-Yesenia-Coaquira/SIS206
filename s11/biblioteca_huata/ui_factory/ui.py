# PATRON 3: ABSTRACT FACTORY  ->  componentes de la GUI (Tkinter o PyQt5)
# (simulados con mensajes en consola, como en la Actividad 3)
from __future__ import annotations
from abc import ABC, abstractmethod

from singleton import Config


# ── Productos abstractos ────────────────────────────────
class VentanaPrincipal(ABC):
    @abstractmethod
    def render(self, titulo: str) -> None: ...


class MenuNavegacion(ABC):
    @abstractmethod
    def agregar_opcion(self, opcion: str) -> None: ...


class TablaResultados(ABC):
    @abstractmethod
    def mostrar_fila(self, codigo: str, titulo: str) -> None: ...


# ── Familia Tkinter ─────────────────────────────────────
class VentanaTkinter(VentanaPrincipal):
    def render(self, titulo: str) -> None: print(f"[Tk] Tk() ventana: {titulo}")

class MenuTkinter(MenuNavegacion):
    def agregar_opcion(self, opcion: str) -> None: print(f"[Tk] Menu.add_command('{opcion}')")

class TablaTkinter(TablaResultados):
    def mostrar_fila(self, codigo: str, titulo: str) -> None: print(f"[Tk] Treeview.insert: {codigo} | {titulo}")


# ── Familia PyQt5 ───────────────────────────────────────
class VentanaPyQt5(VentanaPrincipal):
    def render(self, titulo: str) -> None: print(f"[Qt] QMainWindow: {titulo}")

class MenuPyQt5(MenuNavegacion):
    def agregar_opcion(self, opcion: str) -> None: print(f"[Qt] QMenuBar.addAction('{opcion}')")

class TablaPyQt5(TablaResultados):
    def mostrar_fila(self, codigo: str, titulo: str) -> None: print(f"[Qt] QTableWidget.setItem: {codigo} | {titulo}")


# ── Abstract Factory ────────────────────────────────────
class UIFactory(ABC):
    @abstractmethod
    def crear_ventana(self) -> VentanaPrincipal: ...
    @abstractmethod
    def crear_menu(self) -> MenuNavegacion: ...
    @abstractmethod
    def crear_tabla(self) -> TablaResultados: ...


class UIFactoryTkinter(UIFactory):
    def crear_ventana(self) -> VentanaPrincipal: return VentanaTkinter()
    def crear_menu(self) -> MenuNavegacion: return MenuTkinter()
    def crear_tabla(self) -> TablaResultados: return TablaTkinter()


class UIFactoryPyQt5(UIFactory):
    def crear_ventana(self) -> VentanaPrincipal: return VentanaPyQt5()
    def crear_menu(self) -> MenuNavegacion: return MenuPyQt5()
    def crear_tabla(self) -> TablaResultados: return TablaPyQt5()


FABRICAS_UI = {"tkinter": UIFactoryTkinter, "pyqt5": UIFactoryPyQt5}


def fabrica_ui_para(ui: str | None = None) -> UIFactory:
    ui = ui or Config().ui                       # si no se indica, lo lee del .env
    if ui not in FABRICAS_UI:
        raise ValueError(f"UI no soportada: {ui}")
    return FABRICAS_UI[ui]()


# ── Cliente: no sabe que familia usa ────────────────────
class FormularioBusqueda:
    def __init__(self, factory: UIFactory, repo) -> None:
        self.repo = repo
        self.ventana = factory.crear_ventana()
        self.menu = factory.crear_menu()
        self.tabla = factory.crear_tabla()

    def mostrar(self) -> None:
        self.ventana.render("Biblioteca Digital Huata")
        self.menu.agregar_opcion("Buscar libro")
        self.menu.agregar_opcion("Salir")
        for codigo, titulo in self.repo.listar():
            self.tabla.mostrar_fila(codigo, titulo)