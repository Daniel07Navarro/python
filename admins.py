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

resourcePath = '/categoria'

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
            # Leer una categoría
            response = leerUno(event, logger, _id)
        elif httpMethod == patchMethod:
            # Modificar categoría
            response = modificar(event, logger, _id)
        elif httpMethod == deleteMethod:
            # Eliminar categoría
            response = eliminar(event, logger, _id)
            
        else:
            #Cualquier otro caso
            response = rb.buildResponse(404, 'Funcion no encontrada')
    else:
        # Si no tiene el parámetro de ID
        if httpMethod == postMethod:
            # Crear categoría
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
    Lee un admin.
    ----------
    Recibe:
        (idPersona)
    ----------
    Retorna:
            idPersona
            nombre
            nombre_usuario
            apellido_paterno
            apellido_materno
            dni
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
                 "nombre_usuario",
                 "apellido_paterno",
                 "apellido_materno",
                 "dni",
                 "email",
                 "telefono",
                 "estado"]
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Admin_LeerUno', args, resp_args)
    
    # Generando respuesta
    if success:
        status = 200
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response

def modificar(event, logger, _id):
    """
    Modifica una categoría.
    ----------
    Recibe:
        (idPersona)
        nombre
        apellido_paterno
        apellido_materno
        dni
        email
        telefono
        usuario
        password
    ----------
    Retorna:
        None
    """
    
    # Creando tupla de args
    args = dbconn.get_args(event, logger,
                            "nombre",
                            "apellido_paterno",
                            "apellido_materno",
                            "dni",
                            "email",
                            "telefono",
                            "usuario",
                            "password")
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Admin_Actualizar', args)
    
    # Generando respuesta
    if success:
        status = 204
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response

def eliminar(event, logger, _id):
    """
    Elimina un admin.
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
    success, data = dbconn.callproc(logger, conn, 'sp_Admin_Eliminar', args)
    
    # Generando respuesta
    if success:
        status = 204
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response


def crear(event, logger):
    """
    Crear un admin.
    ----------
    Recibe:
        idPersona
        nombre_usuario
        password
    ----------
    Retorna:
        None
    """
    # Creando tupla de args
    args = dbconn.get_args(event, logger,
                            "nombre",
                            "usuario",
                            "password")
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Admin_Crear', args)
    
    # Generando respuesta
    if success:
        status = 201
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response
    
    
def leer(event, logger):
    """
    Lee todos los admins
    ----------
    Recibe:
        None
    ----------
    Retorna:
        tabla:
            idPersona
            nombre
            nombre_usuario
            apellido_paterno
            apellido_materno
            dni
            email
            telefono
            estado
    """
    
    # Creando la lista de args de respuesta
    resp_args = ["idPersona",
                 "nombre",
                 "nombre_usuario",
                 "apellido_paterno",
                 "apellido_materno",
                 "dni",
                 "email",
                 "telefono",
                 "estado"]
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Admin_Leer', None, resp_args)
    
    # Generando respuesta
    if success:
        status = 200
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response
    