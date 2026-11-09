from threading import Thread

from singleton import ConfiguracionApp


def test_misma_instancia():
    cfg1 = ConfiguracionApp()
    cfg2 = ConfiguracionApp()
    assert cfg1 is cfg2                 # es el mismo objeto


def test_mismo_id_en_memoria():
    assert id(ConfiguracionApp()) == id(ConfiguracionApp())


def test_misma_instancia_con_varios_hilos():
    resultados = []

    def crear():
        resultados.append(ConfiguracionApp())

    hilos = [Thread(target=crear) for _ in range(10)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()

    assert all(obj is resultados[0] for obj in resultados)