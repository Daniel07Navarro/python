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


def leerUno(event, logger, _id):
    """
    Lee un servicio.
    ----------
    Recibe:
        (id)
    ----------
    Retorna:
        idItem
        nombre
        descripcion
        precio actual
        imagen
        duracion
        estado
    """
    
    # Creando tupla de args
    args = ()
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Creando la lista de args de respuesta
    resp_args = ["idItem",
                 "nombre",
                 "descripcion",
                 "precio actual",
                 "imagen",
                 "duracion",
                 "estado",]
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Servicio_LeerUno', args, resp_args)
    
    # Generando respuesta
    if success:
        status = 200
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response

def modificar(event, logger, _id):
    """
    Modifica una especificacion.
    ----------
    Recibe:
        (idItem) o idServicio
        nombre
        descripcion
        imagen
        precio
        duracion
    ----------
    Retorna:
        None
    """
    
    # Creando tupla de args
    args = dbconn.get_args(event, logger,
                            "idItem",
                            "nombre",
                            "descripcion",
                            "imagen",
                            "precio",
                            "duracion")
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Servicio_Actualizar', args)
    
    # Generando respuesta
    if success:
        status = 204
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response


def eliminar(event, logger, _id):
    """
    Elimina un servicio.
    ----------
    Recibe:
        (idItem o idServicio)
    ----------
    Retorna:
        None
    """
    
    # Creando tupla de args
    args = ()
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Servicio_Eliminar', args)
    
    # Generando respuesta
    if success:
        status = 204
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response

def crear(event, logger):
    """
    Crea un Producto.
    ----------
    Recibe:
        nombre
        descripcion
        imagen
        precio
        duracion
    ----------
    Retorna:
        None
    """
    # Creando tupla de args
    args = dbconn.get_args(event, logger,
                            "nombre",
                            "descripcion",
                            "imagen",
                            "precio",
                            "duracion")
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Servicio_Crear', args)
    
    # Generando respuesta
    if success:
        status = 201
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response
    
    
def leer(event, logger, filter):
    """
    Lee todos .
    ----------
    Recibe: 
    ----------
    Retorna:
        tabla:
            idItem
            nombre
            descripcion
            precioActual
            imagen
            duracion
            disponible
    """

    
    # Creando la lista de args de respuesta
    resp_args = ["idItem",
                 "nombre",
                 "descripcion",
                 "precioActual",
                 "imagen",
                 "duracion",
                 "disponibilidad"]
    
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Servicio_Leer', None, resp_args)
    

    # Generando respuesta
    if success:
        status = 200
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response
