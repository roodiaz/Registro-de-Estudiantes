from typing import List, Dict, Any, Optional

def print_table(
    headers: List[str],
    rows: List[Dict[str, Any]],
    column_widths: Optional[Dict[str, int]] = None,
    show_index: bool = False,
    title: Optional[str] = None,
    footer: Optional[str] = None,
    display_headers: Optional[List[str]] = None
) -> None:
    """
    Imprime una tabla formateada a partir de una lista de diccionarios.
    
    Args:
        headers: Lista de encabezados de columna
        rows: Lista de diccionarios con los datos de cada fila
        column_widths: Anchos personalizados para las columnas (opcional)
        show_index: Si es True, muestra un índice numérico en la primera columna
        title: Título opcional para la tabla
        footer: Texto opcional para mostrar al final de la tabla
    """
    if not rows:
        print("No hay datos para mostrar.")
        return
    
    # Asegurarse de que todos los encabezados estén en minúsculas
    headers_lower = [h.lower() for h in headers]
    
    # Calcular anchos de columna si no se especifican
    if not column_widths:
        column_widths = {}
        for h in headers_lower:
            # Ancho mínimo de la columna (máximo entre el ancho del encabezado y el dato más largo)
            max_width = max(
                len(str(h)),  # Ancho del encabezado
                max((len(str(row.get(h, ''))) for row in rows), default=0)  # Ancho del dato más largo
            )
            column_widths[h] = min(max_width + 2, 50)  # Límite de 50 caracteres por columna
    
    # Asegurar que todos los encabezados tengan un ancho definido
    for h in headers_lower:
        if h not in column_widths:
            column_widths[h] = len(h) + 2
    
    # Ajustar el ancho de la tabla (suma de anchos de columna + bordes)
    table_width = sum(column_widths.values()) + len(headers) + 1
    if show_index:
        table_width += 7  # Espacio para la columna de índice
    
    # Imprimir título si se proporciona
    if title:
        print("\n" + "=" * table_width)
        print(f"{title:^{table_width}}")
        print("=" * table_width)
    
    # Usar display_headers si está definido, de lo contrario usar los headers en minúsculas
    display_headers_list = display_headers if display_headers is not None else [h.title() for h in headers_lower]
    
    # Asegurarse de que display_headers tenga la misma longitud que headers
    if len(display_headers_list) != len(headers_lower):
        display_headers_list = [h.title() for h in headers_lower]
    
    # Imprimir encabezados
    header_line = ""
    if show_index:
        header_line += "  #  |"
    
    for i, h in enumerate(headers_lower):
        display_text = str(display_headers_list[i])
        header_line += f" {display_text:<{column_widths[h]}}|"
    
    print("-" * (len(header_line) + 1))
    print(header_line)
    print("-" * (len(header_line) + 1))
    
    # Imprimir filas
    for idx, row in enumerate(rows, 1):
        row_line = ""
        if show_index:
            row_line += f" {idx:<3} |"
        
        for h in headers_lower:
            value = str(row.get(h, '')).replace('\n', ' ').replace('\r', '')[:50]  # Limitar a 50 caracteres
            row_line += f" {value:<{column_widths[h]}}|"
        
        print(row_line)
    
    # Imprimir pie de tabla
    print("-" * (len(header_line) + 1))
    if footer:
        print(f"{footer}")
    print()  # Espacio adicional después de la tabla
