# -*- coding: utf-8 -*-
from datetime import datetime
import re

import requests
from bs4 import BeautifulSoup

from secrets import uuid, devicename, deviceheight, devicewidth, token

query_url = "https://mob1.processotelematico.giustizia.it/proxy/index_mobile.php"
base_payload = dict(
    version="1.1.13",
    platform="iOS 12.1",
    uuid=uuid,
    devicename=devicename,
    devicewidth=devicewidth,
    deviceheight=deviceheight,
    token=token,
    azione="direttarg_sicid_mobile",
    registro="CC",
    idufficio="0580910098",
    tipoufficio=1
)

inscrito_ruolo_re = re.compile("\<li\>iscritto al ruolo il (.+)\<\/li\>")


class Case:
    def __init__(self, case_yr, case_no, date_filed, judge_name, date_hearing):
        self.year = case_yr
        self.number = case_no
        self.date_filed = date_filed
        self.date_hearing = date_hearing
        self.judge_name = judge_name

    def __str__(self):
        return ";".join([
            '{}/{}'.format(self.number, self.year),
            self.date_filed,
            self.judge_name,
            self.date_hearing,
        ])

    def asdict(self):
        return {
            'case_yr': self.year,
            'case_no': self.number,
            'date_filed': self.date_filed,
            'date_hearing': self.date_hearing,
            'judge_name': self.judge_name,
        }


def get_case_details(case_yr, case_no):
    payload = base_payload.copy()

    payload.update(dict(
        aaproc=str(case_yr),
        numproc=str(case_no),
        _=int(datetime.now().timestamp())  # este parâmetro é o tipespam, tem que ser diferente para cada request
    ))

    response = requests.get(query_url, params=payload)
    content = response.text

    if "cittadinanza" in content:

        bs = BeautifulSoup(content)
        nome_giudice = bs.find("nomegiudice")
        data_udienza = bs.find("dataudienza")

        inscrito_ruolo_search = inscrito_ruolo_re.search(content)
        if inscrito_ruolo_search:
            data_inscricao = inscrito_ruolo_search.groups()[0]
        else:
            data_inscricao = "???"

        nome_giudice = nome_giudice.string if nome_giudice else "Not Assigned"
        data_udienza = data_udienza.string if data_udienza else "Not Assigned"

        return Case(
            case_yr,
            case_no,
            data_inscricao,
            nome_giudice,
            data_udienza
        )
