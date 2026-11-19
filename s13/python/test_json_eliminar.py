# test_json_eliminar.py
import os
import json
import tempfile
from repositorio_json import RepositorioJSON
from estudiante import Estudiante

RUTA = os.path.join(tempfile.gettempdir(), "estudiantes_eliminar.json")


def test_eliminar_actualiza_archivo():
    if os.path.exists(RUTA):
        os.remove(RUTA)  # empezar limpio

    # 1. Guardar dos estudiantes
    r1 = RepositorioJSON(RUTA)
    r1.guardar(Estudiante(1001, "Ana Quispe", 15.5, [14.0, 18.0, 14.5]))
    r1.guardar(Estudiante(1002, "Juan Mamani", 12.0, [10.0, 12.0, 14.0]))

    # 2. Eliminar a Ana
    r1.eliminar(1001)

    # 3. Leer el archivo JSON directamente
    with open(RUTA, encoding="utf-8") as f:
        contenido = json.load(f)
    codigos = [item["codigo"] for item in contenido]
    assert 1001 not in codigos
    assert 1002 in codigos
    assert len(contenido) == 1

    # 4. Una nueva instancia tampoco debe encontrar a Ana
    r2 = RepositorioJSON(RUTA)
    assert r2.buscar(1001) is None
    assert r2.buscar(1002) is not None
    assert len(r2.listar()) == 1

    os.remove(RUTA)  # limpiar


if __name__ == "__main__":
    test_eliminar_actualiza_archivo()
    print("eliminar(): el archivo JSON se actualiza ✓")