// Actividad 3 - Abstract Factory: UI multiplataforma
// Sistema del Proyecto Final: Biblioteca Digital Huata
// (basado en el ejemplo de la guia, seccion 4)
#include <memory>
#include <string>
#include <iostream>

// ── 1. Productos abstractos ─────────────────────────────
class VentanaPrincipal {
public:
    virtual ~VentanaPrincipal() = default;
    virtual void render(const std::string& titulo) const = 0;
};

class MenuNavegacion {
public:
    virtual ~MenuNavegacion() = default;
    virtual void agregarOpcion(const std::string& opcion) const = 0;
};

class TablaResultados {
public:
    virtual ~TablaResultados() = default;
    virtual void mostrarFila(const std::string& codigo, const std::string& titulo) const = 0;
};

// ── 2a. Familia Tkinter ─────────────────────────────────
class VentanaTkinter : public VentanaPrincipal {
public:
    void render(const std::string& t) const override
        { std::cout << "[Tk] Tk() ventana: " << t << "\n"; }
};
class MenuTkinter : public MenuNavegacion {
public:
    void agregarOpcion(const std::string& o) const override
        { std::cout << "[Tk] Menu.add_command(label='" << o << "')\n"; }
};
class TablaTkinter : public TablaResultados {
public:
    void mostrarFila(const std::string& c, const std::string& t) const override
        { std::cout << "[Tk] Treeview.insert: " << c << " | " << t << "\n"; }
};

// ── 2b. Familia PyQt5 ───────────────────────────────────
class VentanaPyQt5 : public VentanaPrincipal {
public:
    void render(const std::string& t) const override
        { std::cout << "[Qt] QMainWindow: " << t << "\n"; }
};
class MenuPyQt5 : public MenuNavegacion {
public:
    void agregarOpcion(const std::string& o) const override
        { std::cout << "[Qt] QMenuBar.addAction('" << o << "')\n"; }
};
class TablaPyQt5 : public TablaResultados {
public:
    void mostrarFila(const std::string& c, const std::string& t) const override
        { std::cout << "[Qt] QTableWidget.setItem: " << c << " | " << t << "\n"; }
};

// ── Abstract Factory ────────────────────────────────────
class UIFactory {
public:
    virtual ~UIFactory() = default;
    virtual std::unique_ptr<VentanaPrincipal> crearVentana() const = 0;
    virtual std::unique_ptr<MenuNavegacion>   crearMenu() const = 0;
    virtual std::unique_ptr<TablaResultados>  crearTabla() const = 0;
    virtual std::string nombre() const = 0;
};

class UIFactoryTkinter : public UIFactory {
public:
    std::unique_ptr<VentanaPrincipal> crearVentana() const override { return std::make_unique<VentanaTkinter>(); }
    std::unique_ptr<MenuNavegacion>   crearMenu()    const override { return std::make_unique<MenuTkinter>(); }
    std::unique_ptr<TablaResultados>  crearTabla()   const override { return std::make_unique<TablaTkinter>(); }
    std::string nombre() const override { return "Tkinter"; }
};

class UIFactoryPyQt5 : public UIFactory {
public:
    std::unique_ptr<VentanaPrincipal> crearVentana() const override { return std::make_unique<VentanaPyQt5>(); }
    std::unique_ptr<MenuNavegacion>   crearMenu()    const override { return std::make_unique<MenuPyQt5>(); }
    std::unique_ptr<TablaResultados>  crearTabla()   const override { return std::make_unique<TablaPyQt5>(); }
    std::string nombre() const override { return "PyQt5"; }
};

// ── 3. Cliente: solo conoce la fabrica abstracta ────────
class FormularioBusqueda {
    std::unique_ptr<VentanaPrincipal> ventana_;
    std::unique_ptr<MenuNavegacion>   menu_;
    std::unique_ptr<TablaResultados>  tabla_;

    // catalogo de ejemplo de la Biblioteca Huata
    std::string codigos_[4] = {"L-001", "L-002", "L-003", "L-004"};
    std::string titulos_[4] = {"Yawar Fiesta", "Los rios profundos",
                               "El mundo es ancho y ajeno", "Paco Yunque"};
public:
    explicit FormularioBusqueda(const UIFactory& factory)
        : ventana_(factory.crearVentana()),
          menu_(factory.crearMenu()),
          tabla_(factory.crearTabla()) {}

    void buscar(const std::string& texto) const {
        ventana_->render("Biblioteca Digital Huata - Busqueda");
        menu_->agregarOpcion("Buscar libro");
        menu_->agregarOpcion("Salir");
        std::cout << "Resultados para '" << texto << "':\n";
        for (int i = 0; i < 4; ++i)
            if (titulos_[i].find(texto) != std::string::npos)
                tabla_->mostrarFila(codigos_[i], titulos_[i]);
    }
};

int main() {
    // Cambia solo la fabrica → toda la UI cambia de familia
    UIFactoryTkinter tkFactory;
    FormularioBusqueda formTk(tkFactory);
    formTk.buscar("o");

    std::cout << "\n";

    UIFactoryPyQt5 qtFactory;
    FormularioBusqueda formQt(qtFactory);
    formQt.buscar("o");
    return 0;
}