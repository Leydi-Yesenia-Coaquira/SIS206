// EstudianteGod.h — VIOLACIÓN de SRP — NO copiar como solución
#pragma once
#include <string>
#include <vector>
#include <fstream>
#include <iostream>

class EstudianteGod {
public:
    // DATOS DEL ESTUDIANTE: esta es la única responsabilidad
    // que debería tener la clase.
    int codigo;
    std::string nombre;
    float ppa;
    std::vector<float> notas;

    // Responsabilidad 1: cálculo
    // Calcula el promedio de las notas.
    // Razón para cambiar: si cambia la fórmula del PPA
    // (por ejemplo, usar créditos o descartar notas extremas).
    // En la solución se mueve a IEstrategiaCalculo / PromedioSimple.
    float calcularPPA() {
        if (notas.empty()) return 0.0f;
        float s = 0; for (auto n: notas) s+=n;
        return s / notas.size();
    }

    // Responsabilidad 2: persistencia
    // Guarda los datos del estudiante en un archivo.
    // Razón para cambiar: si se cambia el archivo por una
    // base de datos (SQLite, MySQL) o por otro formato.
    // En la solución se mueve a IRepositorioEstudiante.
    void guardarEnArchivo(const std::string& ruta) {
        std::ofstream f(ruta);
        f << codigo << "," << nombre << "," << ppa << std::endl;
    }

    // Responsabilidad 3: serialización
    // Convierte el objeto en texto JSON.
    // Razón para cambiar: si se pide otro formato (XML, CSV)
    // o se agregan más campos al JSON.
    // Nota: se corrigieron las comillas con \" para que compile.
    std::string toJson() {
        //return "{"codigo":"+std::to_string(codigo)+"}";
        return "{\"codigo\":"+std::to_string(codigo)+"}";
    }

    // Responsabilidad 4: notificación
    // Envía un aviso al estudiante.
    // Razón para cambiar: si se usa SMS, WhatsApp u otro
    // medio en lugar de correo.
    void enviarCorreo(const std::string& dest) {
        std::cout << "Enviando correo a " << dest << std::endl;
    }
};
