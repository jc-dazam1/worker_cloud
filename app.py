from flask import Flask
from modelos.modelos import db
from controladores.controladores import procesar_archivo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:equipo24@database-1.cqyullhbxav6.us-east-1.rds.amazonaws.com:5432/appconversion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

procesar_archivo()