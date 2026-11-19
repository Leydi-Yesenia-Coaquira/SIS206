// Compilar: g++ -std=c++17 -o observer main.cpp
// Ejecutar: ./observer
#include "observer.h"
#include <iostream>

int main() {
    RepositorioMemoria repo_base;
    RepositorioObservable repo_obs(repo_base);

    ConsolaObserver vista;
    LoggerObserver  log_obs;
    EmailObserver   email;          // ADICIONAL
    repo_obs.suscribir(&vista);
    repo_obs.suscribir(&log_obs);
    repo_obs.suscribir(&email);

    repo_obs.guardar(Estudiante(1001, "Ana Quispe",  16.0, {14, 18, 16}));
    repo_obs.guardar(Estudiante(1002, "Juan Mamani", 12.3, {12, 15, 10}));

    std::cout << "\nEstudiantes en repositorio: " << repo_obs.listar().size() << "\n";
    std::cout << "Entradas de log: "
              << Logger::getInstance().getEntradas().size() << "\n";
    return 0;
}