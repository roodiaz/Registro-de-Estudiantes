import csv
from persistence.excel_manager import ExcelManager
import os

class CSVExporter:
    def __init__(self):
        self.excel = ExcelManager()
        if not os.path.exists("data/exportados"):
            os.makedirs("data/exportados")

    def exportar_todo(self):
        estudiantes = self.excel.obtener_estudiantes()
        inscripciones = self.excel.obtener_inscripciones()
        materias = self.excel.obtener_materias()

        with open("data/exportados/todo.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Estudiante", "Legajo", "Materia", "Nota", "Promedio"])
            for est in estudiantes:
                promedio = self.excel.calcular_promedio(est["Id"])
                inscripciones_est = [i for i in inscripciones if i["EstudianteId"] == est["Id"]]
                for ins in inscripciones_est:
                    mat = next((m for m in materias if m["Id"] == ins["MateriaId"]), None)
                    writer.writerow([f"{est['Nombre']} {est['Apellido']}", est["Legajo"], mat["Nombre"], ins["Nota"], promedio])
        print("✅ Exportación completa en data/exportados/todo.csv")

    def exportar_estudiante(self, legajo):
        estudiantes = self.excel.obtener_estudiantes()
        estudiante = next((e for e in estudiantes if e["Legajo"] == legajo), None)
        if not estudiante:
            print("❌ Estudiante no encontrado.")
            return

        inscripciones = self.excel.obtener_inscripciones()
        materias = self.excel.obtener_materias()
        promedio = self.excel.calcular_promedio(estudiante["Id"])

        filename = f"data/exportados/{estudiante['Legajo']}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Estudiante", "Legajo", "Materia", "Nota", "Promedio"])
            for ins in inscripciones:
                if ins["EstudianteId"] == estudiante["Id"]:
                    mat = next((m for m in materias if m["Id"] == ins["MateriaId"]), None)
                    writer.writerow([f"{estudiante['Nombre']} {estudiante['Apellido']}", estudiante["Legajo"], mat["Nombre"], ins["Nota"], promedio])
        print(f"✅ Exportación completa en {filename}")
