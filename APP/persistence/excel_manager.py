import openpyxl
import os

class ExcelManager:
    def __init__(self, archivo="data/registro.xlsx"):
        self.archivo = archivo
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.archivo):
            self._crear_archivo()

    def _crear_archivo(self):
        wb = openpyxl.Workbook()
        wb.remove(wb.active)
        wb.create_sheet("Estudiantes")
        wb.create_sheet("Materias")
        wb.create_sheet("Inscripciones")
        wb.save(self.archivo)

    def _abrir(self):
        return openpyxl.load_workbook(self.archivo)

    # === ESTUDIANTES ===
    def agregar_estudiante(self, data):
        wb = self._abrir()
        ws = wb["Estudiantes"]
        ws.append(data)
        wb.save(self.archivo)

    def obtener_estudiantes(self):
        wb = self._abrir()
        ws = wb["Estudiantes"]
        datos = []
        for row in ws.iter_rows(values_only=True):
            if row:
                datos.append({"Id": row[0], "Nombre": row[1], "Apellido": row[2], "Legajo": row[3]})
        return datos

    def modificar_estudiante(self, id_est, nombre, apellido, legajo):
        wb = self._abrir()
        ws = wb["Estudiantes"]
        for row in ws.iter_rows():
            if row[0].value == id_est:
                row[1].value = nombre
                row[2].value = apellido
                row[3].value = legajo
        wb.save(self.archivo)

    def eliminar_estudiante(self, id_est):
        wb = self._abrir()
        ws = wb["Estudiantes"]
        for row in ws.iter_rows():
            if row[0].value == id_est:
                ws.delete_rows(row[0].row)
        wb.save(self.archivo)

    # === MATERIAS ===
    def agregar_materia(self, data):
        wb = self._abrir()
        ws = wb["Materias"]
        ws.append(data)
        wb.save(self.archivo)

    def obtener_materias(self):
        wb = self._abrir()
        ws = wb["Materias"]
        datos = []
        for row in ws.iter_rows(values_only=True):
            if row:
                datos.append({"Id": row[0], "Nombre": row[1]})
        return datos

    def eliminar_materia(self, id_mat):
        wb = self._abrir()
        ws = wb["Materias"]
        for row in ws.iter_rows():
            if row[0].value == id_mat:
                ws.delete_rows(row[0].row)
        wb.save(self.archivo)

    # === INSCRIPCIONES ===
    def agregar_inscripcion(self, data):
        wb = self._abrir()
        ws = wb["Inscripciones"]
        ws.append(data)
        wb.save(self.archivo)

    def obtener_inscripciones(self):
        wb = self._abrir()
        ws = wb["Inscripciones"]
        datos = []
        for row in ws.iter_rows(values_only=True):
            if row:
                datos.append({"Id": row[0], "EstudianteId": row[1], "MateriaId": row[2], "Nota": float(row[3])})
        return datos

    def calcular_promedio(self, estudiante_id):
        inscripciones = self.obtener_inscripciones()
        notas = [ins["Nota"] for ins in inscripciones if ins["EstudianteId"] == estudiante_id]
        return sum(notas) / len(notas) if notas else 0.0
