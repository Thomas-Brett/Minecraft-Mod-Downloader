from datetime import datetime

import requests

def search_for_mod(mod_name):
    url = f"https://api.modrinth.com/v2/project/{mod_name}"

    headers = {
        "User-Agent": "Auto Mod Downloader"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.HTTPError as e:
        return False

def get_mod_version(mod_name, loader, version):
    url = f'https://api.modrinth.com/v2/project/{mod_name}/version?game_versions=["{version}"]&loaders=["{loader}"]'

    headers = {
        "User-Agent": "Auto Mod Downloader"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        versions = response.json()

        if len(versions) == 0:
            return None
        if len(versions) == 1:
            return versions[0]

        for version in versions:
            if version["version_type"] == "release":
                return version

        return max(versions, key=lambda x: datetime.fromisoformat(x['date_published'].replace("Z", "+00:00")))
    except requests.HTTPError as e:
        print(e)
        return False

def download_mod(mod_version, path):
    try:
        response = requests.get(mod_version["files"][0]["url"], stream=True)
        response.raise_for_status()

        with open(f"{path}/{mod_version['files'][0]['filename']}", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return True
    except requests.HTTPError as e:
        return False

def get_minecraft_versions():
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        versions = response.json()

        version_list = []

        for version in versions["versions"]:
            if version["type"] == "release":
                version_list.append(version["id"])

        return version_list
    except requests.HTTPError as e:
        return ["Could not fetch versions"]