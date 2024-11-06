import tkinter as tk
from ui import ModDownloaderUI
import process

VERSIONS = process.get_minecraft_versions()
LOADERS = ["fabric", "forge", "neoforge"]

def perform_download(inputs):
    app.update_status("Preparing download...")
    failed_mods = []

    for mod in inputs["mods"]:
        mod = mod.strip()
        mod = mod.toLowerCase()

        app.update_status(f"Searching {mod} @ {inputs['version']} for {inputs['loader']}...")

        search_response = process.search_for_mod(mod)

        if not search_response:
            app.update_status(f"Mod {mod} not found.")
            failed_mods.append(mod)
            continue

        if not search_response["game_versions"] or inputs["version"] not in search_response["game_versions"]:
            app.update_status(f"Mod {mod} not available for version {inputs['version']}.")
            failed_mods.append(mod)
            continue

        if not search_response["loaders"] or inputs["loader"] not in search_response["loaders"]:
            app.update_status(f"Mod {mod} not available for loader {inputs['loader']}.")
            failed_mods.append(mod)
            continue

        mod_version = process.get_mod_version(mod, inputs["loader"], inputs["version"])

        app.update_status(f"Found! Downloading {mod} ({mod_version['name']})...")

        success = process.download_mod(mod_version, inputs["download_path"])

        if not success:
            app.update_status(f"Failed to download {mod} ({mod_version['name']}).")
            failed_mods.append(mod)
            continue

        app.update_status(f"Downloaded {mod} ({mod_version['name']}).")

    app.update_status("Downloads complete.")
    if failed_mods:
        app.update_status(f"Failed to download: {', '.join(failed_mods)}")

root = tk.Tk()
app = ModDownloaderUI(root, versions=VERSIONS, loaders=LOADERS, on_download_callback=perform_download)
root.mainloop()