// main_strategy.cpp — Actividad 2A (C++17)
// Compilar: g++ -std=c++17 -o strategy main_strategy.cpp
// Ejecutar: .\strategy.exe
#include "contexto.h"
#include <iostream>
#include <iomanip>

int main() {
    std::cout << std::fixed << std::setprecision(1);

    // Ejemplo de la guía
    std::vector<double> notas = {10.0, 15.0, 18.0, 20.0, 12.0};
    ContextoCalculoPPA ctx(std::make_unique<PromedioSimple>());
    double ppa_simple = ctx.calcular(notas);            // 15.0
    ctx.setEstrategia(std::make_unique<PromedioModerado>());
    double ppa_mod = ctx.calcular(notas);               // 15.0
    std::cout << "Simple=" << ppa_simple << "  Moderado=" << ppa_mod << "\n";

    // Notas con un extremo muy bajo: aquí SÍ hay diferencia
    std::vector<double> notas2 = {5.0, 15.0, 16.0, 17.0, 20.0};
    ctx.setEstrategia(std::make_unique<PromedioSimple>());
    double s2 = ctx.calcular(notas2);
    ctx.setEstrategia(std::make_unique<PromedioModerado>());
    double m2 = ctx.calcular(notas2);
    std::cout << "Simple=" << s2 << "  Moderado=" << m2
              << "  Diferencia=" << (m2 - s2) << "\n";

    // ADICIONAL: PromedioGeometrico
    ctx.setEstrategia(std::make_unique<PromedioGeometrico>());
    std::cout << std::setprecision(2)
              << "Geometrico=" << ctx.calcular(notas) << "\n";
    return 0;
}