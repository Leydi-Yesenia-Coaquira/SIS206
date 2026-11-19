// estudiante.h — Modelo
#pragma once
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>

class Estudiante {
    int codigo_;
    std::string nombre_;
    double ppa_;
    std::vector<double> notas_;
public:
    Estudiante(int codigo, std::string nombre, double ppa = 0.0,
               std::vector<double> notas = {})
        : codigo_(codigo), nombre_(std::move(nombre)), ppa_(ppa),
          notas_(std::move(notas)) {}

    int codigo() const { return codigo_; }
    const std::string& nombre() const { return nombre_; }
    double ppa() const { return ppa_; }
    const std::vector<double>& notas() const { return notas_; }
    void set_ppa(double p) { ppa_ = p; }

    std::string to_string() const {
        std::ostringstream os;
        os << "[" << codigo_ << "] " << nombre_
           << " — PPA: " << std::fixed << std::setprecision(1) << ppa_;
        return os.str();
    }
};