# Biblioteca Digital Huata - integra los 3 patrones
from factory import fabrica_para
from singleton import Config, Logger
from ui_factory import FormularioBusqueda, fabrica_ui_para

if __name__ == "__main__":
    config = Config()                                   # 1. Singleton
    log = Logger()                                      #    Singleton
    log.info("Main", f"Entorno: {config.entorno} | UI: {config.ui}")

    repo = fabrica_para(config.entorno).preparar()      # 2. Factory Method
    repo.guardar("L-001", "Yawar Fiesta")
    repo.guardar("L-002", "Los rios profundos")
    repo.guardar("L-003", "Paco Yunque")

    fabrica_ui = fabrica_ui_para(config.ui)             # 3. Abstract Factory
    FormularioBusqueda(fabrica_ui, repo).mostrar()