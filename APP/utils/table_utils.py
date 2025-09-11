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
    
    # Crear línea de encabezado
    header_line = ""
    separator_line = ""
    
    if show_index:
        header_line += "  #  |"
        separator_line += "-----+-"
    
    for i, h in enumerate(headers_lower):
        display_text = str(display_headers_list[i])
        header_line += f" {display_text:<{column_widths[h]}} |"
        separator_line += "-" * (column_widths[h] + 2) + "+"
    
    # Imprimir separador superior
    print(separator_line)
    # Imprimir encabezado
    print(header_line)
    # Imprimir separador inferior
    print(separator_line)
    
    # Imprimir filas
    for i, row in enumerate(rows, 1):
        # Convertir todas las celdas a string y manejar saltos de línea
        str_row = {k: str(v) if v is not None else '' for k, v in row.items()}
        
        # Encontrar el número máximo de líneas necesarias para esta fila
        max_lines = 1
        for h in headers_lower:
            lines = str_row.get(h, '').split('\n')
            max_lines = max(max_lines, len(lines))
        
        # Imprimir cada línea de la fila (puede ser múltiples líneas por celda)
        for line_num in range(max_lines):
            # Mostrar número de fila solo en la primera línea
            if line_num == 0 and show_index:
                print(f"{i:>4} |", end=" ")
            elif show_index:
                print("     ", end=" ")  # Espacio para alinear columnas
                
            # Imprimir cada celda de la fila
            for j, h in enumerate(headers_lower):
                cell_lines = str_row.get(h, '').split('\n')
                if line_num < len(cell_lines):
                    cell_value = cell_lines[line_num]
                else:
                    cell_value = ""
                
                # Truncar el valor si es más largo que el ancho de la columna
                if len(cell_value) > column_widths[h]:
                    cell_value = cell_value[:column_widths[h]-3] + "..."
                print(f" {cell_value:<{column_widths[h]}} |", end="")
            print()  # Nueva línea para la siguiente línea de la fila
        # Imprimir separador de fila si hay más filas o si es la última fila
        if i < len(rows) or line_num < max_lines - 1:
            print(separator_line)
    
    # Imprimir pie de tabla
    if footer:
        print(separator_line)
        print(f"{footer:^{len(separator_line)}}")
    print()  # Espacio adicional después de la tabla
