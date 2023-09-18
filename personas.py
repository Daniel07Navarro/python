import sys
import logging
import json
import os

import pymysql
import dbconn
import responseBuilder as rb

# Variables de Path:
getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'

resourcePath = '/servicio'

logger, conn = dbconn.initialize_connection()

def lambda_handler(event, context):
    #logger.info(event)
    
    httpMethod = event['httpMethod']
    path = event['path']
    _id = dbconn.get_parameter(event, "id")
    
    # Separar las funciones de acuerdo a si da un parámetro o no y el método a realizar
    if (_id is not None):
        # Si tiene el parámetro de ID
        if httpMethod == getMethod:
            # Leer un servicio 
            response = leerUno(event, logger, _id)
        elif httpMethod == patchMethod:
            # Modificar servicio
            response = modificar(event, logger, _id)
        elif httpMethod == deleteMethod:
            # Eliminar persona
            response = eliminar(event, logger, _id)
            
        else:
            #Cualquier otro caso
            response = rb.buildResponse(404, 'Funcion no encontrada')
    else:
        # Si no tiene el parámetro de ID
        if httpMethod == postMethod:
            # Crear persona
            response = crear(event, logger)
        elif httpMethod == getMethod:
            # Leer (todos los que no estan eliminados)
            response = leer(event, logger)
           
        else:
            #Cualquier otro caso
            response = rb.buildResponse(404, 'Funcion no encontrada')
    
    return response


def leerUno(event, logger, _id):
    """
    Lee una persona .
    ----------
    Recibe:
        (idItem)
    ----------
    Retorna:
        idPersona
        nombre
        email
        telefono
        estado
    """
    
    # Creando tupla de args
    args = ()
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Creando la lista de args de respuesta
    resp_args = ["idPersona",
                 "nombre",
                 "email",
                 "telefono"
                 "estado"]
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Persona_LeerUno', args, resp_args)
    
    # Generando respuesta
    if success:
        status = 200
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response

    
def leer(event, logger):
    """
    Lee todas las personas activas.
    ----------
    Recibe:
        None
    ----------
    Retorna:
        tabla:
            idPersona
            nombre
            email
            telefono
            estado
    """
    
    # Creando la lista de args de respuesta
    resp_args = ["idPersona",
                 "nombre",
                 "email",
                 "telefono",
                 "estado"]
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Persona_Leer', None, resp_args)
    
    # Generando respuesta
    if success:
        status = 200
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response
    
### SIN USAR ###
def leerTodo(event, logger): 
    """
    Lee todas las personas, incluyendo las eliminadas.
    ----------
    Recibe:
        None
    ----------
    Retorna:
        tabla:
            idPersona
            nombre
            email
            telefono
            estado
    """
    
    # Creando la lista de args de respuesta
    resp_args = ["idPersona",
                 "nombre",
                 "email", 
                 "telefono",
                 "estado"]
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Persona_LeerTodo', None, resp_args)
    
    # Generando respuesta
    if success:
        status = 200
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response