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

resourcePath = '/producto'

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
            # Si tiene como parámetro 'search'
            if(_id == 'search'):
                response = leer(event, logger)
            else:
                # Leer un producto
                response = leerUno(event, logger, _id)
        elif httpMethod == patchMethod:
            # Modificar producto
            response = modificar(event, logger, _id)
        elif httpMethod == deleteMethod:
            # Eliminar producto
            response = eliminar(event, logger, _id)
            
        else:
            #Cualquier otro caso
            response = rb.buildResponse(404, 'Funcion no encontrada')
    else:
        # Si no tiene el parámetro de ID
        if httpMethod == postMethod:
            # Crear producto
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
    Lee una categoría.
    ----------
    Recibe:
        (id)
    ----------
    Retorna:
        idItem
        nombre
        descripcion
        precio
        imagen
        categoria
        stock
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
                 "precio",
                 "imagen",
                 "categoria",
                 "stock",
                 "estado"]
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Producto_LeerUno', args, resp_args)
    
    # Generando respuesta
    if success:
        status = 200
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response

def modificar(event, logger, _id):
    """
    Modifica un producto.
    ----------
    Recibe:
        (id)
        nombre
        descripcion
        precio
        imagen
        idCategoria
        stock
        estado
    ----------
    Retorna:
        affected
    """
    
    # Creando tupla de args
    args = dbconn.get_args(event, logger,
                            "nombre",
                            "descripcion",
                            "precio",
                            "imagen",
                            "idCategoria",
                            "stock",
                            "estado")
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Producto_Actualizar', args, ["affected"])
    
    # Generando respuesta
    if success:
        status = 204
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response

def eliminar(event, logger, _id):
    """
    Elimina una categoría.
    ----------
    Recibe:
        (id)
    ----------
    Retorna:
        affected
    """
    
    # Creando tupla de args
    args = ()
    # Añadiendo la id a los args
    args = (_id,) + args
    
    # Realizando procedimientos
    
    # Eliminando las especificaciones:
    success, data = dbconn.callproc(logger, conn, 'sp_Especificacion_EliminarPorProducto', args, None)
    
    # Eliminando las ofertas:
    if success:
        success, data = dbconn.callproc(logger, conn, 'sp_Oferta_EliminarPorItem', args, None)
    
    # Eliminando el producto
    if success:
        success, data = dbconn.callproc(logger, conn, 'sp_Producto_Eliminar', args, ["affected"])
        
    
    # Generando respuesta
    if success:
        status = 200
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
        precio
        imagen
        categoria
        stock
    ----------
    Retorna:
        None
    """
    # Creando tupla de args
    args = dbconn.get_args(event, logger,
                            "nombre",
                            "descripcion",
                            "precio",
                            "imagen",
                            "idCategoria",
                            "stock")
    
    _especificaciones = dbconn.get_arg(event, logger, "especificaciones")
    
    # Realizando procedimientos
    success, data = dbconn.callproc(logger, conn, 'sp_Producto_Crear', args)
    
    _idProd = json.loads(data)[0][0]
    
    #Realizando la creación de especificaciones
    if success and _especificaciones is not None:
        for _esp in _especificaciones:
            args = (_idProd, _esp.get("titulo"), _esp.get("descripcion"))
            success, _edata = dbconn.callproc(logger, conn, 'sp_Especificacion_Crear', args)
    
    # Generando respuesta
    if success:
        status = 201
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response
    
    
def leer(event, logger):
    """
    Lee todos los productos activos.
    ----------
    Recibe:
        (state)
        (searchString)
    ----------
    Retorna:
        tabla:
            idItem
            nombre
            descripcion
            precio
            imagen
            categoria
            stock
            estado
    """
    
    # Creando tupla de args
    args = ()
    
    _state = dbconn.get_queryParameter(event, 'state');
    if(_state is None):
        _state = 'all'
        
    _searchString = dbconn.get_queryParameter(event, 'string')
    
    if(_searchString is None):
        _searchString = '%'
    else:
        _searchString = '%' + _searchString + '%'
    
    _idCategoria = dbconn.get_queryParameter(event, 'categ');
    if(_idCategoria is None):
        _idCategoria = -1
    
    # Añadiendo la id a los args
    args = (_state, _searchString, _idCategoria, ) + args
    
    # Creando la lista de args de respuesta
    resp_args = ["idItem",
                 "nombre",
                 "descripcion",
                 "precio",
                 "imagen",
                 "categoria",
                 "stock",
                 "estado"]
    
    
    # Realizando procedimiento
    success, data = dbconn.callproc(logger, conn, 'sp_Producto_Leer', args, resp_args)

    # Creando la lista de args de respuesta de productos
    resp_args_esp = ["idEspecificacion",
                 "idProducto",
                 "nombre_producto",
                 "titulo",
                 "descripcion"]
    
    if success and data is not None:
        for prod in data:
            _idItem = prod['idItem']
            # Creando tupla de args
            args_esp = ()
            # Añadiendo la id a los args
            args_esp = (_idItem,) + args_esp
            _edata = dbconn.callproc(logger, conn, 'sp_Especificacion_LeerPorProducto', args_esp,resp_args_esp)
            data = data +_edata
    
    
    # Generando respuesta
    if success:
        status = 200
    else:
        status = 500
    response = rb.buildResponse(status, data)
    return response
