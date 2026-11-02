// solid_s10.cpp — Semana 10: Refactorización SRP + DIP en C++17
// Compilar: g++ -std=c++17 solid_s10.cpp -o solid
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <optional>
#include <algorithm>
#include <numeric>

// ─── 1. Solo datos (SRP: 1 razón para cambiar) ──────────────
class Estudiante {
public:
    Estudiante(int cod, std::string nom, float ppa)
        : codigo_(cod), nombre_(std::move(nom)), ppa_(ppa) {}
    [[nodiscard]] int         codigo() const { return codigo_; }
    [[nodiscard]] std::string nombre() const { return nombre_; }
    [[nodiscard]] float       ppa()    const { return ppa_; }
    void set_ppa(float v) { ppa_ = v; }
private:
    int codigo_; std::string nombre_; float ppa_;
};

// 2. Solo cálculo 
struct IEstrategiaCalculo {
    virtual float calcular(const std::vector<float>&) const = 0;
    virtual ~IEstrategiaCalculo() = default;
};

struct PromedioSimple : IEstrategiaCalculo {
    float calcular(const std::vector<float>& n) const override {
        if (n.empty()) return 0.0f;
        float s = 0; for (auto x : n) s += x;
        return s / n.size();
    }
};

// ─── ACTIVIDAD 2A — OCP ─────────────────────────────────────
// Nueva estrategia agregada SIN modificar ServicioEstudiante.
// Descarta la nota más alta y la más baja antes de promediar.
struct PromedioModerado : IEstrategiaCalculo {
    float calcular(const std::vector<float>& notas) const override {
        if (notas.size() <= 2) return 0.0f;
        auto sorted = notas;                       // copia para no alterar las originales
        std::sort(sorted.begin(), sorted.end());   // ordena de menor a mayor
        float suma = std::accumulate(sorted.begin() + 1,   // salta la menor
                                     sorted.end() - 1,     // salta la mayor
                                     0.0f);
        return suma / (sorted.size() - 2);
    }
};

// ─── 3. Solo persistencia (interfaz DIP) ────────────────────
struct IRepositorioEstudiante {
    virtual void guardar(const Estudiante&) = 0;
    virtual std::optional<Estudiante> buscar(int) const = 0;
    virtual ~IRepositorioEstudiante() = default;
};

// Implementación en memoria (no venía en la guía para C++)
class RepositorioMemoria : public IRepositorioEstudiante {
    std::map<int, Estudiante> datos_;
public:
    void guardar(const Estudiante& e) override {
        datos_.insert_or_assign(e.codigo(), e);
    }
    std::optional<Estudiante> buscar(int cod) const override {
        auto it = datos_.find(cod);
        if (it == datos_.end()) return std::nullopt;
        return it->second;
    }
};

// ADICIONAL: guarda cada estudiante en un archivo .csv
class RepositorioArchivo : public IRepositorioEstudiante {
    std::string ruta_;
public:
    explicit RepositorioArchivo(std::string ruta) : ruta_(std::move(ruta)) {}

    void guardar(const Estudiante& e) override {
        std::ofstream f(ruta_, std::ios::app);   // app = agrega al final
        f << e.codigo() << "," << e.nombre() << "," << e.ppa() << "\n";
    }

    std::optional<Estudiante> buscar(int cod) const override {
        std::ifstream f(ruta_);
        std::string linea;
        while (std::getline(f, linea)) {
            auto p1 = linea.find(',');
            auto p2 = linea.rfind(',');
            if (p1 == std::string::npos || p1 == p2) continue;
            int c = std::stoi(linea.substr(0, p1));
            if (c == cod) {
                std::string nom = linea.substr(p1 + 1, p2 - p1 - 1);
                float ppa = std::stof(linea.substr(p2 + 1));
                return Estudiante(c, nom, ppa);
            }
        }
        return std::nullopt;
    }
};

