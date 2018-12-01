# -*- coding: utf-8 -*-
"""
Scrapper para buscar informações de processos da Giustizia Civile

Você vai precisar de um UUID válido e um Token.
Para conseguir os mesmo, você deve instalar o aplicativo em um device real
e capturar estas informações através de um MITM, eu usei o https://mitmproxy.org/ pois é simples e free.

Atenção! Não faça muitas requisições em pouco tempo, isso vai bloquear o seu UUID/token e IP.
Além disso, não seria bom perder este acesso por uso maldoso. Faça um bom uso.
"""
import json
import os
import time

from progress.bar import Bar

from lib.giustizia import get_case_details
from lib.ranges import load_ids_from_json

INITIAL_ID = 0
FINAL_ID = 60000
RANGE_YEAR = 2018

query_range = {RANGE_YEAR: range(INITIAL_ID, FINAL_ID, 1)}

if os.path.exists("json_results.txt"):
    loaded_json = load_ids_from_json("json_results.txt")
    query_range = loaded_json if loaded_json else query_range

json_results = open("json_results.txt", "w+")
csv_results = open("csv_results.csv", "w+")

for year in query_range:
    print("Querying cases from year {}".format(year))

    for process_id in Bar(
            'Querying', suffix='%(percent).1f%% - %(eta)ds'
    ).iter(query_range[year]):
        case = get_case_details(year, process_id)

        if case:
            print(" - {}".format(case))
            json_results.write(json.dumps(case.asdict()))
            csv_results.write(str(case))
            json_results.write("\n")
            csv_results.write("\n")
            json_results.flush()
            csv_results.flush()

        time.sleep(5)  # previne se bloqueado por DOS
#
json_results.close()
csv_results.close()
