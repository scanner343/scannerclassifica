import os
import json
import requests
import time
import plistlib
# --- 🛠️ CAMBIA L'IMPORT CON IL NOME DEL TUO CLIENT ---
from client_343 import RePanzaClient 

def run_scanner():
    EMAIL = os.getenv("LK_EMAIL")
    PASSWORD = os.getenv("LK_PASSWORD")
    
    client = RePanzaClient.auto_login(EMAIL, PASSWORD)
    if not client: return

    session = requests.Session()
    for cookie in client.cookies: session.cookies.set(cookie['name'], cookie['value'])
    session.headers.update({
        'User-Agent': client.user_agent, 'Accept': 'application/x-bplist',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.lordsandknights.com', 'Referer': 'https://www.lordsandknights.com/'
    })

    # --- 🛠️ PARAMETRI MONDO DA MODIFICARE ---
    # URL preso dal CURL (attenzione al RE-IT-X)
    url_ranking = "https://backend2.lordsandknights.com/XYRALITY/WebObjects/LKWorldServer-RE-IT-7.woa/wa/QueryAction/playerRanks"
    WORLD_ID = '343'
    FILE_NAME = "database_classificamondo343.json"
    # ----------------------------------------
    
    all_players = []
    offset = 0; step = 100
    print(f"🚀 Avvio Scansione Classifica {WORLD_ID}...")

    while True:
        try:
            payload = {'offset': str(offset), 'limit': str(step), 'type': '(player_rank)', 'sortBy': '(row.asc)', 'worldId': WORLD_ID}
            response = session.post(url_ranking, data=payload, timeout=30)
            if response.status_code != 200: break
            
            try: data = plistlib.loads(response.content)
            except: break

            players = data.get('playerRanks', [])
            if not players: players = data.get('rows', [])
            if not players: break
            
            all_players.extend(players)
            print(f"📥 Scaricati {len(all_players)} giocatori...")
            if len(players) < step: break
            offset += step
            time.sleep(0.5)
        except: break

    if all_players:
        clean_data = []
        for p in all_players:
            clean_p = {k: (str(v) if not isinstance(v, (str, int, float, bool, list, dict, type(None))) else v) for k, v in p.items()}
            clean_data.append(clean_p)

        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(clean_data, f, indent=4, ensure_ascii=False)
        
        msg = f"✅ Classifica Mondo {WORLD_ID} Aggiornata: {len(clean_data)} giocatori."
        print(msg)
        RePanzaClient.send_telegram_alert(msg)

if __name__ == "__main__":
    run_scanner()
