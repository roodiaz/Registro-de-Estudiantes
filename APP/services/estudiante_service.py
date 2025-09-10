from persistence.excel_manager import ExcelManager
from utils.helpers import generar_id, pausar

class EstudianteService:
    def __init__(self):
        self.excel = ExcelManager()

    def crear_estudiante(self):
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        legajo = input("Legajo: ")
        nuevo_id = generar_id("Estudiantes")
        self.excel.agregar_estudiante([nuevo_id, nombre, apellido, legajo])
        print("\n✅ Estudiante agregado con éxito.")
        pausar()

    def listar_estudiantes(self):
        estudiantes = self.excel.obtener_estudiantes()
        if not estudiantes:
            print("No hay estudiantes registrados.")
        else:
            for est in estudiantes:
                promedio = self.excel.calcular_promedio(est["Id"])
                print(f"{est['Nombre']} {est['Apellido']} | Legajo: {est['Legajo']} | Promedio: {promedio:.2f}")
        pausar()

    def modificar_estudiante(self):
        id_est = input("Ingrese ID del estudiante a modificar: ")
        nombre = input("Nuevo nombre: ")
        apellido = input("Nuevo apellido: ")
        legajo = input("Nuevo legajo: ")
        self.excel.modificar_estudiante(id_est, nombre, apellido, legajo)
        print("\n✅ Estudiante modificado con éxito.")
        pausar()

    def eliminar_estudiante(self):
        id_est = input("Ingrese ID del estudiante a eliminar: ")
        self.excel.eliminar_estudiante(id_est)
        print("\n✅ Estudiante eliminado con éxito.")
        pausar()
