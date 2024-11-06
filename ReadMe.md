# Minecraft Mod Downloader

## Description
This simple python program allows you create a list of mods you want to download, then select a version and modloader, and have it query the modrinth API to attempt to download the correct version of the listed mods.

You can save the list of mods to a file, and load it later for quick and easy mod updates when you want to change versions.

## Usage

The name of the mod is the Modrinth ID of the mod that is found in the URL.
This is often the same as the mod name, but not always.
You can find this by going to the mod page on modrinth and looking at the URL.

1. Run the program
2. Import the CSV of mods, or manually add mods to the list
3. Select the version and modloader you want to download
4. Enter the path to when you want the downloads to go
5. Click download
6. Check the logs to see if there were any errors, it will tell you at the end.

If a mod failed, its likely because the mod author has not uploaded the mod to the version you selected. You can try a different version, or check the mod page to see if the version you want is available.