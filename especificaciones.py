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

resourcePath = '/especificacion'

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
            response = leer(event, logger, _id)
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
           
        else:
            #Cualquier otro caso
            response = rb.buildResponse(404, 'Funcion no encontrada')
    
    return response

def modificar(event, logger, _id):
    """
    Modifica una especificacion.
    ----------
    Recibe:
        (idEspecificacion)
        idProducto
        titulo
        descripcion
    ----------
    Retorna:
        None
    """
    
    # Creando tupla de args
    args = dbconn.get_args(event, logger,
                            "idEspecificacion",
                            "idProducto",
                            "titulo",
                            "descripcion")
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Especificacion_Actualizar', args)
    
    # Generando respuesta
    if success:
        status = 204
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response

def eliminar(event, logger, _id):
    """
    Elimina una especificacion.
    ----------
    Recibe:
        (idEspecificacion)
    ----------
    Retorna:
        None
    """
    
    # Creando tupla de args
    args = ()
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Especificacion_Eliminar', args)
    
    # Generando respuesta
    if success:
        status = 204
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response


def crear(event, logger):
    """
    Crea una especificacion.
    ----------
    Recibe:
        idProducto
        titulo
        descripcion
    ----------
    Retorna:
        None
    """
    # Creando tupla de args
    args = dbconn.get_args(event, logger,
                            "idProducto",
                            "titulo",
                            "descripcion")
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Especificacion_Crear', args)
    
    # Generando respuesta
    if success:
        status = 201
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response

    
def leer(event, logger,_id):
    """
    Lee todas las especificaciones de un producto
    ----------
    Recibe:
        id
    ----------
    Retorna:
        tabla:
            idEspecificacion
            idProducto
            titulo
            descripcion
    """
    
    # Creando la lista de args de respuesta
    resp_args = ["idEspecificacion",
                 "idProducto",
                 "titulo",
                 "descripcion"]
    
        # Creando tupla de args
    args = ()
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Especificacion_Leer', args, resp_args)
    
    # Generando respuesta
    if success:
        status = 200
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response
 