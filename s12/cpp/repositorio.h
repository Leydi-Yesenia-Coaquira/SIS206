// repositorio.h — interfaz + repositorio en memoria
#pragma once
#include "estudiante.h"
#include <map>
#include <optional>
#include <vector>

struct IRepositorioEstudiante {
    virtual void guardar(const Estudiante& e) = 0;
    virtual std::optional<Estudiante> buscar(int codigo) const = 0;
    virtual std::vector<Estudiante> listar() const = 0;
    virtual ~IRepositorioEstudiante() = default;
};

class RepositorioMemoria : public IRepositorioEstudiante {
    std::map<int, Estudiante> datos_;
public:
    void guardar(const Estudiante& e) override {
        datos_.insert_or_assign(e.codigo(), e);
    }
    std::optional<Estudiante> buscar(int codigo) const override {
        auto it = datos_.find(codigo);
        if (it == datos_.end()) return std::nullopt;
        return it->second;
    }
    std::vector<Estudiante> listar() const override {
        std::vector<Estudiante> v;
        for (const auto& [cod, e] : datos_) v.push_back(e);
        return v;
    }
};