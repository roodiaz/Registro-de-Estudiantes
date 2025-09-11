import csv
import os
import tkinter as tk
from tkinter import filedialog
from persistence.excel_manager import ExcelManager
from utils.helpers import pausar

class CSVExporter:
    def __init__(self):
        self.excel = ExcelManager()

    def _get_save_path(self, default_name):
        """Muestra un diálogo para seleccionar la ubicación de guardado."""
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal
        
        # Configurar el diálogo de guardado
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
            initialfile=default_name,
            title="Guardar archivo como"
        )
        
        return file_path

    def exportar_todo(self, output_path=None):
        """
        Exporta todos los datos a un archivo CSV.
        
        Args:
            output_path (str, optional): Ruta donde guardar el archivo. Si es None, se pedirá al usuario.
        """
        estudiantes = self.excel.obtener_estudiantes()
        inscripciones = self.excel.obtener_inscripciones()
        materias = self.excel.obtener_materias()
        
        # Si no se proporcionó una ruta, pedir al usuario que la seleccione
        if not output_path:
            output_path = self._get_save_path("exportacion_estudiantes.csv")
            if not output_path:  # El usuario canceló el diálogo
                print("\n❌ Exportación cancelada por el usuario.")
                pausar()
                return
        
        # Asegurarse de que el directorio de salida exista
        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
        
        # Crear un diccionario para búsqueda rápida de materias
        materias_dict = {m["Id"]: m for m in materias}
        
        # Contador para registros con problemas
        registros_problema = 0

        try:
            with open(output_path, "w", newline="", encoding="utf-8") as f:
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
                print(f"\n⚠️  Se encontraron {registros_problema} registros con problemas durante la exportación.")
            print(f"\n✅ Exportación completada correctamente en:\n{os.path.abspath(output_path)}")
            
        except Exception as e:
            print(f"\n❌ Error al guardar el archivo: {str(e)}")
        
        pausar()

    def exportar_estudiante(self, legajo, output_path=None):
        """
        Exporta los datos de un estudiante a un archivo CSV.
        
        Args:
            legajo (str): Número de legajo del estudiante a exportar
            output_path (str, optional): Ruta donde guardar el archivo. Si es None, se pedirá al usuario.
        """
        estudiantes = self.excel.obtener_estudiantes()
        estudiante = next((e for e in estudiantes if e["Legajo"] == legajo), None)
        if not estudiante:
            print("\n❌ Estudiante no encontrado.")
            pausar()
            return
            
        # Si no se proporcionó una ruta, pedir al usuario que la seleccione
        if not output_path:
            nombre_archivo = f"estudiante_{legajo}_inscripciones.csv"
            output_path = self._get_save_path(nombre_archivo)
            if not output_path:  # El usuario canceló el diálogo
                print("\n❌ Exportación cancelada por el usuario.")
                pausar()
                return

        inscripciones = self.excel.obtener_inscripciones()
        materias = self.excel.obtener_materias()
        
        # Crear un diccionario para búsqueda rápida de materias
        materias_dict = {m["Id"]: m for m in materias}
        
        # Asegurarse de que el directorio de salida exista
        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
        
        # Filtrar solo las inscripciones del estudiante
        inscripciones_est = [i for i in inscripciones if i["EstudianteId"] == estudiante["Id"]]
        
        if not inscripciones_est:
            print(f"\nℹ️  El estudiante {estudiante['Nombre']} {estudiante['Apellido']} no tiene inscripciones.")
            pausar()
            return
            
        # Calcular promedio
        promedio = self.excel.calcular_promedio(estudiante["Id"])
        
        try:
            # Exportar a CSV en la ubicación seleccionada
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Estudiante", "Legajo", "Materia", "Nota"])
                
                for ins in inscripciones_est:
                    mat = materias_dict.get(ins["MateriaId"])
                    if mat:
                        writer.writerow([
                            f"{estudiante['Nombre']} {estudiante['Apellido']}", 
                            estudiante["Legajo"], 
                            mat["Nombre"], 
                            ins["Nota"]
                        ])
                
                # Agregar el promedio al final
                writer.writerow(["", "", "Promedio:", f"{promedio:.2f}" if promedio is not None else "N/A"])
            
            print(f"\n✅ Datos del estudiante exportados correctamente a:\n{os.path.abspath(output_path)}")
            
        except Exception as e:
            print(f"\n❌ Error al exportar los datos del estudiante: {str(e)}")
            
        pausar()
