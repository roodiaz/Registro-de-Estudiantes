from persistence.excel_manager import ExcelManager
from utils.helpers import generar_id, pausar, limpiar_pantalla
from utils.validators import validar_legajo, legajo_existe
from utils.input_utils import confirmar_salida
from utils.table_utils import print_table

class EstudianteService:
    def __init__(self):
        self.excel = ExcelManager()

    def crear_estudiante(self):
        print("\nALTA DE ESTUDIANTE (deje en blanco y presione Enter en cualquier momento para cancelar)\n")
        
        # Solicitar nombre
        while True:
            nombre = input("Nombre: ").strip()
            if not nombre:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
            break
                
        # Solicitar apellido
        while True:
            apellido = input("Apellido: ").strip()
            if not apellido:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                print("Error: El apellido no puede estar vacío.")
                continue
            break
                
        # Solicitar legajo
        while True:
            legajo = input("Legajo (5-10 caracteres alfanuméricos): ").strip()
            if not legajo:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                print("Error: El legajo no puede estar vacío.")
                continue
                
            if not validar_legajo(legajo):
                print("Error: El legajo debe ser alfanumérico y tener entre 5 y 10 caracteres.")
                continue
                
            if legajo_existe(self.excel, legajo):
                print("Error: Ya existe un estudiante con este legajo.")
                if confirmar_salida("¿Desea intentar con otro legajo? (s/n): "):
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            break
            
        nuevo_id = generar_id("Estudiantes")
        self.excel.agregar_estudiante([nuevo_id, nombre, apellido, legajo])
        print("\n✅ Estudiante agregado con éxito.")
        pausar()

    def listar_estudiantes(self):
        estudiantes = self.excel.obtener_estudiantes()
        inscripciones = self.excel.obtener_inscripciones()
        materias = self.excel.obtener_materias()
        
        # Crear diccionario de materias para búsqueda rápida
        materias_dict = {m['Id']: m for m in materias}
        
        # Preparar datos para la tabla
        estudiantes_data = []
        for est in estudiantes:
            # Obtener materias del estudiante
            materias_estudiante = []
            estudiante_id = str(est['Id'])
            
            for ins in inscripciones:
                # Asegurarse de que ambos IDs sean cadenas para la comparación
                if str(ins['EstudianteId']) == estudiante_id:
                    if str(ins['MateriaId']) in materias_dict:
                        materias_estudiante.append(materias_dict[str(ins['MateriaId'])]['Nombre'])
            
            promedio = self.excel.calcular_promedio(est["Id"])
            estudiantes_data.append({
                'legajo': est['Legajo'],
                'nombre': est['Nombre'],
                'apellido': est['Apellido'],
                'materias inscriptas': '\n'.join(materias_estudiante) if materias_estudiante else 'Ninguna',
                'cant. materias': str(len(materias_estudiante)),
                'promedio': f"{promedio:.2f}" if promedio is not None else "N/A"
            })
        
        # Mostrar tabla
        print_table(
            headers=['legajo', 'nombre', 'apellido', 'materias inscriptas', 'cant. materias', 'promedio'],
            rows=estudiantes_data,
            column_widths={
                'legajo': 15,
                'nombre': 20,
                'apellido': 20,
                'materias inscriptas': 40,
                'cant. materias': 15,
                'promedio': 10
            },
            title="LISTADO DE ESTUDIANTES",
            footer=f"Total de estudiantes: {len(estudiantes_data)}"
        )
        pausar()

    def modificar_estudiante(self):
        print("\nMODIFICAR ESTUDIANTE (deje en blanco y presione Enter en cualquier momento para cancelar)\n")
        
        estudiantes = self.excel.obtener_estudiantes()
        if not estudiantes:
            print("No hay estudiantes registrados para modificar.")
            pausar()
            return
            
        # Mostrar estudiantes en tabla
        estudiantes_data = []
        for est in estudiantes:
            estudiantes_data.append({
                'legajo': est['Legajo'],
                'nombre': est['Nombre'],
                'apellido': est['Apellido']
            })
        
        # Mostrar tabla de estudiantes
        print_table(
            headers=['Legajo', 'Nombre', 'Apellido'],
            rows=estudiantes_data,
            column_widths={
                'legajo': 15, 
                'nombre': 25, 
                'apellido': 25
            },
            title="LISTA DE ESTUDIANTES"
        )
            
        while True:
            legajo = input("\nIngrese el LEGAJO del estudiante a modificar (o presione Enter para cancelar): ").strip()
            if not legajo:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            estudiante = next((e for e in estudiantes if e["Legajo"].lower() == legajo.lower()), None)
            if estudiante:
                break
                
            print("Error: No se encontró un estudiante con ese legajo. Intente nuevamente o presione Enter para cancelar.")
            
        # Modificar nombre
        while True:
            nuevo_nombre = input(f"\nNuevo nombre [{estudiante['Nombre']}]: ").strip()
            if not nuevo_nombre:
                if confirmar_salida("¿Desea mantener el nombre actual? (s/n): "):
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
            break
            
        nombre = nuevo_nombre if nuevo_nombre else estudiante['Nombre']
            
        # Modificar apellido
        while True:
            nuevo_apellido = input(f"\nNuevo apellido [{estudiante['Apellido']}]: ").strip()
            if not nuevo_apellido:
                if confirmar_salida("¿Desea mantener el apellido actual? (s/n): "):
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
            break
            
        apellido = nuevo_apellido if nuevo_apellido else estudiante['Apellido']
            
        # Modificar legajo
        while True:
            nuevo_legajo = input(f"\nNuevo legajo (5-10 caracteres alfanuméricos) [{estudiante['Legajo']}]: ").strip()
            if not nuevo_legajo:
                if confirmar_salida("¿Desea mantener el legajo actual? (s/n): "):
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            if not validar_legajo(nuevo_legajo):
                print("Error: El legajo debe ser alfanumérico y tener entre 5 y 10 caracteres.")
                if confirmar_salida("¿Desea intentar con otro legajo? (s/n): "):
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            if nuevo_legajo != estudiante['Legajo'] and legajo_existe(self.excel, nuevo_legajo):
                print("Error: Ya existe otro estudiante con este legajo.")
                if confirmar_salida("¿Desea intentar con otro legajo? (s/n): "):
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            legajo = nuevo_legajo
            break
            
        # Get the student ID from the original student data
        estudiante_actual = next((e for e in self.excel.obtener_estudiantes() if e['Legajo'] == legajo), None)
        if estudiante_actual:
            self.excel.modificar_estudiante(estudiante_actual['Id'], nombre, apellido, legajo)
            print("\n✅ Estudiante modificado con éxito.")
        else:
            print("\n❌ Error: No se pudo encontrar el estudiante para modificar.")
        pausar()

    def eliminar_estudiante(self):
        print("\nELIMINAR ESTUDIANTE (deje en blanco y presione Enter para cancelar)\n")
        
        estudiantes = self.excel.obtener_estudiantes()
        if not estudiantes:
            print("No hay estudiantes registrados para eliminar.")
            pausar()
            return
            
        # Mostrar estudiantes en tabla
        estudiantes_data = []
        for est in estudiantes:            
            estudiantes_data.append({
                'legajo': est['Legajo'],
                'nombre': est['Nombre'],
                'apellido': est['Apellido'],
            })
        
        # Mostrar tabla de estudiantes
        print_table(
            headers=['Legajo', 'Nombre', 'Apellido'],
            rows=estudiantes_data,
            column_widths={
                'legajo': 15, 
                'nombre': 20, 
                'apellido': 20, 
            },
            title="LISTA DE ESTUDIANTES"
        )
            
        while True:
            legajo = input("\nIngrese el LEGAJO del estudiante a eliminar (o presione Enter para cancelar): ").strip()
            if not legajo:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            estudiante = next((e for e in estudiantes if e["Legajo"].lower() == legajo.lower()), None)
            if estudiante:
                break
                
            print("Error: No se encontró un estudiante con ese legajo. Intente nuevamente o presione Enter para cancelar.")
        
        # Verificar si el estudiante tiene inscripciones
        inscripciones = self.excel.obtener_inscripciones()
        tiene_inscripciones = any(ins["EstudianteId"] == estudiante["Id"] for ins in inscripciones)
        
        if tiene_inscripciones:
            num_inscripciones = sum(1 for ins in inscripciones if ins["EstudianteId"] == estudiante["Id"])
            print(f"\n⚠️  No se puede eliminar el estudiante {estudiante['Nombre']} {estudiante['Apellido']}")
            print(f"porque tiene {num_inscripciones} inscripción(es) activa(s).")
            print("Por favor, elimine primero las inscripciones del estudiante.")
        else:
            confirmacion = input(f"\n⚠️  ¿Está seguro que desea eliminar a {estudiante['Nombre']} {estudiante['Apellido']} "
                               f"(Legajo: {estudiante['Legajo']})? Esta acción no se puede deshacer. (s/n): ")
            if confirmacion.lower() == 's':
                self.excel.eliminar_estudiante(estudiante["Id"])
                print("\n✅ Estudiante eliminado con éxito.")
            else:
                print("\nOperación cancelada.")
                
        pausar()
