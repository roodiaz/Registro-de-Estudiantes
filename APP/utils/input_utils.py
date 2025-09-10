def confirmar_salida(mensaje="¿Desea cancelar la operación? (s/n): "):
    """
    Pregunta al usuario si desea cancelar la operación actual.
    Devuelve True si el usuario desea cancelar, False en caso contrario.
    """
    respuesta = input(mensaje).strip().lower()
    return respuesta == 's'
