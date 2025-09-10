from persistence.excel_manager import ExcelManager
from utils.helpers import generar_id, pausar, limpiar_pantalla
from utils.input_utils import confirmar_salida
from utils.table_utils import print_table

class MateriaService:
    def __init__(self):
        self.excel = ExcelManager()

    def crear_materia(self):
        print("\nALTA DE MATERIA (deje en blanco y presione Enter en cualquier momento para cancelar)\n")
        
        # Solicitar código de materia
        while True:
            codigo = input("Código de la materia (ej: MAT101): ").strip().upper()
            if not codigo:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                print("Error: El código de la materia no puede estar vacío.")
                continue
                
            # Verificar si ya existe una materia con el mismo código
            if self.excel.codigo_materia_existe(codigo):
                print(f"Error: Ya existe una materia con el código {codigo}.")
                if confirmar_salida("¿Desea intentar con otro código? (s/n): "):
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            break
            
        # Solicitar nombre de la materia
        while True:
            nombre = input("Nombre de la materia: ").strip()
            if not nombre:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                print("Error: El nombre de la materia no puede estar vacío.")
                continue
                
            # Verificar si ya existe una materia con el mismo nombre (case-insensitive)
            materias = self.excel.obtener_materias()
            if any(m['Nombre'].lower() == nombre.lower() for m in materias):
                print("Error: Ya existe una materia con ese nombre.")
                if confirmar_salida("¿Desea intentar con otro nombre? (s/n): "):
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            break
            
        try:
            nuevo_id = generar_id("Materias")
            self.excel.agregar_materia([nuevo_id, codigo, nombre])
            print("\n✅ Materia agregada con éxito.")
        except Exception as e:
            print(f"\n❌ Error al agregar la materia: {str(e)}")
            
        pausar()

    def modificar_materia(self):
        print("\nMODIFICAR MATERIA (deje en blanco y presione Enter en cualquier momento para cancelar)\n")
        
        materias = self.excel.obtener_materias()
        if not materias:
            print("No hay materias registradas.")
            pausar()
            return
        
        # Obtener conteo de inscripciones por materia
        inscripciones = self.excel.obtener_inscripciones()
        contador_inscripciones = {}
        for ins in inscripciones:
            contador_inscripciones[ins["MateriaId"]] = contador_inscripciones.get(ins["MateriaId"], 0) + 1
        
        # Preparar datos para la tabla
        materias_data = []
        for mat in materias:
            num_inscripciones = contador_inscripciones.get(mat["Id"], 0)
            materias_data.append({
                'codigo': mat['Codigo'],
                'nombre': mat['Nombre'],
                'inscripciones': str(num_inscripciones)
            })
        
        # Mostrar tabla
        print_table(
            headers=['Código', 'Nombre', 'Estudiantes Inscriptos'],
            rows=materias_data,
            column_widths={
                'codigo': 15,
                'nombre': 40,
                'inscripciones': 20
            },
            title="LISTADO DE MATERIAS",
            footer=f"Total de materias: {len(materias_data)}"
        )
        pausar()

    def eliminar_materia(self):
        print("\nELIMINAR MATERIA (deje en blanco y presione Enter en cualquier momento para cancelar)\n")
        
        materias = self.excel.obtener_materias()
        if not materias:
            print("No hay materias registradas para eliminar.")
            pausar()
            return
            
        # Mostrar materias disponibles en tabla
        print("Materias disponibles:")
        
        # Preparar datos para la tabla
        materias_data = []
        for mat in materias:
            inscripciones = self.excel.obtener_inscripciones()
            num_inscripciones = sum(1 for ins in inscripciones if ins["MateriaId"] == mat["Id"])
            materias_data.append({
                'codigo': mat['Codigo'],
                'nombre': mat['Nombre'],
                'inscripciones': str(num_inscripciones)
            })
        
        # Mostrar tabla
        print_table(
            headers=['Código', 'Nombre', 'Estudiantes Inscriptos'],
            rows=materias_data,
            column_widths={'codigo': 15, 'nombre': 40, 'inscripciones': 20}
        )
            
        while True:
            codigo = input("\nIngrese el CÓDIGO de la materia a eliminar (o presione Enter para cancelar): ").strip().upper()
            if not codigo:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            # Verificar si la materia existe
            materia = self.excel.obtener_materia_por_codigo(codigo)
            if not materia:
                print("Error: No se encontró una materia con ese código. Intente nuevamente.")
                continue
                
            # Verificar si hay inscripciones para esta materia
            inscripciones = self.excel.obtener_inscripciones()
            tiene_inscripciones = any(ins["MateriaId"] == materia["Id"] for ins in inscripciones)
            
            if tiene_inscripciones:
                num_inscripciones = sum(1 for ins in inscripciones if ins["MateriaId"] == materia["Id"])
                print(f"\n⚠️  No se puede eliminar la materia '{materia['Nombre']}' porque tiene {num_inscripciones} estudiante(s) inscripto(s).")
                print("Por favor, elimine primero las inscripciones asociadas.")
                pausar()
                return
                
            confirmacion = input(f"\n⚠️  ¿Está seguro que desea eliminar la materia '{materia['Nombre']}' (Código: {materia['Codigo']})? Esta acción no se puede deshacer. (s/n): ")
            if confirmacion.lower() == 's':
                if self.excel.eliminar_materia(codigo):
                    print("\n✅ Materia eliminada con éxito.")
                else:
                    print("\n❌ Error al eliminar la materia.")
            else:
                print("\nOperación cancelada.")
            
            break
                
        pausar()
