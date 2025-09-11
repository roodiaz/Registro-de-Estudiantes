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
        
    def _guardar(self, workbook):
        workbook.save(self.archivo)

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
        self._guardar(wb)

    def eliminar_estudiante(self, id_est):
        wb = self._abrir()
        ws = wb["Estudiantes"]
        for row in ws.iter_rows():
            if row[0].value == id_est:
                ws.delete_rows(row[0].row)
        self._guardar(wb)

    # === MATERIAS ===
    def agregar_materia(self, datos):
        wb = self._abrir()
        ws = wb["Materias"]
        
        # Verificar si ya existe una materia con el mismo código
        codigo = datos[1]  # El código está en la segunda posición
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row and str(row[1]).lower() == codigo.lower():
                raise ValueError(f"Ya existe una materia con el código: {codigo}")
                
        ws.append(datos)
        self._guardar(wb)

    def obtener_materias(self):
        wb = self._abrir()
        ws = wb["Materias"]
        datos = []
        for row in ws.iter_rows(values_only=True):
            if row:
                datos.append({
                    "Id": row[0],
                    "Codigo": row[1],
                    "Nombre": row[2]
                })
        return datos

    def obtener_materia_por_codigo(self, codigo):
        wb = self._abrir()
        ws = wb["Materias"]
        for row in ws.iter_rows(values_only=True):
            if row and str(row[1]).lower() == codigo.lower():
                return {
                    "Id": row[0],
                    "Codigo": row[1],
                    "Nombre": row[2]
                }
        return None

    def codigo_materia_existe(self, codigo):
        wb = self._abrir()
        ws = wb["Materias"]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row and str(row[1]).lower() == codigo.lower():
                return True
        return False

    def modificar_materia(self, codigo, nuevo_nombre):
        wb = self._abrir()
        ws = wb["Materias"]
        for row in ws.iter_rows(min_row=2):
            if str(row[1].value).lower() == codigo.lower():  # Buscar por código
                row[2].value = nuevo_nombre  # Actualizar nombre
                self._guardar(wb)
                return True
        return False

    def eliminar_materia(self, codigo):
        wb = self._abrir()
        ws = wb["Materias"]
        for idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
            if row[1].value and str(row[1].value).strip().lower() == codigo.lower():
                ws.delete_rows(idx)
                self._guardar(wb)
                return True
        return False

    # === INSCRIPCIONES ===
    def agregar_inscripcion(self, data):
        wb = self._abrir()
        ws = wb["Inscripciones"]
        ws.append(data)
        self._guardar(wb)
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
