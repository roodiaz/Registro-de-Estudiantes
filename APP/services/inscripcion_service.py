from persistence.excel_manager import ExcelManager
from utils.helpers import generar_id, pausar, limpiar_pantalla
from utils.validators import validar_nota
from utils.input_utils import confirmar_salida
from utils.table_utils import print_table

class InscripcionService:
    def __init__(self):
        self.excel = ExcelManager()

    def mostrar_estudiantes(self):
        """Muestra la lista de estudiantes en formato de tabla."""
        estudiantes = self.excel.obtener_estudiantes()
        if not estudiantes:
            print("\n❌ No hay estudiantes registrados.")
            return False
            
        print("\nListado de estudiantes:")
        print("-" * 60)
        print(f"{'Legajo':<10} | {'Apellido':<20} | {'Nombre':<20}")
        print("-" * 60)
        for est in sorted(estudiantes, key=lambda x: (x['Apellido'], x['Nombre'])):
            print(f"{est['Legajo']:<10} | {est['Apellido']:<20} | {est['Nombre']:<20}")
        print("-" * 60)
        return True

    def inscribir_estudiante(self):
        print("\nINSCRIPCIÓN DE ESTUDIANTE (deje en blanco y presione Enter en cualquier momento para cancelar)\n")
        
        # Obtener estudiantes y materias para validación
        estudiantes = self.excel.obtener_estudiantes()
        materias = self.excel.obtener_materias()
        
        if not estudiantes:
            print("Error: No hay estudiantes registrados. Por favor, registre un estudiante primero.")
            pausar()
            return
            
        if not materias:
            print("Error: No hay materias registradas. Por favor, registre una materia primero.")
            pausar()
            return
        
        # Mostrar estudiantes disponibles en tabla
        print("Estudiantes disponibles:")
        
        # Preparar datos para la tabla
        estudiantes_data = []
        for est in estudiantes:
            # Contar materias en las que está inscripto
            inscripciones = self.excel.obtener_inscripciones()
            materias_inscriptas = sum(1 for ins in inscripciones if ins["EstudianteId"] == est["Id"])
            
            estudiantes_data.append({
                'legajo': est['Legajo'],
                'nombre': est['Nombre'],
                'apellido': est['Apellido'],
                'materias': str(materias_inscriptas)
            })
        
        # Mostrar tabla
        print_table(
            headers=['Legajo', 'Nombre', 'Apellido', 'Materias Inscriptas'],
            rows=estudiantes_data,
            column_widths={
                'legajo': 15, 
                'nombre': 20, 
                'apellido': 20, 
                'materias': 10
            }
        )
        
        # Validar estudiante
        while True:
            legajo = input("\nIngrese LEGAJO del estudiante (o presione Enter para cancelar): ").strip()
            if not legajo:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            estudiante = next((e for e in estudiantes if e["Legajo"] == legajo), None)
            if estudiante:
                break
                
            print("Error: LEGAJO de estudiante no válido. Intente nuevamente o presione Enter para cancelar.")
        
        # Obtener materias en las que ya está inscripto el estudiante
        inscripciones = self.excel.obtener_inscripciones()
        materias_inscriptas = set(
            ins["MateriaId"] 
            for ins in inscripciones 
            if ins["EstudianteId"] == estudiante["Id"]
        )
        
        # Filtrar materias disponibles (excluyendo las ya inscriptas)
        materias_disponibles = [m for m in materias if m["Id"] not in materias_inscriptas]
        
        if not materias_disponibles:
            print("\n⚠️  El estudiante ya está inscripto en todas las materias disponibles.")
            pausar()
            return
            
        # Mostrar materias disponibles en tabla
        print("\nMaterias disponibles (no inscriptas):")
        
        # Preparar datos para la tabla
        materias_data = []
        for mat in materias_disponibles:
            # Contar estudiantes inscriptos en esta materia
            estudiantes_inscriptos = sum(
                1 for ins in inscripciones 
                if ins["MateriaId"] == mat["Id"]
            )
            
            materias_data.append({
                'código': mat['Codigo'],
                'nombre': mat['Nombre'],
                'estudiantes': str(estudiantes_inscriptos)
            })
        
        # Mostrar tabla
        print_table(
            headers=['Código', 'Nombre', 'Estudiantes Inscriptos'],
            rows=materias_data,
            column_widths={
                'código': 8,
                'nombre': 40,
                'estudiantes': 10
            }
        )
        
        # Validar materia
        while True:
            codigo = input("\nIngrese CÓDIGO de la materia (o presione Enter para cancelar): ").strip()
            if not codigo:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            materia = next((m for m in materias if m["Codigo"] == codigo), None)
            if not materia:
                print("Error: CÓDIGO de materia no válido. Intente nuevamente o presione Enter para cancelar.")
                continue
                
            # Verificar si ya existe una inscripción para este estudiante en esta materia
            inscripciones = self.excel.obtener_inscripciones()
            existe_inscripcion = any(
                ins["EstudianteId"] == estudiante["Id"] and ins["MateriaId"] == materia["Id"] 
                for ins in inscripciones
            )
            
            if existe_inscripcion:
                print(f"Error: {estudiante['Nombre']} {estudiante['Apellido']} ya está inscripto en {materia['Nombre']}.")
                if confirmar_salida("¿Desea intentar con otra materia? (s/n): "):
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            break
        
        # Validar nota
        while True:
            nota_str = input("\nIngrese la nota (1-10, o presione Enter para cancelar): ").strip()
            if not nota_str:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            if validar_nota(nota_str):
                nota = float(nota_str.replace(',', '.'))
                break
                
            print("Error: La nota debe ser un número entre 1 y 10.")
            if confirmar_salida("¿Desea intentar con otra nota? (s/n): "):
                print("\nOperación cancelada.")
                pausar()
                return
        
        # Crear la inscripción
        try:
            nuevo_id = generar_id("Inscripciones")
            self.excel.agregar_inscripcion([nuevo_id, estudiante["Id"], materia["Id"], str(nota)])
            print("\n✅ Inscripción registrada con éxito.")
        except Exception as e:
            print(f"\n❌ Error al registrar la inscripción: {str(e)}")
            
        pausar()


    def listar_inscripciones(self):
        limpiar_pantalla()
        inscripciones = self.excel.obtener_inscripciones()
        
        if not inscripciones:
            print("No hay inscripciones registradas.")
            pausar()
            return

        estudiantes = self.excel.obtener_estudiantes()
        materias = self.excel.obtener_materias()
        
        # Crear diccionarios para búsqueda rápida
        estudiantes_dict = {e["Id"]: e for e in estudiantes}
        materias_dict = {m["Id"]: m for m in materias}
        
        # Preparar datos para la tabla
        inscripciones_data = []
        inscripciones_invalidas = 0
        
        for ins in inscripciones:
            est = estudiantes_dict.get(ins["EstudianteId"])
            mat = materias_dict.get(ins["MateriaId"])
            
            if est and mat:
                # Mostrar "Sin calificar" si no hay nota asignada
                nota = "Sin calificar" if not ins['Nota'] or ins['Nota'] == "" else str(ins['Nota'])
                # Formatear la fecha de inscripción
                fecha_inscripcion = ins.get('Fecha', 'N/A')
                if fecha_inscripcion and fecha_inscripcion != 'N/A':
                    try:
                        from datetime import datetime
                        fecha_obj = datetime.strptime(str(fecha_inscripcion), '%Y-%m-%d %H:%M:%S')
                        fecha_formateada = fecha_obj.strftime('%d/%m/%Y %H:%M')
                    except (ValueError, TypeError):
                        fecha_formateada = str(fecha_inscripcion)
                else:
                    fecha_formateada = 'N/A'
                
                inscripciones_data.append({
                    'estudiante': f"{est['Nombre']} {est['Apellido']}",
                    'legajo': est.get('Legajo', 'N/A'),
                    'materia': mat['Nombre'],
                    'nota': nota,
                    'fecha': fecha_formateada
                })
            else:
                inscripciones_invalidas += 1
        
        # Mostrar tabla
        print_table(
            headers=['estudiante', 'legajo', 'materia', 'nota', 'fecha'],
            rows=inscripciones_data,
            column_widths={
                'estudiante': 25,
                'legajo': 15,
                'materia': 25,
                'nota': 8,
                'fecha': 20
            },
            display_headers=['Estudiante', 'Legajo', 'Materia', 'Nota', 'Fecha Inscripción'],
            title="LISTADO DE INSCRIPCIONES",
            footer=(
                f"Total de inscripciones: {len(inscripciones)} | "
                f"Válidas: {len(inscripciones_data)} | "
                f"Con errores: {inscripciones_invalidas}"
            )
        )
        
        # Mostrar advertencia si hay inscripciones inválidas
        if inscripciones_invalidas > 0:
            print(f"\n⚠️  Advertencia: {inscripciones_invalidas} inscripción(es) con datos inconsistentes "
                  "(estudiante o materia no encontrados)")
        
        pausar()