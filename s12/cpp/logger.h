// logger.h — Singleton
#pragma once
#include <string>
#include <vector>
#include <iostream>
#include <ctime>

class Logger {
    std::vector<std::string> entradas_;
    Logger() = default;
public:
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

    static Logger& getInstance() {
        static Logger instancia;
        return instancia;
    }

    void log(const std::string& msg) {
        std::time_t t = std::time(nullptr);
        char hora[9];
        std::strftime(hora, sizeof(hora), "%H:%M:%S", std::localtime(&t));
        std::string linea = std::string("[LOG] ") + hora + " " + msg;
        entradas_.push_back(linea);
        std::cout << linea << std::endl;
    }

    const std::vector<std::string>& getEntradas() const { return entradas_; }
};