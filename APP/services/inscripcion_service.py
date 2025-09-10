from persistence.excel_manager import ExcelManager
from utils.helpers import generar_id, pausar, limpiar_pantalla
from utils.validators import validar_nota
from utils.input_utils import confirmar_salida

class InscripcionService:
    def __init__(self):
        self.excel = ExcelManager()

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
                'ID': est['Id'],
                'Nombre': est['Nombre'],
                'Apellido': est['Apellido'],
                'Legajo': est.get('Legajo', 'N/A'),
                'Materias': str(materias_inscriptas)
            })
        
        # Mostrar tabla
        print_table(
            headers=['ID', 'Nombre', 'Apellido', 'Legajo', 'Materias Inscriptas'],
            rows=estudiantes_data,
            column_widths={
                'ID': 8,
                'Nombre': 20,
                'Apellido': 20,
                'Legajo': 15,
                'Materias': 10
            }
        )
        
        # Validar estudiante
        while True:
            est_id = input("\nIngrese ID del estudiante (o presione Enter para cancelar): ").strip()
            if not est_id:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            estudiante = next((e for e in estudiantes if e["Id"] == est_id), None)
            if estudiante:
                break
                
            print("Error: ID de estudiante no válido. Intente nuevamente o presione Enter para cancelar.")
        
        # Mostrar materias disponibles en tabla
        print("\nMaterias disponibles:")
        
        # Preparar datos para la tabla
        materias_data = []
        for mat in materias:
            # Contar estudiantes inscriptos en esta materia
            inscripciones = self.excel.obtener_inscripciones()
            estudiantes_inscriptos = sum(1 for ins in inscripciones if ins["MateriaId"] == mat["Id"])
            
            materias_data.append({
                'ID': mat['Id'],
                'Nombre': mat['Nombre'],
                'Estudiantes': str(estudiantes_inscriptos)
            })
        
        # Mostrar tabla
        print_table(
            headers=['ID', 'Materia', 'Estudiantes Inscriptos'],
            rows=materias_data,
            column_widths={
                'ID': 8,
                'Materia': 40,
                'Estudiantes': 10
            }
        )
        
        # Validar materia
        while True:
            mat_id = input("\nIngrese ID de la materia (o presione Enter para cancelar): ").strip()
            if not mat_id:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            materia = next((m for m in materias if m["Id"] == mat_id), None)
            if not materia:
                print("Error: ID de materia no válido. Intente nuevamente o presione Enter para cancelar.")
                continue
                
            # Verificar si ya existe una inscripción para este estudiante en esta materia
            inscripciones = self.excel.obtener_inscripciones()
            existe_inscripcion = any(
                ins["EstudianteId"] == est_id and ins["MateriaId"] == mat_id 
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
            nota_str = input("\nIngrese nota (1-10, o presione Enter para cancelar): ").strip()
            if not nota_str:
                if confirmar_salida():
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            if not validar_nota(nota_str):
                print("Error: La nota debe ser un número entre 1 y 10.")
                if confirmar_salida("¿Desea intentar con otra nota? (s/n): "):
                    print("\nOperación cancelada.")
                    pausar()
                    return
                continue
                
            nota = float(nota_str)
            break
        
        # Confirmar antes de guardar
        print(f"\nResumen de la inscripción:")
        print(f"Estudiante: {estudiante['Nombre']} {estudiante['Apellido']} (ID: {estudiante['Id']})")
        print(f"Materia: {materia['Nombre']} (ID: {materia['Id']})")
        print(f"Nota: {nota}")
        
        if not confirmar_salida("\n¿Desea confirmar la inscripción? (s/n): "):
            print("\nOperación cancelada.")
            pausar()
            return
        
        # Crear la inscripción
        try:
            nuevo_id = generar_id("Inscripciones")
            self.excel.agregar_inscripcion([nuevo_id, est_id, mat_id, nota])
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
                inscripciones_data.append({
                    'id': ins['Id'],
                    'estudiante': f"{est['Nombre']} {est['Apellido']}",
                    'legajo': est.get('Legajo', 'N/A'),
                    'materia': mat['Nombre'],
                    'nota': str(ins['Nota'])
                })
            else:
                inscripciones_invalidas += 1
        
        # Mostrar tabla
        print_table(
            headers=['ID', 'Estudiante', 'Legajo', 'Materia', 'Nota'],
            rows=inscripciones_data,
            column_widths={
                'id': 8,
                'estudiante': 25,
                'legajo': 15,
                'materia': 25,
                'nota': 8
            },
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