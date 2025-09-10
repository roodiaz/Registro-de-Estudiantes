import uuid
import os

def generar_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:6]}"

def validar_legajo(legajo):
    return legajo.isdigit()

def limpiar_pantalla():
    # Windows
    if os.name == "nt":
        os.system("cls")
    # Linux/Mac
    else:
        os.system("clear")

def pausar():
    input("\nPresione Enter para continuar...")
