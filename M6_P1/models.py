from sqlalchemy import Column, Integer, String, Boolean
import db

class Tarea(db.Base): #vinvulamos la variable Base del fichero bd.py
    # Dará un nombre al momento de pasar a tabla de la bd
    __tablename__ = "tarea"

    # Dar a un tipo de dato a las columnas de la bd
    id = Column(Integer, primary_key=True) #Automaticamente esta PK será autoincrement
    contenido = Column(String(200), nullable=False) #nullable dirá que el dato si o si tiene que tener un registro
    categoria = Column(String, nullable=False)
    fecha = Column(String, nullable=False)
    hecha = Column(Boolean) #Si la tarea esta hecha o no
    edit = Column(Boolean)

    def __init__(self, contenido, categoria, fecha, hecha, edit):
        self.contenido = contenido
        self.categoria = categoria
        self.fecha = fecha
        self.hecha = hecha
        self.edit = edit

    def __str__(self):
        return "Tarea({}: {} / {}, {})".format(self.id, self.contenido, self.categoria, self.hecha)