# Biblioteca Digital Huata — Actividad 5 (Semana 11, SIS206)

Integra 3 patrones GoF:

| Módulo | Patrón | Contenido |
|---|---|---|
| `singleton/` | Singleton | `Logger` y `Config` (lee `.env`) |
| `factory/` | Factory Method | Crea el repositorio según `ENTORNO`: memoria, archivo (JSON) o bd (SQLite) |
| `ui_factory/` | Abstract Factory | Componentes de la GUI según `UI`: tkinter o pyqt5 |

## Ejecutar

```
python main.py
python -m pytest -v
```

## Configuración (`.env`, se crea solo la primera vez)

```
ENTORNO=memoria     # memoria | archivo | bd
UI=tkinter          # tkinter | pyqt5
```

## Diagrama

`uml