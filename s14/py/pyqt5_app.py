# pyqt5_app.py
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLineEdit,
    QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView,
    QFileDialog)
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui  import QColor
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from estudiante import Estudiante
import sys


# ── Modelo ───────────────────────────────────────────
class ModeloAcademico(QObject):
    """Envuelve ServicioEstudiante y emite señales Qt."""
    estudiante_guardado = pyqtSignal(object)
    estudiante_eliminado = pyqtSignal(int)

    def __init__(self, svc) -> None:
        super().__init__()
        self._svc = svc

    def registrar(self, e) -> None:
        self._svc.registrar(e)
        self.estudiante_guardado.emit(e)

    def eliminar(self, cod: int) -> None:
        self._svc.eliminar(cod)
        self.estudiante_eliminado.emit(cod)

    def listar(self):
        return self._svc.listar()

    def buscar(self, cod: int):
        return self._svc.buscar(cod)


# ── Validaciones (las mismas reglas para registrar e importar) ──
def validar_codigo(texto) -> int:
    txt = str(texto).strip()
    if txt.endswith(".0"):              # Excel a veces da 1001.0
        txt = txt[:-2]
    if not txt.isdigit():
        raise ValueError("El código debe ser un número")
    if len(txt) > 4:
        raise ValueError("El código debe tener máximo 4 dígitos")
    return int(txt)


def validar_notas(texto) -> list:
    txt = str(texto or "").strip()
    try:
        notas = [float(x) for x in txt.split(",") if x.strip()]
    except ValueError:
        raise ValueError("Las notas deben ser números separados por comas")
    fuera = [n for n in notas if n < 0 or n > 20]
    if fuera:
        malas = ", ".join(f"{n:g}" for n in fuera)
        raise ValueError(f"Nota(s) fuera de rango: {malas}. "
                         "Solo se permiten notas de 0 a 20")
    return notas


