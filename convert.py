import requests
import urllib.parse
import time
import os

SOURCE = "https://your-proxy.onrender.com/fetch?url=http://filex.homes/get.php?username=1month&password=1month&type=m3u_plus"
PROXY = "https://your-proxy.onrender.com/m3u8?url="

def fetch():
    for i in range(3):
        try:
            res = requests.get(SOURCE, timeout=15)
            if res.status_code == 200 and "#EXTM3U" in res.text:
                return res.text
        except:
            time.sleep(5)
    return None

data = fetch()

if not data:
    print("Using old playlist")
    exit()

lines = data.splitlines()
clean = ["#EXTM3U"]

for i in range(len(lines)):
    if lines[i].startswith("#EXTINF"):
        name = lines[i].split(",")[-1]
        stream = lines[i+1]

        encoded = urllib.parse.quote(stream, safe='')
        proxy_stream = PROXY + encoded

        clean.append(f'#EXTINF:-1,{name}')
        clean.append(proxy_stream)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(clean))

print("Done")
