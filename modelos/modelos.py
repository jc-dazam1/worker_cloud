from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class Estado(enum.Enum):
   CARGADO = 1
   PROCESADO = 2

class ConversionFormatoAudio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    archivo_original = db.Column(db.String)
    archivo_convertido = db.Column(db.String)
    formato_original = db.Column(db.String)
    formato_destino = db.Column(db.String)
    nombre_archivo = db.Column(db.String)
    usuario = db.Column(db.String)
    estado = db.Column(db.Enum(Estado))
    