import json

import requests

def search_for_mod(mod_name, version, loader):
    url = "https://api.modrinth.com/search"
    params = {
        "query": mod_name,
        "facets": json.dumps([
            ["categories:" + loader],
            ["versions:" + version],
            ["project_type: mod"]
        ]),
        "index": "relevance",
        "limit": 1,
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Auto Mod Downloader"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None