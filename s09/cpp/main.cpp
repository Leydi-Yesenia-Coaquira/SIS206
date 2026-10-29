// main.cpp — Uso de la clase Estudiante
#include "estudiante.h"
#include <iostream>

int main() {
    Estudiante e{1001, "Ana Quispe", 15.5f, 3};
    e.agregar_nota(14.0f);
    e.agregar_nota(16.0f);
    e.agregar_nota(18.0f);
    std::cout << e.to_string() << std::endl;

    if (auto prom = e.calcular_promedio(); prom.has_value())
        std::cout << "Promedio semestral: " << prom.value() << std::endl;

    // Agregar una nota de 20.0 y verificar que el promedio cambia
    e.agregar_nota(20.0f);
    if (auto prom = e.calcular_promedio(); prom.has_value())
        std::cout << "Promedio con nota 20: " << prom.value() << std::endl;

    // ADICIONAL: es_aprobado()
    std::cout << "Aprobado: " << (e.es_aprobado() ? "Si" : "No") << std::endl;

    // Prueba de validacion
    try {
        Estudiante invalido{-1, "X", 5.0f, 1};
    } catch (const std::invalid_argument& ex) {
        std::cout << "Error esperado: " << ex.what() << std::endl;
    }
}
// Compilar: g++ -std=c++17 main.cpp -o main && ./main