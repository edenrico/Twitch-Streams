import requests
import pandas as pd
from datetime import datetime, timezone
import os

LANGUAGES = ["pt", "en", "es"]
LIMIT = 100

def _mask(value: str, prefix: int = 6) -> str:
    if not value:
        return "None"
    return value[:prefix] + "..." + value[-4:]

def _creds():
    return os.getenv("CLIENT_ID"), os.getenv("ACCESS_TOKEN")

def get_streams(language):
    client_id, access_token = _creds()
    print(
        f"[DEBUG] Preparando request para language={language}, client_id={_mask(client_id)}, "
        f"token={_mask(access_token)}"
    )

    if not client_id or not access_token:
        print("[ERRO] CLIENT_ID ou ACCESS_TOKEN nao configurados. Abortando chamada para Twitch.")
        return []

    url = f"https://api.twitch.tv/helix/streams?first={LIMIT}&language={language}"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erro {response.status_code}: {response.text}")
        return []
    return response.json().get("data", [])

def collect_all_streams():
    client_id, access_token = _creds()
    print(
        f"[DEBUG] Inicio da coleta. LANGUAGES={LANGUAGES}, client_id={_mask(client_id)}, "
        f"token={_mask(access_token)}"
    )
    all_streams = []
    for lang in LANGUAGES:
        streams = get_streams(lang)
        for s in streams:
            started = datetime.fromisoformat(s["started_at"].replace("Z", "+00:00"))
            duration_min = (datetime.now(timezone.utc) - started).total_seconds() / 60
            all_streams.append({
                "streamer": s["user_name"],
                "categoria": s["game_name"],
                "idioma": s["language"],
                "viewers": s["viewer_count"],
                "inicio": s["started_at"],
                "duracao_min": round(duration_min, 1),
                "hora": started.hour,
                "dia_semana": started.strftime("%A"),
                "user_id": s.get("user_id"),       
                "game_id": s.get("game_id"),       
                "is_mature": s.get("is_mature"),   
                "tags": s.get("tags", [])
            })
    print(f"Total de streams coletadas: {len(all_streams)}")
    return pd.DataFrame(all_streams)
