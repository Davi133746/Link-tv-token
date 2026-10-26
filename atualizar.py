# Instala a biblioteca necessária na nuvem do Google
!pip install -q requests

import re
import requests
import time
import base64

# CONFIGURAÇÕES - PREENCHA AQUI:
URL_FONTE = "https://horizon.globo.com/auth-session/activity/webmedia/watchlive?video_session_id=ef7cc1f1-65f1-0a71-b020-1cd85f716d6e&autoPlayAvailable=true&playback_id=4452349&subscriber_only=true&title=Agora%20na%20Globo&program=Program%20%5BRede%20Globo%20(196)%20-%20Fant%C3%A1stico%20(814)%3A%2025%20de%20out.%2C%2017%3A00%3A00%20-%2025%20de%20out.%2C%2023%3A34%3A59%5D&channel=Rede%20Globo&kind=live&experiment_1=default&wroom=0&dvr=0&player_id=4f95a697-2c00-dc60-2254-7d337172ecea&browser=Chrome83&object=video%3A4452349&playback=hls&player_type=android&platform=web-android&url=https%3A%2F%2Fgloboplay.globo.com%2Ftv-globo%2Fao-vivo%2F6120663%2F&domain=globoplay&cdn=googlemedia&player_version=7.191.0&api_version=5.11.0&tenant=unknown&btime=0&n=10&signal=globo-rj&started_at=1792969212630&avg_bitrate=4385000&session_time=239000&watch_time=212188&startup_time=2780&nominal_bitrate=4385000"
USUARIO_GITHUB = "davi133746"
REPOSITORIO_GITHUB = "Link-tv-token"
TOKEN_GITHUB = "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"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
    "Referer": "https://globo.com",
    "Origin": "https://globo.com"
}

def atualizar_no_github(link_m3u8):
    url_api = f"https://api.github.com/repos/{USUARIO_GITHUB}/{REPOSITORIO_GITHUB}/contents/lista.m3u"
    headers_git = {
        "Authorization": f"token {TOKEN_GITHUB}",
        "Accept": "application/vnd.github.v3+json"
    }

    r_check = requests.get(url_api, headers=headers_git)
    sha = r_check.json().get("sha") if r_check.status_code == 200 else None

    conteudo = f"#EXTM3U\n#EXTINF:-1,Canal Atualizado\n{link_m3u8}\n"
    conteudo_base64 = base64.b64encode(conteudo.encode('utf-8')).decode('utf-8')

    dados = {
        "message": "Lista atualizada via Google Colab",
        "content": conteudo_base64
    }
    if sha:
        dados["sha"] = sha

    r_put = requests.put(url_api, headers=headers_git, json=dados)
    if r_put.status_code in [200, 201]:
        print("[+] GitHub atualizado com sucesso!")
    else:
        print("[-] Erro ao atualizar o GitHub:", r_put.text)

# Loop para o navegador ficar atualizando sozinho na nuvem
while True:
    try:
        print("[*] Buscando novo token...")
        r = requests.get(URL_FONTE, headers=HEADERS, timeout=10)

        padrao = r'https://[a-zA-Z0-9.-]+\.video\.globo\.com/j/ey[^"\s\']+'
        match = re.search(padrao, r.text)

        link = match.group(0) if match else None

        if link:
            print("[+] Link obtido!")
            atualizar_no_github(link)
        else:
            print("[-] Não foi possível extrair o link.")

    except Exception as e:
        print(f"[-] Erro: {e}")

    print("[*] Aguardando 1 hora para a próxima atualização...")
    time.sleep(3600)
