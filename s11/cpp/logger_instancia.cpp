#include <cassert>
#include <iostream>

#define main main_logger            // evita choque con el main del otro archivo
#include "meyers_singleton.cpp"
#undef main

int main() {
    // Prueba 1: dos llamadas devuelven la misma direccion de memoria
    Logger& a = Logger::instancia();
    Logger& b = Logger::instancia();
    assert(&a == &b);
    std::cout << "Prueba 1 OK: misma direccion de memoria\n";

    // Prueba 2: varias llamadas seguidas, siempre el mismo objeto
    for (int i = 0; i < 100; ++i)
        assert(&Logger::instancia() == &a);
    std::cout << "Prueba 2 OK: 100 llamadas, misma instancia\n";

    // Prueba 3: un cambio hecho desde una referencia se ve desde la otra
    a.setNivelMinimo(NivelLog::ERROR);
    b.info("Test", "Este mensaje NO debe aparecer (nivel minimo ERROR)");
    b.error("Test", "Este SI aparece: el cambio de 'a' afecto a 'b'");
    std::cout << "Prueba 3 OK: a y b son el mismo objeto\n";

    std::cout << "\nTodas las pruebas assert pasaron.\n";
    return 0;
}