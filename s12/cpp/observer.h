// observer.h
#pragma once
#include "estudiante.h"
#include "logger.h"       // AGREGADO
#include "repositorio.h"  // AGREGADO
#include <vector>
#include <iostream>       // AGREGADO
#include <string>         // AGREGADO

// Interfaz observer
struct IObserverEstudiante {
    virtual void on_guardado(const Estudiante& e) = 0;
    virtual ~IObserverEstudiante() = default;
};

// Observador: Logger
struct LoggerObserver : IObserverEstudiante {
    void on_guardado(const Estudiante& e) override {
        Logger::getInstance().log(
            "Guardado: [" + std::to_string(e.codigo()) + "] " + e.nombre());
    }
};

// Observador: Consola
struct ConsolaObserver : IObserverEstudiante {
    void on_guardado(const Estudiante& e) override {
        std::cout << ">> Vista: " << e.to_string() << std::endl;
    }
};

// ADICIONAL: Observador Email
struct EmailObserver : IObserverEstudiante {
    void on_guardado(const Estudiante& e) override {
        std::cout << "Enviando correo a " << e.nombre() << std::endl;
    }
};

// Subject
class RepositorioObservable {
    IRepositorioEstudiante& repo_;
    std::vector<IObserverEstudiante*> obs_;
public:
    explicit RepositorioObservable(IRepositorioEstudiante& r) : repo_(r) {}
    void suscribir(IObserverEstudiante* o) { obs_.push_back(o); }
    void guardar(const Estudiante& e) {
        repo_.guardar(e);
        for (auto* o : obs_) o->on_guardado(e);
    }
    // AGREGADO
    std::optional<Estudiante> buscar(int cod) const { return repo_.buscar(cod); }
    std::vector<Estudiante> listar() const { return repo_.listar(); }
};