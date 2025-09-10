from persistence.excel_manager import ExcelManager
from utils.helpers import generar_id, pausar

class InscripcionService:
    def __init__(self):
        self.excel = ExcelManager()

    def inscribir_estudiante(self):
        est_id = input("Ingrese ID del estudiante: ")
        mat_id = input("Ingrese ID de la materia: ")
        nota = float(input("Ingrese nota: "))
        nuevo_id = generar_id("Inscripciones")
        self.excel.agregar_inscripcion([nuevo_id, est_id, mat_id, nota])
        print("\n✅ Inscripción registrada con éxito.")
        pausar()

    def listar_inscripciones(self):
        inscripciones = self.excel.obtener_inscripciones()
        if not inscripciones:
            print("No hay inscripciones registradas.")
            pausar()
            return

        estudiantes = self.excel.obtener_estudiantes()
        materias = self.excel.obtener_materias()

        for ins in inscripciones:
            est = next((e for e in estudiantes if e["Id"] == ins["EstudianteId"]), None)
            mat = next((m for m in materias if m["Id"] == ins["MateriaId"]), None)
            if est and mat:
                print(f"{est['Nombre']} {est['Apellido']} | Materia: {mat['Nombre']} | Nota: {ins['Nota']}")
        pausar()