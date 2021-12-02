from modelos.modelos import ConversionFormatoAudio, Estado, db
import os
import subprocess
import shutil
import smtplib
import boto3
import json
import time
from botocore.exceptions import NoCredentialsError
from logger import Logger

ACCESS_KEY = 'AKIA3ML4UTNPTEQO5ONO'
SECRET_KEY = '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'

BUCKET_NAME = 'audioconverterbucket'

QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/782482316127/AudioConverter.fifo'
QUEUE_REGION = 'us-west-2'

logs = Logger()

def crear_conexion_notificacion():
    """
    Crea y retorna la conexión con el servidor de correos
    """        
    _smtp = smtplib.SMTP('smtp.gmail.com', 587)
    _smtp.ehlo()
    _smtp.starttls()
    _smtp.login('caecheverri01@gmail.com', 'srieyvupdyskwufw')
    
    return _smtp

def enviar_notificacion():
    """
    Envía una notificación de adevertencia
    """
    _smtp = crear_conexion_notificacion()
    msg = 'Subject: Archivo convertido' + '\n' + 'Hola\n\nEl archivo enviado ya fue convertido'
    _smtp.sendmail('caecheverri01@gmail.com', 'caecheverri01@gmail.com', msg)    
    _smtp.quit()


def convertir_audio(id_registro):
    """
    Convierte un archivo de audio, del formato original a un formato destino.
    Para la realizar la conversion se obtiene el archivo original de la ruta nfs
    luego se ejecuta la utilidad ffmpeg para realizar la conversion del formato y 
    generar el nuevo archivo convertido con el nombre especificado
    """
    dir_path = './tmp_convert/'
        
    registro_audio = ConversionFormatoAudio.query.filter(ConversionFormatoAudio.id == id_registro, ConversionFormatoAudio.estado == Estado.CARGADO).first()
   
    if registro_audio != None:
        archivo_fmt_original = registro_audio.nombre_archivo + '.' + registro_audio.formato_original
        archivo_fmt_destino = registro_audio.nombre_archivo + '.' + registro_audio.formato_destino

        if not os.path.exists(os.path.dirname(dir_path)):
            os.makedirs(os.path.dirname(dir_path))

        archivo_descargado = descargar_archivo_s3(dir_path + archivo_fmt_original, archivo_fmt_original)

        if archivo_descargado :
            file_src = dir_path + archivo_fmt_original
            file_dst = dir_path + archivo_fmt_destino

            subprocess.run(['ffmpeg', '-i' , file_src , '-y' , file_dst])

            archivo_enviado = enviar_archivo_s3(file_dst, archivo_fmt_destino)
            
            if archivo_enviado :
                actualizar_registro_audio(registro_audio, registro_audio.nombre_archivo)
                os.remove(dir_path + archivo_fmt_original)
                os.remove(dir_path + archivo_fmt_destino)
                #enviar_notificacion()
                return True
    
    return False
        

def actualizar_registro_audio(registro_audio, file_converted): 
    """
    Actualiza el registro en la base de datos con el contenido del archivo convertido y el estado procesado
    """
    registro_audio.archivo_convertido = file_converted
    registro_audio.estado = Estado.PROCESADO
    db.session.commit()

def enviar_archivo_s3(archivo_local, archivo_s3):
    """
    Carga un archivo al bucket de AWS S3
    """
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(archivo_local, BUCKET_NAME, archivo_s3)
        logs.info('controlador', 'carga-archivo cargado', archivo_s3)
        return True
    except FileNotFoundError:
        logs.info('controlador', 'carga-archivo no encontrado', archivo_s3)
        return False
    except NoCredentialsError:
        logs.info('controlador', 'carga-credenciales no validas', archivo_s3)
        return False

def descargar_archivo_s3(archivo_local, archivo_s3):
    """
    Descarga un archivo del bucket de AWS S3
    """
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    try:
        s3.download_file(BUCKET_NAME, archivo_s3, archivo_local)
        logs.info('controlador', 'descarga-archivo descargado', archivo_s3)
        return True
    except FileNotFoundError:
        logs.info('controlador', 'descarga-archivo no encontrado', archivo_s3)
        return False
    except NoCredentialsError:
        print("Credentials not available")
        logs.info('controlador', 'descarga-credenciales no validas', archivo_s3)
        return False

def obtener_mensaje_sqs():
    """
    Obtiene un mensaje de la cola AWS SQS
    """
    id_audio = None
    receipt_handle = None
    sqs = boto3.client('sqs', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=QUEUE_REGION)

    response = sqs.receive_message(
        QueueUrl = QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )

    for message in response.get('Messages', []):
        message_body = message['Body']
        receipt_handle = message['ReceiptHandle']
        id_audio = json.loads(message_body)['id_audio']

    return (id_audio, receipt_handle)

def borrar_mensaje_sqs(receipt_handle):
    """
    Borrar un mensaje de la cola AWS SQS
    """
    sqs = boto3.client('sqs', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=QUEUE_REGION)

    response = sqs.delete_message(
        QueueUrl = QUEUE_URL,
        ReceiptHandle=receipt_handle,
    )

def procesar_archivo():
    """
    Inicia el procesamiento de conversion de archivos
    """
    while True:
        (id_audio, receipt_handle) = obtener_mensaje_sqs()
        
        if id_audio != None:
            convertir_audio(id_registro = id_audio)
            borrar_mensaje_sqs(receipt_handle=receipt_handle)

        time.sleep(10)


    
