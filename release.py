import os
import requests
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

r = requests.get("https://api.github.com/repos/madisvain/requestbin/releases/latest")
assets = r.json()["assets"]

if len(assets) > 0:
    dist = next(asset for asset in assets if asset["name"] == "web.zip")

    r = requests.get(dist["browser_download_url"], stream=True)
    with open("web.zip", "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    z = zipfile.ZipFile("web.zip")
    print(os.path.join(BASE_DIR, "requestbin", "web"))
    z.extractall(os.path.join(BASE_DIR, "requestbin", "web"))

    os.remove("web.zip")
