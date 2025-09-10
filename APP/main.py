from services.estudiante_service import EstudianteService
from services.materia_service import MateriaService
from services.inscripcion_service import InscripcionService

def mostrar_menu():
    print("\n=== Sistema de Registro de Estudiantes ===\n")
    print("1. Gestión de Estudiantes")
    print("2. Gestión de Materias")
    print("3. Gestión de Inscripciones")
    print("4. Exportar datos")
    print("5. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # TODO: Submenú de estudiantes
            pass
        elif opcion == "2":
            # TODO: Submenú de materias
            pass
        elif opcion == "3":
            # TODO: Submenú de inscripciones
            pass
        elif opcion == "4":
            # TODO: Exportar datos
            pass
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    main()
