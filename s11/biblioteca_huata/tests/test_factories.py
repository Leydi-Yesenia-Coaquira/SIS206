# Pruebas con pytest y mocks: los factories crean el tipo correcto
# Ejecutar desde la carpeta biblioteca_huata:   python -m pytest -v
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from factory import (FabricaArchivo, FabricaBD, FabricaMemoria, RepositorioArchivo,
                     RepositorioBD, RepositorioMemoria, fabrica_para)
from singleton import Config, Logger
from ui_factory import (FormularioBusqueda, UIFactory, UIFactoryPyQt5, UIFactoryTkinter,
                        fabrica_ui_para)
from ui_factory.ui import (MenuPyQt5, MenuTkinter, TablaPyQt5, TablaTkinter,
                           VentanaPyQt5, VentanaTkinter)


# ── Singleton ───────────────────────────────────────────
def test_singletons_son_unicos():
    assert Logger() is Logger()
    assert Config() is Config()


# ── Factory Method: cada entorno crea su repositorio ────
@pytest.mark.parametrize("entorno, fabrica_esperada, repo_esperado", [
    ("memoria", FabricaMemoria, RepositorioMemoria),
    ("archivo", FabricaArchivo, RepositorioArchivo),
    ("bd",      FabricaBD,      RepositorioBD),
])
def test_factory_method_crea_el_repositorio_correcto(entorno, fabrica_esperada, repo_esperado):
    config_falsa = MagicMock(entorno=entorno)                     # mock de Config
    with patch("factory.repositorios.Config", return_value=config_falsa), \
         patch("factory.repositorios.sqlite3.connect"):           # mock de la BD
        fabrica = fabrica_para()                                  # lee el entorno del mock
        repo = fabrica.crear_repositorio()
    assert isinstance(fabrica, fabrica_esperada)
    assert isinstance(repo, repo_esperado)


def test_fabrica_bd_abre_la_base_sin_tocar_disco():
    with patch("factory.repositorios.sqlite3.connect") as connect_falso:
        FabricaBD().crear_repositorio()
    connect_falso.assert_called_once_with("biblioteca.db")


def test_preparar_registra_en_el_logger():
    logger_falso = MagicMock()
    with patch("factory.repositorios.Logger", return_value=logger_falso):
        FabricaMemoria().preparar()
    logger_falso.info.assert_called_once()


def test_entorno_no_soportado():
    with pytest.raises(ValueError):
        fabrica_para("nube")


# ── Abstract Factory: cada familia crea sus componentes ─
@pytest.mark.parametrize("ui, fabrica_esperada, ventana, menu, tabla", [
    ("tkinter", UIFactoryTkinter, VentanaTkinter, MenuTkinter, TablaTkinter),
    ("pyqt5",   UIFactoryPyQt5,   VentanaPyQt5,   MenuPyQt5,   TablaPyQt5),
])
def test_abstract_factory_crea_la_familia_correcta(ui, fabrica_esperada, ventana, menu, tabla):
    config_falsa = MagicMock(ui=ui)
    with patch("ui_factory.ui.Config", return_value=config_falsa):
        fabrica = fabrica_ui_para()
    assert isinstance(fabrica, fabrica_esperada)
    assert isinstance(fabrica.crear_ventana(), ventana)
    assert isinstance(fabrica.crear_menu(), menu)
    assert isinstance(fabrica.crear_tabla(), tabla)


def test_formulario_usa_la_fabrica_sin_conocer_la_familia():
    fabrica_falsa = MagicMock(spec=UIFactory)                     # mock de la fabrica
    repo_falso = MagicMock()
    repo_falso.listar.return_value = [("L-001", "Yawar Fiesta")]

    FormularioBusqueda(fabrica_falsa, repo_falso).mostrar()

    fabrica_falsa.crear_ventana.assert_called_once()
    fabrica_falsa.crear_menu.assert_called_once()
    fabrica_falsa.crear_tabla.assert_called_once()
    fabrica_falsa.crear_tabla.return_value.mostrar_fila.assert_called_once_with("L-001", "Yawar Fiesta")