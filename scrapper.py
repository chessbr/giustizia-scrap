import requests
import time
from datetime import datetime
import os

INITIAL_ID = 45000
FINAL_ID = 52000
YEAR = 2018

payload = dict(
    version="1.1.13",
    platform="iOS 12.0",
    uuid="UUID DO DEVICE AQUI AQUI",
    devicename="iPhone6,2",
    devicewidth=320,
    deviceheight=568,
    token="TOKEN AQUI",
    azione="direttarg_sicid_mobile",
    registro="CC",
    idufficio="0580910098",
    aaproc=YEAR,
    tipoufficio=1
)

for process_id in range(INITIAL_ID, FINAL_ID, 1):
    payload.update(dict(
        numproc=process_id,
        _=int(datetime.now().timestamp())
    ))
    response = requests.get("https://mob1.processotelematico.giustizia.it/proxy/index_mobile.php", params=payload)
    content = response.text

    print ("Buscando %d" % process_id)
    if "cittadinanza" in content:
        print("%s eh um processo de cidadania" % process_id)

        if "creaEventoCalendarioIos" in content:
            print("\tTem data de audiencia")

    time.sleep(5)   # previne se bloqueado por DOS
