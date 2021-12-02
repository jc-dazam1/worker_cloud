from flask_restful import Resource
from flask import request
from flask import jsonify
from time import sleep

from controladores.controladores import convertir_audio

class VistaConvertidorAudio(Resource):
    
    def post(self):
        """
        Servicio que recibe el id del audio a convertir
        """
        convertir_audio(request.json["id_audio"])
        
