// contexto.h — Contexto del patrón Strategy
#pragma once
#include "estrategias.h"
#include "logger.h"
#include <memory>

class ContextoCalculoPPA {
    std::unique_ptr<IEstrategiaCalculo> est_;   // dueño de la estrategia
public:
    explicit ContextoCalculoPPA(std::unique_ptr<IEstrategiaCalculo> e)
        : est_(std::move(e)) {}

    void setEstrategia(std::unique_ptr<IEstrategiaCalculo> e) {
        Logger::getInstance().log("Estrategia cambiada a " + e->nombre());
        est_ = std::move(e);   // la estrategia anterior se borra sola
    }

    double calcular(const std::vector<double>& notas) const {
        return est_->calcular(notas);
    }
};