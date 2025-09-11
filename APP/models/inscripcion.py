from datetime import datetime

class Inscripcion:
    def __init__(self, id, estudiante_id, materia_id, nota, fecha=None):
        self.id = id
        self.estudiante_id = estudiante_id
        self.materia_id = materia_id
        self.nota = nota
        self.fecha = fecha if fecha is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'Id': self.id,
            'EstudianteId': self.estudiante_id,
            'MateriaId': self.materia_id,
            'Nota': self.nota,
            'Fecha': self.fecha
        }
