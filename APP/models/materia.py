class Materia:
    def __init__(self, id, codigo, nombre):
        self.id = id
        self.codigo = codigo.upper()  # Store code in uppercase
        self.nombre = nombre

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
