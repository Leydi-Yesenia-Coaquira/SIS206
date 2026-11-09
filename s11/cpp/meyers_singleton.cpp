// ✅ Singleton Meyers — thread-safe desde C++11 por garantía del estándar
// (Código de la guía, sección 2.1 Forma 1, con los cambios marcados  // [CAMBIO])
#include <string>
#include <iostream>
#include <fstream>
#include <mutex>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <stdexcept>   // [CAMBIO] necesario para std::runtime_error
#include <cassert>     // [CAMBIO] necesario para assert (punto 3 de la actividad)

enum class NivelLog { DEBUG, INFO, WARN, ERROR };

class Logger {
private:
    std::ofstream archivo_;
    std::mutex mtx_;
    NivelLog nivelMinimo_;

    // Constructor privado: nadie puede crear instancias directamente
    explicit Logger(const std::string& ruta = "app.log",
                    NivelLog nivel = NivelLog::DEBUG)   // [CAMBIO] INFO -> DEBUG para que se registren los 4 niveles
        : nivelMinimo_(nivel) {
        archivo_.open(ruta, std::ios::app);
        if (!archivo_.is_open())
            throw std::runtime_error("No se puede abrir " + ruta);
    }

    // Eliminar copia y movimiento — garantiza unicidad
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;
    Logger(Logger&&) = delete;
    Logger& operator=(Logger&&) = delete;

    std::string timestamp() const {
        auto now = std::chrono::system_clock::now();
        auto t = std::chrono::system_clock::to_time_t(now);
        std::ostringstream oss;
        oss << std::put_time(std::localtime(&t), "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }

    static std::string nivelStr(NivelLog n) {
        switch(n) {
            case NivelLog::DEBUG: return "DEBUG";
            case NivelLog::INFO:  return "INFO ";
            case NivelLog::WARN:  return "WARN ";
            case NivelLog::ERROR: return "ERROR";
        }
        return "?????";
    }

public:
    // Punto de acceso único — static local
    static Logger& instancia(const std::string& ruta = "app.log") {
        static Logger inst(ruta); // se crea UNA sola vez, garantía C++11
        return inst;
    }

    // [CAMBIO] permite cambiar el nivel mínimo para filtrar mensajes
    void setNivelMinimo(NivelLog nivel) {
        std::lock_guard<std::mutex> lock(mtx_);
        nivelMinimo_ = nivel;
    }

    void log(NivelLog nivel, const std::string& modulo,
             const std::string& mensaje) {
        if (nivel < nivelMinimo_) return;
        std::lock_guard<std::mutex> lock(mtx_);
        std::string entrada = "[" + timestamp() + "] [" +
            nivelStr(nivel) + "] [" + modulo + "] " + mensaje;
        archivo_ << entrada << "\n";
        archivo_.flush();
        std::cout << entrada << "\n";
    }

    // [CAMBIO] faltaba el método para el nivel DEBUG
    void debug(const std::string& mod, const std::string& msg)
        { log(NivelLog::DEBUG, mod, msg); }
    void info (const std::string& mod, const std::string& msg)
        { log(NivelLog::INFO, mod, msg); }
    void warn (const std::string& mod, const std::string& msg)
        { log(NivelLog::WARN, mod, msg); }
    void error(const std::string& mod, const std::string& msg)
        { log(NivelLog::ERROR, mod, msg); }
};

// ── Uso: mismo objeto en cualquier parte del sistema ──
class ServicioMatricula {
public:
    void matricular(const std::string& est, const std::string& curso) {
        Logger::instancia().info("ServicioMatricula",
            "Matriculando " + est + " en " + curso);
        Logger::instancia().debug("ServicioMatricula",          // [CAMBIO]
            "Validando cupos del curso " + curso);
        // ... lógica de matrícula
        Logger::instancia().info("ServicioMatricula", "Matrícula exitosa");
    }
};

int main() {
    Logger::instancia().info("Main", "Sistema iniciado");
    ServicioMatricula svc;
    svc.matricular("2023001", "SIS206");
    Logger::instancia().warn("Main", "Carga alta detectada");
    Logger::instancia().error("Main", "No se pudo conectar al servidor de notas"); // [CAMBIO]

    // [CAMBIO] prueba del filtro: con nivel mínimo WARN, DEBUG e INFO no se registran
    Logger::instancia().setNivelMinimo(NivelLog::WARN);
    Logger::instancia().debug("Main", "Este mensaje NO debe aparecer");
    Logger::instancia().info ("Main", "Este tampoco");
    Logger::instancia().setNivelMinimo(NivelLog::DEBUG);

    // &Logger::instancia() == &Logger::instancia() → true siempre
    std::cout << "Misma instancia: " << std::boolalpha
              << (&Logger::instancia() == &Logger::instancia()) << std::endl;

    // [CAMBIO] verificación con assert (punto 3): si fueran distintas, el programa se detiene
    assert(&Logger::instancia() == &Logger::instancia());
    std::cout << "assert OK: siempre es la misma instancia" << std::endl;
    return 0;
}