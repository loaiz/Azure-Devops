# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 08:30:49 2023

@author: Yeferson Loaiza
"""
import re

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pprint
import pandas as pd
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.work_item_tracking.models import JsonPatchOperation

# Configura los detalles de autenticación
organizacion = 'Name Organization'
personal_access_token = 'Token'#all acces token 
organization_url = f'https://dev.azure.com/{organizacion}'
project_name = 'ProjecName'

# Crea la instancia de la conexión
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Crea el cliente de trabajo
work_client = connection.clients.get_work_client()
core_client = connection.clients.get_core_client()
get_projects_response = core_client.get_projects()
wit_client = connection.clients.get_work_item_tracking_client()

# Obtiene las tareas del proyecto
query = {
    'query': f"SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo] FROM workitems WHERE [System.WorkItemType] = 'Task' OR [System.WorkItemType] = 'User Story' AND [System.TeamProject] = '{project_name}'",
    'api-version': '6.0'
}

tasks = wit_client.query_by_wiql(query).work_items
work_item_references = wit_client.query_by_wiql(query).work_items

Id = []
Titulo = []
Estado = []
Asignado = []
Descripcion = []
Organizacion = []
Proyecto = []

x = work_item_references[7]

work_item_id = x.id

# Obtener el work item completo
work_item = wit_client.get_work_item(id=work_item_id)

# Imprimir toda la información del work item
print('ID:', work_item.id)
print('Título:', work_item.fields['System.Title'])
print('Estado:', work_item.fields['System.State'])
print('Asignado a:', work_item.fields['System.AssignedTo'])
# Imprimir otras propiedades y campos según sea necesario

# Imprimir todos los campos del work item
for field_name, field_value in work_item.fields.items():
    print(field_name, ':', field_value)



#ciclo donde recorre los items de trabajo
for work_item_reference in work_item_references:
    work_item_id = work_item_reference.id
    work_item = wit_client.get_work_item(id=work_item_id)
    titulo = work_item.fields['System.Title']
    estado = work_item.fields['System.State']
    print('ID:', work_item.id)
    print('Título:', titulo)
    print('Estado:', estado)
    try:
        asignado = work_item.fields['System.AssignedTo']
        asigned = asignado['displayName']
        print('------------------------')
        print('Asignado a:',asigned)
        print('------------------------')
        pass
    except Exception:
        print('------------------------')
        print('Asignado a: nadie')
        print('------------------------')
        pass
    try:
        descripcion = work_item.fields['System.Description']
        description = descripcion.replace('<div>','').replace('</div>','')
        print('Descripcion:', description)
        pass
    except Exception:
        print('Descripcion: no hay')
        pass
    Id.append(work_item_id)
    Titulo.append(titulo)
    Estado.append(estado)
    Asignado.append(asigned)
    Descripcion.append(description)
    Organizacion.append(organizacion)
    Proyecto.append(project_name)



reporte = pd.DataFrame({"Id":Id, "Titulo": Titulo,"Estado": Estado,"Asignado": Asignado,"Descripcion":Descripcion,"Organizacion":Organizacion,"Proyecto":Proyecto})

