# test_json_persistencia.py
import os
import tempfile
from repositorio_json import RepositorioJSON
from estudiante import Estudiante

# Funciona en Windows y en Linux (no usa "/tmp" fijo)
RUTA = os.path.join(tempfile.gettempdir(), "estudiantes_test.json")


def test_persistencia_entre_instancias():
    # if os.path.exists(RUTA):
    #     os.remove(RUTA)  # empezar limpio

    # Primera instancia: guardar
    r1 = RepositorioJSON(RUTA)
    r1.guardar(Estudiante(1001, "Ana Quispe", 15.5, [14.0, 18.0, 14.5]))
    r1.guardar(Estudiante(1002, "Juan Mamani", 12.0, [10.0, 12.0, 14.0]))

    # Segunda instancia: verificar que los datos persisten
    r2 = RepositorioJSON(RUTA)
    ana = r2.buscar(1001)
    assert ana is not None
    assert ana.nombre == "Ana Quispe"
    assert abs(ana.ppa - 15.5) < 0.01
    juan = r2.buscar(1002)
    assert juan is not None
    assert len(r2.listar()) == 2

    print("Estudiantes en el archivo:", len(r2.listar()))
    print("Archivo guardado en:", RUTA)

    # os.remove(RUTA)  # limpiar


if __name__ == "__main__":
    test_persistencia_entre_instancias()
    print("RepositorioJSON: persistencia verificada ✓")