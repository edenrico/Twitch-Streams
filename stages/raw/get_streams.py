import requests
import pandas as pd
from datetime import datetime, timezone
import os

LANGUAGES = ["pt", "en", "es"]
LIMIT = 100
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")

def get_streams(language):
    url = f"https://api.twitch.tv/helix/streams?first={LIMIT}&language={language}"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erro {response.status_code}: {response.text}")
        return []
    return response.json().get("data", [])

def collect_all_streams():
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