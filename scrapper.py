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
import time
import json
from lib.giustizia import get_case_details
from progress.bar import Bar

INITIAL_ID = 40000
FINAL_ID = 50000
YEAR = 2018

json_results = open("json_results.txt", "w+")
csv_results = open("csv_results.csv", "w+")

query_range = range(INITIAL_ID, FINAL_ID, 1)

if os.path.exists("cidadanias.txt"):
    cidadanias = open("cidadanias.txt")
    query_range = cidadanias.read().split("\n")

for process_id in Bar(
        'Querying', suffix='%(percent).1f%% - %(eta)ds'
).iter(query_range):
    case = get_case_details(YEAR, process_id)

    if case:
        print(" - \t{}".format(case))
        json_results.write(json.dumps(case.asdict()))
        csv_results.write(str(case))
        json_results.write("\n")
        csv_results.write("\n")
        json_results.flush()
        csv_results.flush()

    time.sleep(5)  # previne se bloqueado por DOS

json_results.close()
csv_results.close()
