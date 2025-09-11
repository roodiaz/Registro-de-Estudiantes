# 📘 Registro de estudiantes – Conversación inicial

## Prompt 1
> Vamos a utilizar este proyecto para realizar un tp de Registro de estudiantes, al finalizar el proyecto te voy a solicitar un markdown para poder exportar nuestra conversion en un archivo .md

### Respuesta
Perfecto 🙌. Podemos trabajar todo el proyecto acá mismo, y al final te armo un **archivo .md** bien estructurado con toda la conversación, el código y la documentación que generemos.  

Para organizar mejor el TP de **Registro de estudiantes**, ¿querés que lo armemos como:  
1. **Requerimientos funcionales** (qué debe hacer el sistema).  
2. **Modelo de datos** (tablas SQL/Mongo o clases en C#).  
3. **Arquitectura** (Angular front + API backend, por ejemplo).  
4. **Casos de uso / historias de usuario**.  
5. **Implementación básica** (código ejemplo).  
6. **Conclusión + README final en Markdown**.  

👉 Así, cuando lleguemos al final, exporto todo en un único `.md`.  

¿Querés que arranquemos definiendo los **requerimientos funcionales** del sistema de registro de estudiantes?

---

## Prompt 2
> A continuacion te voy a marcar los puntos mas importantes a tener en cuenta:
>
> 1. Se trata de una aplicacion para llevar un registro de estudiantes  
> 2. Debe ser desarrollada en python  
> 3. Debe contener todas las funcionalidades basicas de un CRUD y una opcion de salir del sistema.  
> 4. Las clases necesarias son:  
> &nbsp;&nbsp;&nbsp;&nbsp;Estudiante: Id, nombre, apellido, legajo, promedio, materias  
> &nbsp;&nbsp;&nbsp;&nbsp;Materias: Id, nombre materia y si queres podes adicionarle algun dato  
> 5. Vamos a utilizar un archivo CSV como base de datos, es decir, cada cambio realizado en el CRUD debe impactar y persistir en el mismo  
> 6. El CSV utilizado como base no debe ser accesible por el usuario de forma sencilla  
> 7. Agregar opcion para exportar los datos en CSV  
> 8. La app debe ser por consola, sin embargo, intenta hacer la interfaz amigable para el usuario.
>
> Teniendo en cuenta todos los puntos mencionados, antes de comenzar a trabajar, tenes alguna pregunta con respecto al desarrollo?

### Respuesta
Genial, gracias por marcar los puntos 👌. Antes de empezar a escribir código quiero confirmar algunos detalles para que no queden dudas:  

1. **Identificador único**: ¿lo generamos automático o lo ingresa el usuario?  
2. **Relación estudiante–materias**: ¿guardamos IDs en el CSV o nombres?  
3. **CSV**: ¿un solo archivo o varios?  
4. **Promedio**: ¿manual o calculado con notas?  
5. **Exportación**: ¿todo o también por estudiante?  
6. **Menú**: ¿opciones numéricas o comandos por texto?  

---

## Prompt 3
> En respuesta a tus consultas:
>
> 1. El Id sera unico y generado de forma automatica  
> 2. Cada estudiante puede tener mas de una materia asignada. En el csv exportable se debe visualizar el nombre de la materia, el utilizado como base la relacion seria mediante Id (como si fuera una base de datos)  
> 3. Puede ser un mismo archivos pero con una hoja para Estudiantes y otra para Materias  
> 4. El promedio sera calculado en base a las notas de las materias, es decir, agrega el campo de nota  
> 5. La exportacion puede ser de todo lo almacenado (con la info del estudiante y sus materias asociadas) y tambien te debe dejar exporta la informacion de un estudiante en especifico (a traves de su legajo)  
> 6. El menu principal y los secundarios deben ser todos numericos
>
> Hay alguna otra duda?

### Respuesta
Perfecto 🙌, súper claro.  
Me quedan solo dos dudas más:  

1. **Persistencia**: CSV no tiene hojas → usamos Excel (.xlsx) con 2 hojas (`Estudiantes` y `Materias`), ¿te parece?  
2. **Notas**: ¿se actualizan manualmente o quedan fijas al asignarlas?  

---

## Prompt 4
> 1. Ya que el CSV no soporta hojas como excel cambiemos el enfoque, usemos un Excel como base. El exportable se mantiene como CSV  
> 2.  
>    - ¿Querés que las notas se actualicen manualmente? No, la nota una vez asignada no puede ser modificada  
>    - ¿El promedio se recalcula automáticamente? Si, el promedio debe ser recalculado siempre
>
> Alguna otra consulta?

### Respuesta
¡Excelente, clarísimo! 🚀  
Entonces:  
- Base en Excel (.xlsx) con hojas `Estudiantes` y `Materias`.  
- Exportación en CSV.  
- Notas fijas.  
- Promedio recalculado siempre.  

👉 Solo falta decidir si necesitamos una hoja intermedia (`Inscripciones`) para guardar la relación estudiante–materia–nota.  

---

## Prompt 5
> Vamos a necesitar una hoja intermedia para asociar el estudiante con la materia, y ese hoja intermedia va a ser la que contenga la nota

### Respuesta
¡Perfecto! 🙌  
Queda así:  
- `Estudiantes`: Id, nombre, apellido, legajo.  
- `Materias`: Id, nombre.  
- `Inscripciones`: Id, EstudianteId, MateriaId, Nota.  

De esa forma, un estudiante puede tener varias materias y un promedio calculado en base a sus inscripciones.  

---

## Prompt 6
> Antes de comenzar con el desarrollo de la app vamos a definir la estructura del codigo. No quiero algo muy complejo, ni algo tan basico en un solo archivo.  
>
> Que tenes para proponer?

### Respuesta
¡Bien ahí! ⚡  
Propuesta: una estructura modular tipo **mini-MVC para consola**:  

registro_estudiantes/
├── main.py # Menú principal
├── models/ # Clases de dominio
├── services/ # CRUDs y lógica de negocio
├── persistence/ # Manejo de Excel/CSV
├── utils/ # Helpers
└── data/ # Archivos de datos


Así evitamos un solo archivo gigante y mantenemos todo ordenado.  

---

## Prompt 7
> Perfecto, continuemos con esa estructura. Si es necesario en el camino aplicaremos algun cambio

### Respuesta
¡Genial! 🚀  
Entonces armamos el esqueleto con las carpetas y archivos vacíos, definiendo las clases y métodos principales.  

---

## Prompt 8
> Listo ya arme la estructura. Pasame todo el codigo necesario para tener la app funcional, luego yo me encargo de testear y avisarte si tengo algun error

### Respuesta
(👉 Aquí fue donde ya se pasó todo el código funcional con `main.py`, `models/`, `services/`, `persistence/` y `utils/` completos).  

---
	
