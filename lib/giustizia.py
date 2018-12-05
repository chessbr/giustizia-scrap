# -*- coding: utf-8 -*-
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from secrets import (
    deviceheight, devicename, devicewidth, os_version, token,
    user_agent, uuid
)

QUERY_URL = "https://mob1.processotelematico.giustizia.it/proxy/index_mobile.php"
BASE_PAYLOAD = dict(
    version="1.1.13",
    platform=os_version,
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
HEADERS = {
    'User-Agent': user_agent
}

RE_INSCRITO_RUOLO = re.compile("\<li\>iscritto al ruolo il (.+)\<\/li\>")
RE_REMOVE_LAWYER_PREFIX = re.compile("(?<=Avv. ).*")


class Case:
    def __init__(self, case_yr, case_no, date_filed, judge_name, date_hearing, case_state, primary_lawyer_initials,
                 raw_case_content=None, judgement_number=None):
        self.year = case_yr
        self.number = case_no
        self.date_filed = date_filed
        self.date_hearing = date_hearing
        self.judge_name = judge_name
        self.case_state = case_state
        self.primary_lawyer_initials = primary_lawyer_initials
        self.raw_case_content = raw_case_content
        self.judgement_number = judgement_number

    def __str__(self):
        return ";".join([
            '{}/{}'.format(self.number, self.year),
            self.date_filed,
            self.judge_name,
            self.date_hearing,
            self.case_state,
            self.primary_lawyer_initials,
            self.judgement_number,
        ])

    def asdict(self):
        return {
            'case_yr': self.year,
            'case_no': self.number,
            'date_filed': self.date_filed,
            'date_hearing': self.date_hearing,
            'judge_name': self.judge_name,
            'case_state': self.case_state,
            'primary_lawyer_initials': self.primary_lawyer_initials,
            'judgement_number': self.judgement_number,
            'raw_case_content': self.raw_case_content,
        }


def get_case_details(case_yr, case_no):
    payload = BASE_PAYLOAD.copy()

    payload.update(dict(
        aaproc=str(case_yr),
        numproc=str(case_no),
        _=int(datetime.now().timestamp())
    ))

    response = requests.get(QUERY_URL, params=payload, headers=HEADERS)
    content = response.text

    if "Errore tecnico" in content:
        print("Request failed", content.text)
        raise Exception()

    if "cittadinanza" in content:
        bs = BeautifulSoup(content)
        nome_giudice = bs.find("nomegiudice")
        data_udienza = bs.find("dataudienza")

        inscrito_ruolo_search = RE_INSCRITO_RUOLO.search(content)
        if inscrito_ruolo_search:
            data_inscricao = inscrito_ruolo_search.groups()[0]
        else:
            data_inscricao = "???"

        case_state = extract_case_state_from_content(bs) or "Unknown"

        nome_giudice = nome_giudice.string if nome_giudice else "Not Assigned"
        data_udienza = data_udienza.string[:10] if data_udienza else "Not Assigned"

        primary_lawyer_initials = extract_primary_lawyer_initials(bs) or "Unknown"

        judgement_number = extract_judgement_number(bs)

        return Case(
            case_yr,
            case_no,
            data_inscricao,
            nome_giudice,
            data_udienza,
            case_state,
            primary_lawyer_initials,
            raw_case_content=content,
            judgement_number=judgement_number
        )


def extract_case_state_from_content(bs_content):
    try:
        case_state_list_copy = bs_content.findAll("li")
        for idx, val in enumerate(case_state_list_copy):
            if val.contents[0] == 'Stato fascicolo':
                return case_state_list_copy[idx + 1].contents[0]
        return None
    except:
        return None


def extract_primary_lawyer_initials(bs_content):
    try:
        case_state_list_copy = bs_content.findAll("li")
        for idx, val in enumerate(case_state_list_copy):
            if val.contents[0] == 'Parti fascicolo':
                redacted_name = RE_REMOVE_LAWYER_PREFIX.search(case_state_list_copy[idx + 1].contents[3]).group(0)
                return redacted_name.replace(' ', '').replace('*', '')
        return None
    except:
        return None


def extract_judgement_number(bs_content):
    try:
        li_entries = bs_content.findAll("li")
        for idx, val in enumerate(li_entries):
            if val.contents[0] == 'Sentenza definitiva':
                return li_entries[idx + 1].contents[0][4:]
        return None
    except:
        return None
