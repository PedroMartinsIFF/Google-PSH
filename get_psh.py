#!/usr/bin/python3

# listando todos os eventos
# python3 get_psh.py event_list key

# Detalhes de um evento em especifico usando nome completo do resultado anterior
# python3 get_psh.py event_detail    
import requests
import json
from google.auth import jwt 
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
        for i in data['events']:
            name_completo = i['name'].strip()
            resultado = re.search(r'[^/]+$', name_completo)
            if resultado:
                name = resultado.group(0)
            title = i['title'].strip()
            category = i['category'].strip()
            state = i['state'].strip()
            updateTime = i['updateTime']
            startTime = i['startTime']
            #endTime = i['endTime']

            new_line = '{"{#EVENTID}":"'+ str(name)+ '", "{#TITLE}":"'+ str(title)+ '", "{#CATEGORY}":"'+ str(category)+ '", "{#STATE}":"'+ str(state)+ '", "{#updateTime}":"'+ str(updateTime)+ '", "{#startTime}":"'+ str(startTime)+ '"}'
            result = result + new_line
            result = result + ","
            #print(name+" - "+state)
    result = result+ ']}'
    result = result.replace(",]}","]}")
    print(result)




if opcao == "event_detail":
    detalhar_evento = "https://servicehealth.googleapis.com/v1alpha/"+project_id
    event_detail = requests.get(url=detalhar_evento, headers=headers, verify=True)
    data = event_detail.json()
    print(data)
