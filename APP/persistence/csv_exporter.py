import csv
from persistence.excel_manager import ExcelManager
import os
from utils.helpers import pausar

class CSVExporter:
    def __init__(self):
        self.excel = ExcelManager()
        if not os.path.exists("data/exportados"):
            os.makedirs("data/exportados")

    def exportar_todo(self):
        estudiantes = self.excel.obtener_estudiantes()
        inscripciones = self.excel.obtener_inscripciones()
        materias = self.excel.obtener_materias()
        
        # Crear un diccionario para búsqueda rápida de materias
        materias_dict = {m["Id"]: m for m in materias}
        
        # Contador para registros con problemas
        registros_problema = 0

        with open("data/exportados/todo.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Estudiante", "Legajo", "Materia", "Nota", "Promedio"])
            
            for est in estudiantes:
                try:
                    promedio = self.excel.calcular_promedio(est["Id"])
                    inscripciones_est = [i for i in inscripciones if i["EstudianteId"] == est["Id"]]
                    
                    for ins in inscripciones_est:
                        mat = materias_dict.get(ins["MateriaId"])
                        if mat:
                            writer.writerow([
                                f"{est['Nombre']} {est['Apellido']}", 
                                est["Legajo"], 
                                mat["Nombre"], 
                                ins["Nota"], 
                                f"{promedio:.2f}" if promedio is not None else "N/A"
                            ])
                        else:
                            registros_problema += 1
                            print(f"⚠️  Advertencia: No se encontró la materia con ID {ins['MateriaId']} para el estudiante {est['Nombre']} {est['Apellido']}")
                except Exception as e:
                    registros_problema += 1
                    print(f"⚠️  Error al procesar el estudiante {est['Nombre']} {est['Apellido']}: {str(e)}")
        
        if registros_problema > 0:
            print(f"⚠️  Se encontraron {registros_problema} registros con problemas durante la exportación.")
        print("\n✅ Exportación completa en data/exportados/todo.csv")
        pausar()

    def exportar_estudiante(self, legajo):
        estudiantes = self.excel.obtener_estudiantes()
        estudiante = next((e for e in estudiantes if e["Legajo"] == legajo), None)
        if not estudiante:
            print("\n❌ Estudiante no encontrado.")
            pausar()
            return

        inscripciones = self.excel.obtener_inscripciones()
        materias = self.excel.obtener_materias()
        
        # Crear un diccionario para búsqueda rápida de materias
        materias_dict = {m["Id"]: m for m in materias}
        
        # Filtrar solo las inscripciones del estudiante
        inscripciones_est = [i for i in inscripciones if i["EstudianteId"] == estudiante["Id"]]
        
        if not inscripciones_est:
            print("\n❌ El estudiante {estudiante['Nombre']} {estudiante['Apellido']} no tiene inscripciones.")
            pausar()
            return
        
        try:
            promedio = self.excel.calcular_promedio(estudiante["Id"])
            filename = f"data/exportados/{estudiante['Legajo']}_{estudiante['Apellido']}.csv"
            registros_problema = 0
            
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Estudiante", "Legajo", "Materia", "Nota", "Promedio"])
                
                for ins in inscripciones_est:
                    mat = materias_dict.get(ins["MateriaId"])
                    if mat:
                        writer.writerow([
                            f"{estudiante['Nombre']} {estudiante['Apellido']}",
                            estudiante["Legajo"],
                            mat["Nombre"],
                            ins["Nota"],
                            f"{promedio:.2f}" if promedio is not None else "N/A"
                        ])
                    else:
                        registros_problema += 1
                        print(f"⚠️  Advertencia: No se encontró la materia con ID {ins['MateriaId']}")
            
            if registros_problema > 0:
                print("\n⚠️  Se encontraron {registros_problema} registros con problemas durante la exportación.")
            else:
                print("\n✅ Exportación completa en {filename}")
                
        except Exception as e:
            print("\n❌ Error al exportar los datos del estudiante: {str(e)}")
        print("\n✅ Exportación completa en {filename}")
        pausar()
