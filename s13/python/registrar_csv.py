# registrar_csv.py 
from repositorio_csv import RepositorioCSV
from estudiante import Estudiante

repo = RepositorioCSV("estudiantes.csv")  # se crea en esta misma carpeta

repo.guardar(Estudiante(1001, "Ana Quispe", 15.5, [14.0, 18.0, 14.5]))
repo.guardar(Estudiante(1002, "Juan Mamani", 12.0, [10.0, 12.0, 14.0]))
repo.guardar(Estudiante(1003, "Rosa Condori", 16.0, [15.0, 17.0, 16.0]))

print("Se registraron", len(repo.listar()), "estudiantes en estudiantes.csv ✓")