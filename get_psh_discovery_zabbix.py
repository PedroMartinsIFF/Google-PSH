#!/usr/bin/python3

# listando todos os eventos
# python3 get_psh.py event_list 

# Detalhes de um evento em especifico usando nome completo do resultado anterior
# python3 get_psh.py event_detail 
# pip3 install google.auth
import requests
import json
from google.auth import jwt
from dateutil.parser import isoparse
import sys
import re

opcao = sys.argv[1]
project_id = sys.argv[2]
#Key file
credentials_file = ''
with open(credentials_file) as file:
    credentials_data = json.load(file)
audience = 'https://servicehealth.googleapis.com/'
credentials = jwt.Credentials.from_service_account_info(credentials_data, audience=audience)
request = requests.Request()
credentials.refresh(request)
access_token = credentials.token
page_token = "&page_token="
headers = {
        'Authorization': 'Bearer ' + access_token.decode("utf-8"),
        'Content-Type': 'application/json'
    }

if opcao == "event_list":
    result = '{ "data": ['
    while page_token != "":
        listar_eventos = "https://servicehealth.googleapis.com/v1alpha/projects/"+project_id+"/locations/global/events?page_size=100"+page_token
        event_list = requests.get(url=listar_eventos, headers=headers, verify=True)
        data = json.loads(event_list.text)
        if "nextPageToken" in data:
            page_token = "&page_token="+data['nextPageToken']
        else:
            page_token = ""
        if not data:
            page_token = ""
        else:
            for i in data['events']:
                name_completo = i['name'].strip()
                resultado = re.search(r'[^/]+$', name_completo)
                if resultado:
                    name = resultado.group(0)
                title = i['title'].strip()
                new_line = '{"{#EVENTID}":"'+ str(name)+ '", "{#TITLE}":"'+ str(title)+ '"}'
                result = result + new_line
                result = result + ","
    result = result+ ']}'
    result = result.replace(",]}","]}")
    print(result)

if opcao == "event_detail":
    result = '{ "data": ['
    event_id =sys.argv[3]
    detalhar_evento = "https://servicehealth.googleapis.com/v1alpha/projects/"+project_id+"/locations/global/events/"+event_id
    event_detail = requests.get(url=detalhar_evento, headers=headers, verify=True)
    data = json.loads(event_detail.text)
    title = data['title'].strip()
    category = data['category'].strip()
    state = data['state'].strip()
    services = data['services']
    total_elementos = len(services)
    elementos_atual = 1
    result_service = ""
    for i in services:
        service = i['serviceName']
        result_service = result_service + service
        if elementos_atual < total_elementos:
            result_service = result_service + ", "
        elementos_atual = elementos_atual + 1
    services = result_service
    if "startTime" in data:
        startTime = data['startTime']
        startTime = int(isoparse(startTime).timestamp())
    else:
        startTime = 0

    if "endTime" in data:
        endTime = data['endTime']
        endTime = int(isoparse(endTime).timestamp())
    else:
        endTime = 0

    if "updateTime" in data:
        updateTime = data['updateTime']
        updateTime = int(isoparse(updateTime).timestamp())
    else:
        updateTime = 0

    if "nextUpdateTime" in data:
        nextUpdateTime = data['nextUpdateTime']
        nextUpdateTime = int(isoparse(nextUpdateTime).timestamp())
    else:
        nextUpdateTime = 0
    new_line = '{ "data": [{"EVENTID":"'+ str(event_id)+ '","TITLE":"'+ str(title)+ '", "CATEGORY":"'+ str(category)+ '", "STATE":"'+ str(state)+ '", "UPDATETIME":'+ str(updateTime)+ ', "STARTTIME":'+ str(startTime)+ ', "ENDTIME":'+ str(endTime)+ ', "NEXTUPDATETIME":'+ str(nextUpdateTime)+ ', "SERVICES":"'+ str(services)+ '"}]}'
    print(new_line)