# ── Vista ────────────────────────────────────────────
class VistaEstudiantes(QMainWindow):
    def __init__(self, modelo: ModeloAcademico) -> None:
        super().__init__()
        self._mod = modelo
        self.setWindowTitle(
            "SIS206 — Sistema Académico UNAP")
        self.resize(850, 520)
        self._construir_ui()
        # Observer: señal → slot
        self._mod.estudiante_guardado.connect(
            self._on_estudiante_guardado)
        self._mod.estudiante_eliminado.connect(
            self._on_estudiante_eliminado)
        self._recargar_tabla()

    def _construir_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Fila 1: registrar / eliminar
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Código:"))
        self._ed_cod = QLineEdit(); self._ed_cod.setMaximumWidth(80)
        hbox.addWidget(self._ed_cod)
        hbox.addWidget(QLabel("Nombre:"))
        self._ed_nom = QLineEdit()
        hbox.addWidget(self._ed_nom)
        hbox.addWidget(QLabel("Notas (,):"))
        self._ed_notas = QLineEdit(); self._ed_notas.setMaximumWidth(140)
        hbox.addWidget(self._ed_notas)
        btn_reg = QPushButton("Registrar")
        btn_reg.clicked.connect(self._registrar)
        hbox.addWidget(btn_reg)
        btn_eli = QPushButton("Eliminar")
        btn_eli.clicked.connect(self._eliminar)
        hbox.addWidget(btn_eli)
        layout.addLayout(hbox)

        # Fila 2: buscar / mostrar todos / excel
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Buscar cód.:"))
        self._ed_buscar = QLineEdit(); self._ed_buscar.setMaximumWidth(80)
        hbox2.addWidget(self._ed_buscar)
        btn_bus = QPushButton("Buscar")
        btn_bus.clicked.connect(self._buscar)
        hbox2.addWidget(btn_bus)
        btn_todos = QPushButton("Mostrar todos")
        btn_todos.clicked.connect(self._recargar_tabla)
        hbox2.addWidget(btn_todos)
        btn_exp = QPushButton("Exportar Excel")
        btn_exp.clicked.connect(self._exportar_excel)
        hbox2.addWidget(btn_exp)
        btn_imp = QPushButton("Importar Excel")
        btn_imp.clicked.connect(self._importar_excel)
        hbox2.addWidget(btn_imp)
        hbox2.addStretch()
        layout.addLayout(hbox2)

        # Fila 3: mensaje de error en rojo
        self._lbl_error = QLabel("")
        self._lbl_error.setStyleSheet(
            "color: red; font-weight: bold;")
        layout.addWidget(self._lbl_error)

        # Tabla
        self._tbl = QTableWidget(0, 4)
        self._tbl.setHorizontalHeaderLabels(
            ["Código", "Nombre", "PPA", "Notas"])
        self._tbl.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch)
        self._tbl.setEditTriggers(
            QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self._tbl)

    # ── Handlers ─────────────────────────────────────
    def _registrar(self) -> None:
        self._lbl_error.setText("")
        try:
            cod = validar_codigo(self._ed_cod.text())
            nom = self._ed_nom.text().strip()
            if not nom:
                raise ValueError("Nombre vacío")
            notas = validar_notas(self._ed_notas.text())
            self._mod.registrar(Estudiante(cod, nom, 0.0, notas))
            self._ed_cod.clear()
            self._ed_nom.clear()
            self._ed_notas.clear()
        except ValueError as ex:
            self._lbl_error.setText(f"⚠ {ex}")
            QMessageBox.critical(self, "Error", str(ex))

    def _eliminar(self) -> None:
        fila = self._tbl.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Seleccione un estudiante")
            return
        cod = int(self._tbl.item(fila, 0).text())
        resp = QMessageBox.question(self, "Confirmar",
            f"¿Eliminar al estudiante {cod}?")
        if resp == QMessageBox.Yes:
            self._mod.eliminar(cod)   # emite la señal → la tabla se recarga sola

    def _buscar(self) -> None:
        texto = self._ed_buscar.text().strip()
        if not texto.isdigit():
            QMessageBox.warning(self, "Aviso", "Escriba un código numérico")
            return
        e = self._mod.buscar(int(texto))
        if e is None:
            self._llenar_tabla([])
            self._lbl_error.setText("⚠ No se encontró el estudiante")
        else:
            self._lbl_error.setText("")
            self._llenar_tabla([e])

    def _exportar_excel(self) -> None:
        estudiantes = self._mod.listar()
        if not estudiantes:
            QMessageBox.warning(self, "Aviso", "No hay estudiantes para exportar")
            return
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar como", "estudiantes.xlsx",
            "Archivo de Excel (*.xlsx)")
        if not ruta:
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "Estudiantes"
        ws.append(["Código", "Nombre", "Notas", "PPA"])
        for celda in ws[1]:
            celda.font = Font(bold=True, color="FFFFFF")
            celda.fill = PatternFill("solid", fgColor="5B2C83")
        for e in estudiantes:
            notas = ", ".join(f"{n:g}" for n in e.notas)
            ws.append([e.codigo, e.nombre, notas, round(e.ppa, 2)])
            fila = ws.max_row
            ws.cell(fila, 1).number_format = "0000"
            ws.cell(fila, 4).number_format = "0.00"
        ws.column_dimensions["A"].width = 10
        ws.column_dimensions["B"].width = 30
        ws.column_dimensions["C"].width = 20
        ws.column_dimensions["D"].width = 10

        try:
            wb.save(ruta)
        except PermissionError:
            QMessageBox.critical(self, "Error",
                "El archivo está abierto en Excel. Ciérralo e intenta otra vez.")
            return
        QMessageBox.information(self, "Listo", f"Excel guardado en:\n{ruta}")

    def _importar_excel(self) -> None:
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Abrir Excel", "", "Archivo de Excel (*.xlsx)")
        if not ruta:
            return
        try:
            wb = load_workbook(ruta)
        except Exception:
            QMessageBox.critical(self, "Error", "No se pudo abrir el archivo")
            return
        ws = wb.active

        agregados = 0
        errores = []
        for num, fila in enumerate(
                ws.iter_rows(min_row=2, values_only=True), start=2):
            cod, nom, notas_raw = (list(fila) + [None, None, None])[:3]
            if cod is None and nom is None:
                continue                         # fila vacía
            try:
                cod = validar_codigo(cod)
                nom = str(nom or "").strip()
                if not nom:
                    raise ValueError("Nombre vacío")
                notas = validar_notas(notas_raw)
                if self._mod.buscar(cod) is not None:
                    raise ValueError(f"El código {cod} ya existe")
                self._mod.registrar(Estudiante(cod, nom, 0.0, notas))
                agregados += 1
            except ValueError as ex:
                errores.append(f"Fila {num}: {ex}")

        mensaje = f"Se importaron {agregados} estudiante(s)."
        if errores:
            mensaje += "\n\nNo se importaron:\n" + "\n".join(errores)
            self._lbl_error.setText(f"⚠ {len(errores)} fila(s) con error")
        else:
            self._lbl_error.setText("")
        QMessageBox.information(self, "Importar Excel", mensaje)

    # ── Slots (Observer) ─────────────────────────────
    def _on_estudiante_guardado(self, e) -> None:
        self._recargar_tabla()

    def _on_estudiante_eliminado(self, cod: int) -> None:
        self._recargar_tabla()

    # ── Tabla ────────────────────────────────────────
    def _recargar_tabla(self) -> None:
        self._llenar_tabla(self._mod.listar())

    def _llenar_tabla(self, estudiantes) -> None:
        self._tbl.setRowCount(0)
        for e in estudiantes:
            r = self._tbl.rowCount()
            self._tbl.insertRow(r)
            self._tbl.setItem(r, 0,
                QTableWidgetItem(f"{e.codigo:04d}"))
            self._tbl.setItem(r, 1,
                QTableWidgetItem(e.nombre))
            ppa_item = QTableWidgetItem(f"{e.ppa:.2f}")
            if e.ppa < 10.5:
                ppa_item.setForeground(QColor("#C00000"))   # desaprobado en rojo
            self._tbl.setItem(r, 2, ppa_item)
            notas_txt = ", ".join(f"{n:g}" for n in e.notas)
            self._tbl.setItem(r, 3,
                QTableWidgetItem(notas_txt))


if __name__ == "__main__":
    from servicios import ServicioEstudiante
    from estrategias import PromedioSimple
    from repositorios import RepositorioJSON
    app   = QApplication(sys.argv)
    svc   = ServicioEstudiante(
        RepositorioJSON("datos.json"), PromedioSimple())
    mod   = ModeloAcademico(svc)
    vista = VistaEstudiantes(mod)
    vista.show()
    sys.exit(app.exec_())