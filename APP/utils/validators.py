def validar_legajo(legajo):
    """
    Valida el formato del legajo. 
    Debe ser alfanumérico y tener entre 5 y 10 caracteres.
    """
    if not isinstance(legajo, str):
        return False
    return legajo.isalnum() and 5 <= len(legajo) <= 10

def legajo_existe(excel_manager, legajo, id_excluido=None):
    """
    Verifica si ya existe un estudiante con el mismo legajo.
    Si se proporciona id_excluido, ignora al estudiante con ese ID (útil para actualizaciones).
    """
    estudiantes = excel_manager.obtener_estudiantes()
    for est in estudiantes:
        if est["Legajo"] == legajo and (id_excluido is None or est["Id"] != id_excluido):
            return True
    return False

def validar_nota(nota_str):
    """Valida que la nota sea un número entre 1 y 10"""
    try:
        nota = float(nota_str)
        return 1 <= nota <= 10
    except (ValueError, TypeError):
        return False
