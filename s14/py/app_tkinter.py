# app_tkinter.py — versión completa
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from servicios import ServicioEstudiante
from estrategias import PromedioSimple
from repositorios import RepositorioJSON
from estudiante import Estudiante


class AppEstudiantes(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("SIS206 — Sistema Académico UNAP")
        self.geometry("800x500")
        self.resizable(True, True)

        # Modelo (Servicio)
        self._svc = ServicioEstudiante(
            RepositorioJSON("datos.json"),
            PromedioSimple())

        self._construir_ui()
        self._actualizar_lista()

    # ── UI ───────────────────────────────────
    def _construir_ui(self) -> None:
        # Barra de entrada
        frm_top = ttk.LabelFrame(self,
            text="Registrar Estudiante", padding=8)
        frm_top.pack(fill="x", padx=8, pady=4)

        ttk.Label(frm_top, text="Código:").grid(
            row=0, column=0, sticky="e")
        self._ent_cod = ttk.Entry(frm_top, width=8)
        self._ent_cod.grid(row=0, column=1, padx=4)

        ttk.Label(frm_top, text="Nombre:").grid(
            row=0, column=2, sticky="e")
        self._ent_nom = ttk.Entry(frm_top, width=28)
        self._ent_nom.grid(row=0, column=3, padx=4)

        ttk.Label(frm_top, text="Notas (,):").grid(
            row=0, column=4, sticky="e")
        self._ent_notas = ttk.Entry(frm_top, width=18)
        self._ent_notas.grid(row=0, column=5, padx=4)

        ttk.Button(frm_top, text="Registrar",
            command=self._registrar).grid(
            row=0, column=6, padx=8)
        ttk.Button(frm_top, text="Eliminar",
            command=self._eliminar).grid(
            row=0, column=7, padx=4)

        # Búsqueda por código (fila 2)
        ttk.Label(frm_top, text="Buscar cód.:").grid(
            row=1, column=0, sticky="e", pady=(8, 0))
        self._ent_buscar = ttk.Entry(frm_top, width=8)
        self._ent_buscar.grid(row=1, column=1, padx=4, pady=(8, 0))
        ttk.Button(frm_top, text="Buscar",
            command=self._buscar).grid(
            row=1, column=2, padx=4, pady=(8, 0))
        ttk.Button(frm_top, text="Mostrar todos",
            command=self._actualizar_lista).grid(
            row=1, column=3, sticky="w", padx=4, pady=(8, 0))
        ttk.Button(frm_top, text="Exportar Excel",
            command=self._exportar_excel).grid(
            row=1, column=4, columnspan=2, sticky="w", padx=4, pady=(8, 0))
        ttk.Button(frm_top, text="Importar Excel",          # ← NUEVO
            command=self._importar_excel).grid(
            row=1, column=6, columnspan=2, sticky="w", padx=4, pady=(8, 0))

        # Mensaje de error en rojo (fila 3)
        self._lbl_error = tk.Label(frm_top, text="",
            fg="red", font=("Segoe UI", 10, "bold"))
        self._lbl_error.grid(row=2, column=0, columnspan=8,
            sticky="w", pady=(6, 0))

        # Lista de estudiantes
        frm_bot = ttk.LabelFrame(self,
            text="Estudiantes", padding=4)
        frm_bot.pack(fill="both",
            expand=True, padx=8, pady=4)

        self._lb = tk.Listbox(frm_bot,
            font=("Courier New", 11),
            selectmode=tk.SINGLE)
        sb = ttk.Scrollbar(frm_bot,
            orient="vertical",
            command=self._lb.yview)
        self._lb.configure(
            yscrollcommand=sb.set)
        self._lb.pack(side="left", fill="both",
            expand=True)
        sb.pack(side="right", fill="y")

    # ── Handlers (Controlador) ───────────
    def _registrar(self) -> None:
        self._lbl_error.config(text="")            # limpia el error anterior
        try:
            txt_cod = self._ent_cod.get().strip()
            if not txt_cod.isdigit():
                raise ValueError("El código debe ser un número")
            if len(txt_cod) > 4:
                raise ValueError("El código debe tener máximo 4 dígitos")
            cod = int(txt_cod)
            nom = self._ent_nom.get().strip()
            if not nom:
                raise ValueError("Nombre vacío")
            raw = self._ent_notas.get().strip()
            notas = [float(x) for x in
                raw.split(",") if x.strip()] if raw else []

            # ── Validar rango de notas 0 a 20 ──
            fuera = [n for n in notas if n < 0 or n > 20]
            if fuera:
                malas = ", ".join(f"{n:g}" for n in fuera)
                raise ValueError(
                    f"Nota(s) fuera de rango: {malas}. "
                    "Solo se permiten notas de 0 a 20")

            e = Estudiante(cod, nom, 0.0, notas)
            self._svc.registrar(e)
            self._actualizar_lista()
            self._ent_cod.delete(0, "end")
            self._ent_nom.delete(0, "end")
            self._ent_notas.delete(0, "end")
        except ValueError as ex:
            self._lbl_error.config(text=f"⚠ {ex}")   # mensaje en rojo
            messagebox.showerror("Error", str(ex))

    def _eliminar(self) -> None:
        sel = self._lb.curselection()
        if not sel:
            messagebox.showwarning(
                "Aviso", "Seleccione un estudiante")
            return
        texto = self._lb.get(sel[0])
        if not texto.startswith("["):
            return  # ej: "No se encontró el estudiante"
        cod = int(texto[1:texto.index("]")])
        self._svc.eliminar(cod)
        self._actualizar_lista()

    def _buscar(self) -> None:
        texto = self._ent_buscar.get().strip()
        if not texto.isdigit():
            messagebox.showwarning(
                "Aviso", "Escriba un código numérico")
            return
        e = self._svc.buscar(int(texto))
        self._lb.delete(0, "end")
        if e is None:
            self._lb.insert("end", "No se encontró el estudiante")
        else:
            ppa_str = f"{e.ppa:.2f}" if e.notas else "sin notas"
            self._lb.insert("end",
                f"[{e.codigo:04d}]  {e.nombre:<28}"
                f"  PPA: {ppa_str}")

    def _exportar_excel(self) -> None:
        estudiantes = self._svc.listar()
        if not estudiantes:
            messagebox.showwarning("Aviso", "No hay estudiantes para exportar")
            return

        # 1. Preguntar dónde guardar
        ruta = filedialog.asksaveasfilename(
            title="Guardar como",
            defaultextension=".xlsx",
            initialfile="estudiantes.xlsx",
            filetypes=[("Archivo de Excel", "*.xlsx")])
        if not ruta:
            return

        # 2. Crear el Excel y el encabezado
        wb = Workbook()
        ws = wb.active
        ws.title = "Estudiantes"
        ws.append(["Código", "Nombre", "Notas", "PPA"])
        for celda in ws[1]:
            celda.font = Font(bold=True, color="FFFFFF")
            celda.fill = PatternFill("solid", fgColor="5B2C83")

        # 3. Una fila por cada estudiante
        for e in estudiantes:
            notas = ", ".join(f"{n:g}" for n in e.notas)
            ws.append([e.codigo, e.nombre, notas, round(e.ppa, 2)])
            fila = ws.max_row
            ws.cell(fila, 1).number_format = "0000"
            ws.cell(fila, 4).number_format = "0.00"

        # 4. Ancho de columnas
        ws.column_dimensions["A"].width = 10
        ws.column_dimensions["B"].width = 30
        ws.column_dimensions["C"].width = 20
        ws.column_dimensions["D"].width = 10

        # 5. Guardar
        try:
            wb.save(ruta)
        except PermissionError:
            messagebox.showerror("Error",
                "El archivo está abierto en Excel. Ciérralo e intenta otra vez.")
            return
        messagebox.showinfo("Listo", f"Excel guardado en:\n{ruta}")

    def _importar_excel(self) -> None:                     # ← NUEVO
        # 1. Elegir el archivo
        ruta = filedialog.askopenfilename(
            title="Abrir Excel",
            filetypes=[("Archivo de Excel", "*.xlsx")])
        if not ruta:
            return

        try:
            wb = load_workbook(ruta)
        except Exception:
            messagebox.showerror("Error", "No se pudo abrir el archivo")
            return
        ws = wb.active

        agregados = 0
        errores = []

        # 2. Leer fila por fila (desde la fila 2, la 1 es el encabezado)
        for num, fila in enumerate(
                ws.iter_rows(min_row=2, values_only=True), start=2):
            cod, nom, notas_raw = (list(fila) + [None, None, None])[:3]
            if cod is None and nom is None:
                continue                       # fila vacía

            try:
                # Código: número de máximo 4 dígitos
                txt_cod = str(cod).strip()
                if txt_cod.endswith(".0"):
                    txt_cod = txt_cod[:-2]
                if not txt_cod.isdigit() or len(txt_cod) > 4:
                    raise ValueError("código inválido")
                cod = int(txt_cod)

                # Nombre
                nom = str(nom or "").strip()
                if not nom:
                    raise ValueError("nombre vacío")

                # Notas: "15, 18, 14" o un solo número
                txt = str(notas_raw or "").strip()
                notas = [float(x) for x in txt.split(",") if x.strip()]
                if any(n < 0 or n > 20 for n in notas):
                    raise ValueError("nota fuera de 0 a 20")

                # No repetir códigos
                if self._svc.buscar(cod) is not None:
                    raise ValueError(f"el código {cod} ya existe")

                self._svc.registrar(Estudiante(cod, nom, 0.0, notas))
                agregados += 1
            except ValueError as ex:
                errores.append(f"Fila {num}: {ex}")

        # 3. Actualizar el cuadro y avisar
        self._actualizar_lista()
        mensaje = f"Se importaron {agregados} estudiante(s)."
        if errores:
            mensaje += "\n\nNo se importaron:\n" + "\n".join(errores)
            self._lbl_error.config(text=f"⚠ {len(errores)} fila(s) con error")
        else:
            self._lbl_error.config(text="")
        messagebox.showinfo("Importar Excel", mensaje)

    def _actualizar_lista(self) -> None:
        self._lb.delete(0, "end")
        for e in self._svc.listar():
            ppa_str = f"{e.ppa:.2f}" if e.notas else "sin notas"
            self._lb.insert("end",
                f"[{e.codigo:04d}]  {e.nombre:<28}"
                f"  PPA: {ppa_str}")


if __name__ == "__main__":
    AppEstudiantes().mainloop()