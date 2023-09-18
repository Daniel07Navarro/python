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

resourcePath = '/consulta'

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
            # Leer consultas
            response = leerUno(event, logger, _id)
        elif httpMethod == patchMethod:
            # Modificar consultas
            response = modificar(event, logger, _id)
        elif httpMethod == deleteMethod:
            # Eliminar consultas
            response = eliminar(event, logger, _id)
            
        else:
            #Cualquier otro caso
            response = rb.buildResponse(404, 'Funcion no encontrada')
    else:
        # Si no tiene el parámetro de ID
        if httpMethod == postMethod:
            # Crear encargados
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
    Leer consultas.
    ----------
    Recibe:
        (Id)
    ----------
    Retorna:
        idCliente
        mensaje
        idFase
        fechaCreacion
        idEncargado
        fechaCierre
        idRazonCierre
        estado
        
    """
    
    # Creando tupla de args
    args = ()
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Creando la lista de args de respuesta
    resp_args = [ "idCliente",
                  "mensaje",
                  "fase",
                  "fechaCreacion",
                  "encargado",
                  "fechaCierre",
                  "razonCierre",
                  "estado"]
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_consulta_LeerUno', args, resp_args)
    
    # Generando respuesta
    if success:
        status = 200
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response

def modificar(event, logger, _id):
    """
    Modificar consultas.
    ----------
    Recibe:
        (ID)
        idCliente
        mensaje
        idFase
        fechaCreacion
        idEncargado
        fechaCierre
        idRazonCierre
        estado
    ----------
    Retorna:
        None
    """
    
    # Creando tupla de args
    args = dbconn.get_args(event, logger,
                          "idCliente",
                          "mensaje",
                          "idFase",
                          "fechaCreacion,
                          "idEncargado",
                          "fechaCierre",
                          "idRazonCierre",
                          "estado")
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_consulta_Actualizar', args)
    
    # Generando respuesta
    if success:
        status = 204
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response

def eliminar(event, logger, _id):
    """
    Eliminar consultas.
    ----------
    Recibe:
        (id)
    ----------
    Retorna:
        None
    """
    
    # Creando tupla de args
    args = ()
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_consulta_Eliminar', args)
    
    # Generando respuesta
    if success:
        status = 204
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response


def crear(event, logger):
    """
    Crea consultas.
    ----------
    Recibe:
        idCliente
        mensaje
        idFase
        idEncargado
        estado
        
    ----------
    Retorna:
        None
    """
    # Creando tupla de args
    args = dbconn.get_args(event, logger,
                            "mensaje",
                            "idFase",
                            "idEncargado",
                            "estado")
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_consulta_crear', args)
    
    # Generando respuesta
    if success:
        status = 201
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response
    
    
def leer(event, logger):
    """
    Lee todas las consultas activos.
    ----------
    Recibe:
        None
    ----------
    Retorna:
        tabla:
                idCliente
                mensaje
                fase
                fechaCreacion
                encargado
                fechaCierre
                razonCierre
                estado
    """
    
   # Creando la lista de args de respuesta
    resp_args = [ "idCliente",
                  "mensaje",
                  "fase",
                  "fechaCreacion",
                  "encargado",
                  "fechaCierre",
                  "razonCierre",
                  "estado"]
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_consulta_Leer', None, resp_args)
    
    # Generando respuesta
    if success:
        status = 200
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response
    
 