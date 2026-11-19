# leer_csv.py 
from repositorio_csv import RepositorioCSV

repo = RepositorioCSV("estudiantes.csv")

print("Estudiantes cargados desde el archivo:")
for e in repo.listar():
    print(f"  {e.codigo} - {e.nombre} - PPA: {e.ppa} - Notas: {e.notas}")
print("Total:", len(repo.listar()))