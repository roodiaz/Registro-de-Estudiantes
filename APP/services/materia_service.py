from persistence.excel_manager import ExcelManager
from utils.helpers import generar_id, pausar

class MateriaService:
    def __init__(self):
        self.excel = ExcelManager()

    def crear_materia(self):
        nombre = input("Nombre de la materia: ")
        nuevo_id = generar_id("Materias")
        self.excel.agregar_materia([nuevo_id, nombre])
        print("\n✅ Materia agregada con éxito.")
        pausar()

    def listar_materias(self):
        materias = self.excel.obtener_materias()
        if not materias:
            print("No hay materias registradas.")
            return
        for mat in materias:
            print(f"Materia: {mat['Nombre']}")
        pausar()

    def eliminar_materia(self):
        id_mat = input("Ingrese ID de la materia a eliminar: ")
        self.excel.eliminar_materia(id_mat)
        print("\n✅ Materia eliminada con éxito.")
        pausar()
