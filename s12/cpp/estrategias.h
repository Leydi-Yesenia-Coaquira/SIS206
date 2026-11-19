// estrategias.h — Strategy para el cálculo del PPA
#pragma once
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>
#include <cmath>

// Interfaz Strategy
struct IEstrategiaCalculo {
    virtual double calcular(const std::vector<double>& notas) const = 0;
    virtual std::string nombre() const = 0;
    virtual ~IEstrategiaCalculo() = default;
};

// Promedio simple: suma / cantidad
struct PromedioSimple : IEstrategiaCalculo {
    double calcular(const std::vector<double>& notas) const override {
        if (notas.empty()) return 0.0;
        double suma = std::accumulate(notas.begin(), notas.end(), 0.0);
        return suma / notas.size();
    }
    std::string nombre() const override { return "PromedioSimple"; }
};

// Promedio moderado: quita la nota más baja y la más alta
struct PromedioModerado : IEstrategiaCalculo {
    double calcular(const std::vector<double>& notas) const override {
        if (notas.size() < 3) return PromedioSimple().calcular(notas);
        std::vector<double> v = notas;          // copia para ordenar
        std::sort(v.begin(), v.end());
        double suma = std::accumulate(v.begin() + 1, v.end() - 1, 0.0);
        return suma / (v.size() - 2);
    }
    std::string nombre() const override { return "PromedioModerado"; }
};

// ADICIONAL: Promedio geométrico: raíz n-ésima del producto
struct PromedioGeometrico : IEstrategiaCalculo {
    double calcular(const std::vector<double>& notas) const override {
        if (notas.empty()) return 0.0;
        double producto = 1.0;
        for (double n : notas) producto *= n;
        return std::pow(producto, 1.0 / notas.size());
    }
    std::string nombre() const override { return "PromedioGeometrico"; }
};