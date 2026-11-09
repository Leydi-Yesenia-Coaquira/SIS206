// ✅ Abstract Factory: familia de componentes de UI académica
#include <memory>
#include <string>
#include <iostream>

// ── Productos abstractos ────────────────────────────────
class Boton {
public:
    virtual ~Boton() = default;
    virtual void render() const = 0;
    virtual void onClick(const std::string& accion) const = 0;
};

class CampoTexto {
public:
    virtual ~CampoTexto() = default;
    virtual void render() const = 0;
    virtual std::string getValue() const = 0;
};

// ── Familia Tkinter ─────────────────────────────────────
class BotonTkinter : public Boton {
public:
    void render() const override { std::cout << "[Tk] Button rendered\n"; }
    void onClick(const std::string& a) const override
        { std::cout << "[Tk] Button.command=" << a << "\n"; }
};
class CampoTextoTkinter : public CampoTexto {
public:
    void render() const override { std::cout << "[Tk] Entry rendered\n"; }
    std::string getValue() const override { return "tk_value"; }
};

// ── Familia PyQt5 ───────────────────────────────────────
class BotonPyQt : public Boton {
public:
    void render() const override { std::cout << "[Qt] QPushButton rendered\n"; }
    void onClick(const std::string& a) const override
        { std::cout << "[Qt] clicked.connect(" << a << ")\n"; }
};
class CampoTextoPyQt : public CampoTexto {
public:
    void render() const override { std::cout << "[Qt] QLineEdit rendered\n"; }
    std::string getValue() const override { return "qt_value"; }
};

// ── Abstract Factory ────────────────────────────────────
class UIFactory {
public:
    virtual ~UIFactory() = default;
    [[nodiscard]] virtual std::unique_ptr<Boton>      crearBoton()      const = 0;
    [[nodiscard]] virtual std::unique_ptr<CampoTexto> crearCampoTexto() const = 0;
    [[nodiscard]] virtual std::string nombre() const noexcept = 0;
};

class UIFactoryTkinter : public UIFactory {
public:
    std::unique_ptr<Boton>      crearBoton()      const override { return std::make_unique<BotonTkinter>(); }
    std::unique_ptr<CampoTexto> crearCampoTexto() const override { return std::make_unique<CampoTextoTkinter>(); }
    std::string nombre() const noexcept override { return "Tkinter"; }
};

class UIFactoryPyQt : public UIFactory {
public:
    std::unique_ptr<Boton>      crearBoton()      const override { return std::make_unique<BotonPyQt>(); }
    std::unique_ptr<CampoTexto> crearCampoTexto() const override { return std::make_unique<CampoTextoPyQt>(); }
    std::string nombre() const noexcept override { return "PyQt5"; }
};

// ── Código cliente: solo conoce la fábrica abstracta ────
class FormularioMatricula {
    std::unique_ptr<Boton>      btnMatricular_;
    std::unique_ptr<CampoTexto> campoEstudiante_;
public:
    explicit FormularioMatricula(const UIFactory& factory)
        : btnMatricular_(factory.crearBoton()),
          campoEstudiante_(factory.crearCampoTexto()) {}

    void mostrar() const {
        campoEstudiante_->render();
        btnMatricular_->render();
        btnMatricular_->onClick("matricular_estudiante");
    }
};

int main() {
    // Cambia solo la fábrica → toda la UI cambia consistentemente
    UIFactoryTkinter tkFactory;
    FormularioMatricula frmTk(tkFactory);
    frmTk.mostrar();

    UIFactoryPyQt qtFactory;
    FormularioMatricula frmQt(qtFactory);
    frmQt.mostrar();
    return 0;
}