// ─── 4. Orquestación (ServicioEstudiante usa DIP) ───────────
class ServicioEstudiante {
    IRepositorioEstudiante& repo_;
    IEstrategiaCalculo&     calc_;
public:
    ServicioEstudiante(IRepositorioEstudiante& r, IEstrategiaCalculo& c)
        : repo_(r), calc_(c) {}

    void registrar(Estudiante e, const std::vector<float>& notas) {
        e.set_ppa(calc_.calcular(notas));
        repo_.guardar(e);
    }
};

// Muestra el resultado de una búsqueda
void mostrar(const IRepositorioEstudiante& repo, int cod) {
    if (auto e = repo.buscar(cod))
        std::cout << "[" << e->codigo() << "] " << e->nombre()
                  << " - PPA: " << e->ppa() << "\n";
    else
        std::cout << "Estudiante " << cod << " no encontrado\n";
}

int main() {
    PromedioSimple calc;

    // Prueba 1: repositorio en memoria
    std::cout << "=== RepositorioMemoria ===\n";
    RepositorioMemoria repoMem;
    ServicioEstudiante svc(repoMem, calc);
    svc.registrar(Estudiante{1001, "Ana Quispe", 0.0f}, {14, 20, 16, 18, 12});
    svc.registrar(Estudiante{1002, "Luis Mamani", 0.0f}, {11, 13, 15});
    mostrar(repoMem, 1001);   // esperado: 16
    mostrar(repoMem, 1002);   // esperado: 13
    mostrar(repoMem, 9999);   // no existe

    // Prueba 2 (ADICIONAL): repositorio en archivo .csv
    std::cout << "\n=== RepositorioArchivo (estudiantes.csv) ===\n";
    std::remove("estudiantes.csv");   // empieza con archivo limpio
    RepositorioArchivo repoCsv("estudiantes.csv");
    ServicioEstudiante svcCsv(repoCsv, calc);   // ServicioEstudiante NO cambió
    svcCsv.registrar(Estudiante{1003, "Rosa Condori", 0.0f}, {17, 18, 19});
    mostrar(repoCsv, 1003);   // esperado: 18

    // ─── ACTIVIDAD 2A — OCP ─────────────────────────────────
    // Mismas notas, misma clase ServicioEstudiante.
    // Lo ÚNICO que cambia es la estrategia que se le pasa.
    std::vector<float> notasAna = {14.0f, 20.0f, 16.0f, 18.0f, 12.0f};

    std::cout << "\n=== Actividad 2A: PromedioModerado ===\n";
    RepositorioMemoria repoMod;
    PromedioModerado   calcMod;   // <- solo cambia esta línea
    ServicioEstudiante svcMod(repoMod, calcMod);
    svcMod.registrar(Estudiante{1001, "Ana Quispe", 0.0f}, notasAna);
    mostrar(repoMod, 1001);   // esperado: (14+16+18)/3 = 16

    std::cout << "\n=== Actividad 2A: PromedioSimple ===\n";
    RepositorioMemoria repoSim;
    PromedioSimple     calcSim;   // <- solo cambia esta línea
    ServicioEstudiante svcSim(repoSim, calcSim);
    svcSim.registrar(Estudiante{1001, "Ana Quispe", 0.0f}, notasAna);
    mostrar(repoSim, 1001);   // esperado: (14+20+16+18+12)/5 = 16

    // Con estas notas ambos dan 16 por coincidencia: el 12 y el 20
    // están a la misma distancia (4) del 16, así que se compensan.
    // Prueba con notas donde sí se nota la diferencia:
    std::vector<float> notasLuis = {5.0f, 15.0f, 16.0f, 17.0f, 18.0f};
    svcMod.registrar(Estudiante{1002, "Luis Mamani", 0.0f}, notasLuis);
    svcSim.registrar(Estudiante{1002, "Luis Mamani", 0.0f}, notasLuis);
    std::cout << "\n=== Notas de Luis {5, 15, 16, 17, 18} ===\n";
    std::cout << "Moderado: "; mostrar(repoMod, 1002);   // (15+16+17)/3 = 16
    std::cout << "Simple:   "; mostrar(repoSim, 1002);   // 71/5 = 14.2

    return 0;
}