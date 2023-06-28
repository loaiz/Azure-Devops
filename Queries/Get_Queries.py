"""
Created on Tue Jun 27 07:23:01 2023

@author: Yeferson Loaiza
"""

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# Configurar los detalles de autenticación
# organization_url = "https://dev.azure.com/{organizacion}"
# personal_access_token = "{personal_access_token}"

# Configura los detalles de autenticación
organizacion = 'Name Organization'
personal_access_token = 'Token'#all acces token 
organization_url = f'https://dev.azure.com/{organizacion}'
project_name = 'ProjecName'


# Crear la instancia de la conexión
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Obtener el cliente de seguimiento de elementos de trabajo
wit_client = connection.clients.get_work_item_tracking_client()

# Definir el ID de la consulta en Azure DevOps
query_id = "query id"

# Obtener los detalles de la consulta
query_result = wit_client.query_by_id(query_id)

# Obtener las columnas de la consulta
columns = query_result.columns


for field in columns:
    print(field.reference_name, ':', field.name)

for column in columns:
    field = wit_client.get_field(column.reference_name)
    print("Nombre de la columna:", column.name)
    print("Referencia de campo:", column.reference_name)
    # print("Tipo de campo:", column.type_name)
    print("Tipo de campo:", field.type)
    print("_____________________________")


work_item_ids = [work_item.id for work_item in query_result.work_items]

work_items = wit_client.get_work_items(ids=work_item_ids, expand='Relations')
for work_item in work_items:
    print("ID:", work_item.id)
    print("Título:", work_item.fields["System.Title"])
    print("Estado:", work_item.fields["System.State"])
    # print("Asignado a:", work_item.fields["System.AssignedTo"]["displayName"])
    print("Descripción:", work_item.fields.get("System.Description", ""))
    print(work_item.fields.get("System.Parent"))
    
