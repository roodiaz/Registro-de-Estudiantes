from services.estudiante_service import EstudianteService
from services.materia_service import MateriaService
from services.inscripcion_service import InscripcionService
from persistence.csv_exporter import CSVExporter
from utils.helpers import limpiar_pantalla


def menu_estudiantes(servicio):
    while True:
        limpiar_pantalla()
        print("\n--- Gestión de Estudiantes ---\n")
        print("1. Crear estudiante")
        print("2. Listar estudiantes")
        print("3. Modificar estudiante")
        print("4. Eliminar estudiante")
        print("5. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ")
        if opcion == "1":
            servicio.crear_estudiante()
        elif opcion == "2":
            servicio.listar_estudiantes()
        elif opcion == "3":
            servicio.modificar_estudiante()
        elif opcion == "4":
            servicio.eliminar_estudiante()
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")


def menu_materias(servicio):
    while True:
        limpiar_pantalla()
        print("\n--- Gestión de Materias ---\n")
        print("1. Crear materia")
        print("2. Listar materias")
        print("3. Eliminar materia")
        print("4. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ")
        if opcion == "1":
            servicio.crear_materia()
        elif opcion == "2":
            servicio.listar_materias()
        elif opcion == "3":
            servicio.eliminar_materia()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")


def menu_inscripciones(servicio):
    while True:
        limpiar_pantalla()
        print("\n--- Gestión de Inscripciones ---\n")
        print("1. Inscribir estudiante en materia")
        print("2. Listar inscripciones")
        print("3. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ")
        if opcion == "1":
            servicio.inscribir_estudiante()
        elif opcion == "2":
            servicio.listar_inscripciones()
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")


def menu_exportaciones(exporter, inscripcion_service):
    while True:
        limpiar_pantalla()
        print("\n--- Exportar datos ---\n")
        print("1. Exportar todo")
        print("2. Exportar estudiante por legajo")
        print("3. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ")
        if opcion == "1":
            exporter.exportar_todo()
        elif opcion == "2":
            # Mostrar lista de estudiantes usando el servicio de inscripciones
            if inscripcion_service.mostrar_estudiantes():
                legajo = input("\nIngrese el LEGAJO del estudiante a exportar: ").strip()
                if legajo:  # Solo intentar exportar si se ingresó un legajo
                    exporter.exportar_estudiante(legajo)
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")


def mostrar_menu():
    print("\n=== Sistema de Registro de Estudiantes ===\n")
    print("1. Gestión de Estudiantes")
    print("2. Gestión de Materias")
    print("3. Gestión de Inscripciones")
    print("4. Exportar datos")
    print("5. Salir")


def main():
    estudiante_service = EstudianteService()
    materia_service = MateriaService()
    inscripcion_service = InscripcionService()
    exporter = CSVExporter()

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            menu_estudiantes(estudiante_service)
        elif opcion == "2":
            menu_materias(materia_service)
        elif opcion == "3":
            menu_inscripciones(inscripcion_service)
        elif opcion == "4":
            menu_exportaciones(exporter, inscripcion_service)
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    main()
