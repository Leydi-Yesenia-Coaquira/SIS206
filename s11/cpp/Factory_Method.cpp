// ✅ Factory Method: generadores de reporte intercambiables
#include <string>
#include <memory>
#include <vector>
#include <iostream>
#include <stdexcept>
#include <map>
#include <functional>

// ── Producto abstracto ──────────────────────────────────
class ReporteAcademico {
public:
    virtual ~ReporteAcademico() = default;
    virtual void agregarDato(const std::string& clave,
                              const std::string& valor) = 0;
    virtual std::string generar() const = 0;
    [[nodiscard]] virtual std::string formato() const noexcept = 0;
    [[nodiscard]] virtual std::string extension() const noexcept = 0;
};

// ── Productos concretos ─────────────────────────────────
class ReporteTXT : public ReporteAcademico {
    std::vector<std::pair<std::string,std::string>> datos_;
public:
    void agregarDato(const std::string& k, const std::string& v) override {
        datos_.emplace_back(k, v);
    }
    std::string generar() const override {
        std::string r = "=== REPORTE ACADÉMICO ===\n";
        for (auto& [k,v] : datos_) r += k + ": " + v + "\n";
        return r;
    }
    std::string formato() const noexcept override { return "Texto plano"; }
    std::string extension() const noexcept override { return ".txt"; }
};

class ReporteCSV : public ReporteAcademico {
    std::vector<std::pair<std::string,std::string>> datos_;
public:
    void agregarDato(const std::string& k, const std::string& v) override {
        datos_.emplace_back(k, v);
    }
    std::string generar() const override {
        std::string r = "campo,valor\n";
        for (auto& [k,v] : datos_) r += k + "," + v + "\n";
        return r;
    }
    std::string formato() const noexcept override { return "CSV"; }
    std::string extension() const noexcept override { return ".csv"; }
};

class ReporteHTML : public ReporteAcademico {
    std::vector<std::pair<std::string,std::string>> datos_;
public:
    void agregarDato(const std::string& k, const std::string& v) override {
        datos_.emplace_back(k, v);
    }
    std::string generar() const override {
        std::string r = "<table border='1'>\n<tr><th>Campo</th><th>Valor</th></tr>\n";
        for (auto& [k,v] : datos_)
            r += "<tr><td>" + k + "</td><td>" + v + "</td></tr>\n";
        return r + "</table>";
    }
    std::string formato() const noexcept override { return "HTML"; }
    std::string extension() const noexcept override { return ".html"; }
};

// ── Creador base (Factory Method) ───────────────────────
class GeneradorReporte {
public:
    virtual ~GeneradorReporte() = default;
    // Factory Method: subclases sobrescriben
    [[nodiscard]] virtual std::unique_ptr<ReporteAcademico> crearReporte() const = 0;

    // Template Method: usa el producto sin saber qué es
    void procesarYGuardar(const std::string& estudiante,
                        double promedio) const {
        auto reporte = crearReporte();  // ← factory method
        reporte->agregarDato("Estudiante", estudiante);
        reporte->agregarDato("Promedio",
                            std::to_string(promedio));
        reporte->agregarDato("Estado",
                            promedio >= 11.0 ? "Aprobado" : "Desaprobado");
        std::string contenido = reporte->generar();
        std::string archivo   = "reporte_" + estudiante + reporte->extension();
        std::cout << "[" << reporte->formato() << "] Guardando en: "
                  << archivo << "\n" << contenido << std::endl;
    }
};

// ── Creadores concretos ──────────────────────────────────
class GeneradorTXT  : public GeneradorReporte {
    std::unique_ptr<ReporteAcademico> crearReporte() const override {
        return std::make_unique<ReporteTXT>();
    }
};
class GeneradorCSV  : public GeneradorReporte {
    std::unique_ptr<ReporteAcademico> crearReporte() const override {
        return std::make_unique<ReporteCSV>();
    }
};
class GeneradorHTML : public GeneradorReporte {
    std::unique_ptr<ReporteAcademico> crearReporte() const override {
        return std::make_unique<ReporteHTML>();
    }
};

// ── Registro de fábricas (Registry Pattern + Factory) ────
class RegistroGeneradores {
    using CreadorFn = std::function<std::unique_ptr<GeneradorReporte>()>;
    std::map<std::string, CreadorFn> registro_;
public:
    void registrar(const std::string& fmt, CreadorFn fn) {
        registro_[fmt] = std::move(fn);
    }
    std::unique_ptr<GeneradorReporte> crear(const std::string& fmt) const {
        auto it = registro_.find(fmt);
        if (it == registro_.end())
            throw std::invalid_argument("Formato no registrado: " + fmt);
        return it->second();
    }
};

int main() {
    RegistroGeneradores reg;
    reg.registrar("txt",  [] { return std::make_unique<GeneradorTXT>(); });
    reg.registrar("csv",  [] { return std::make_unique<GeneradorCSV>(); });
    reg.registrar("html", [] { return std::make_unique<GeneradorHTML>(); });

    // Código cliente NO depende de clases concretas
    for (const auto& fmt : {"txt", "csv", "html"}) {
        auto gen = reg.crear(fmt);
        gen->procesarYGuardar("Maria Quispe", 15.75);
    }
    return 0;
}
