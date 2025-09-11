# 🎓 Sistema de Gestión de Estudiantes

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un sistema de gestión académica desarrollado en Python que permite administrar estudiantes, materias e inscripciones mediante una interfaz de consola intuitiva. El sistema almacena los datos en un archivo Excel estructurado y ofrece funcionalidades de exportación a CSV.

## 🚀 Características Principales

- **Gestión Completa de Estudiantes**
  - Altas, bajas y modificaciones de estudiantes
  - Validación de legajos únicos
  - Cálculo automático de promedios

- **Administración de Materias**
  - Creación y gestión de asignaturas
  - Códigos de materia únicos
  - Control de materias con estudiantes inscriptos

- **Sistema de Inscripciones**
  - Inscripción de estudiantes a materias
  - Carga de calificaciones
  - Validación de inscripciones duplicadas

- **Exportación de Datos**
  - Exportación completa a CSV
  - Exportación individual por estudiante
  - Nombres de archivo descriptivos

## 📋 Requisitos Previos

- Python 3.9 o superior
- Sistema operativo: Windows, macOS o Linux
- Permisos de escritura en el directorio de la aplicación

## 🛠️ Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/Registro-de-Estudiantes.git
   cd Registro-de-Estudiantes
   ```

2. (Opcional) Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Ejecución

1. Navega al directorio de la aplicación:
   ```bash
   cd APP
   ```

2. Ejecuta el programa principal:
   ```bash
   python main.py
   ```

3. Navega por los menús usando los números correspondientes y sigue las instrucciones en pantalla.

## 📁 Estructura del Proyecto

```
Registro-de-Estudiantes/
├── APP/
│   ├── models/               # Modelos de datos
│   │   ├── estudiante.py
│   │   ├── inscripcion.py
│   │   └── materia.py
│   │
│   ├── persistence/          # Manejo de persistencia
│   │   ├── csv_exporter.py
│   │   └── excel_manager.py
│   │
│   ├── services/             # Lógica de negocio
│   │   ├── estudiante_service.py
│   │   ├── inscripcion_service.py
│   │   └── materia_service.py
│   │
│   ├── utils/                # Utilidades
│   │   ├── helpers.py
│   │   ├── input_utils.py
│   │   ├── table_utils.py
│   │   └── validators.py
│   │
│   └── main.py              # Punto de entrada
│
├── data/                    # Datos de la aplicación
│   └── registro_estudiantes.xlsx
│
├── requirements.txt         # Dependencias
└── README.md               # Este archivo
```

## 📚 Librerías Utilizadas

- **openpyxl** (>=3.0.0): Lectura y escritura de archivos Excel (.xlsx)
- **uuid**: Generación de identificadores únicos para registros
- **os**: Manejo de rutas y directorios del sistema operativo
- **csv**: Exportación de datos a archivos CSV
- **datetime**: Manejo de fechas y horas
- **re**: Expresiones regulares para validación de datos

## 🎯 Uso Básico

### Agregar un Estudiante
1. Selecciona "Gestión de Estudiantes"
2. Elige "Crear estudiante"
3. Completa los datos solicitados (legajo, nombre, apellido)
4. Confirma la operación

### Inscribir un Estudiante a una Materia
1. Selecciona "Gestión de Inscripciones"
2. Elige "Inscribir estudiante en materia"
3. Selecciona el estudiante por su legajo
4. Elige la materia por su código
5. Ingresa la calificación (opcional)

### Exportar Datos
1. Selecciona "Exportar datos"
2. Elige el tipo de exportación (todos los estudiantes o por legajo)
3. Sigue las instrucciones en pantalla

## ⚠️ Limitaciones y Aclaraciones

- No modificar manualmente el archivo Excel generado
- Las notas no pueden ser modificadas una vez cargadas
- Los códigos de materia deben ser únicos
- Los legajos de estudiante deben ser únicos
- Se recomienda hacer copias de seguridad periódicas de los datos

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ✉️ Contacto

- **Autor**: [Rocio Diaz]
- **Asignatura**: Ingeniería de Software
- **Año**: 2025

---

Desarrollado con ChatGPT y Windsurf para el Trabajo Práctico de Ingeniería de Software.
