# -*- coding: utf-8 -*-
"""
Scrapper para buscar informações de processos da Giustizia Civile

Você vai precisar de um UUID válido e um Token.
Para conseguir os mesmo, você deve instalar o aplicativo em um device real
e capturar estas informações através de um MITM, eu usei o https://mitmproxy.org/ pois é simples e free.

Atenção! Não faça muitas requisições em pouco tempo, isso vai bloquear o seu UUID/token e IP.
Além disso, não seria bom perder este acesso por uso maldoso. Faça um bom uso.
"""
import os
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

inscrito_ruolo_re = re.compile("\<li\>iscritto al ruolo il (.+)\<\/li\>")

INITIAL_ID = 46626
FINAL_ID = 52000
YEAR = 2018

payload = dict(
    version="1.1.13",
    platform="iOS 12.0",
    uuid="DEVICE UUID",
    devicename="iPhone6,2",
    devicewidth=320,
    deviceheight=568,
    token="TOKEN",
    azione="direttarg_sicid_mobile",
    registro="CC",
    idufficio="0580910098",
    aaproc=YEAR,
    tipoufficio=1
)

resultados = open("resultados.txt", "w+")

processos = range(INITIAL_ID, FINAL_ID, 1)

if os.path.exists("cidadanias.txt"):
    cidadanias = open("cidadanias.txt")
    processos = cidadanias.read().split("\n")

for process_id in processos:
    process_id = str(process_id)

    payload.update(dict(
        numproc=process_id,
        _=int(datetime.now().timestamp())       # este parâmetro é o tipespam, tem que ser diferente para cada request
    ))
    response = requests.get("https://mob1.processotelematico.giustizia.it/proxy/index_mobile.php", params=payload)
    content = response.text

    print ("Buscando %s" % process_id)
    if "cittadinanza" in content:

        bs = BeautifulSoup(content)
        nome_giudice = bs.find("nomegiudice")
        data_udienza = bs.find("dataudienza")

        inscrito_ruolo_search = inscrito_ruolo_re.search(content)
        if inscrito_ruolo_search:
            data_inscricao = inscrito_ruolo_search.groups()[0]
        else:
            data_inscricao = "???"

        nome_giudice = nome_giudice.string if nome_giudice else "SEM JUIZ"
        data_udienza = data_udienza.string if data_udienza else "SEM DATA AUDIENCIA"

        row = ";".join([process_id, data_inscricao, nome_giudice, data_udienza])
        print(row)
        resultados.write(row)
        resultados.write("\n")
        resultados.flush()

    time.sleep(5)   # previne se bloqueado por DOS

resultados.close()
