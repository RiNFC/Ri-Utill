import requests, re
import time
import pytube.download_helper as dh
import dotenv
import os
from urllib.parse import urlparse
import nextcord
from nextcord.ext import commands
from Addons.notify import notify

dotenv.load_dotenv()

client = commands.Bot()

@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.idle, activity=nextcord.Game("Monading on my Pleroma"))

#Thanks Stackoverflow
def check_youtube_url(url, timeout=5):
    try:
        if not all(urlparse(url)[:2]):
            return 3
    except:
        return 3

    m = re.search(r"(youtube\.com|youtu\.be)/(watch\?v=|embed/|shorts/)?([A-Za-z0-9_-]{11})", url)
    if not m:
        return 2

    try:
        r = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": f"https://www.youtube.com/watch?v={m.group(3)}"},
            timeout=timeout,
        )
        return 0 if r.status_code == 200 else 1
    except:
        return 1


@client.slash_command(description="Downloads Youtube Video")
async def downloadyt(interaction: nextcord.Interaction, url: str):
    errors = ["", "Invalid Youtube Video", "Not a Youtube Video URL", "Invalid URL"]
    c = check_youtube_url(url)
    if c == 0:
        msgt = await interaction.send("Downloading video...")
        try: dh.download_video(url)
        except KeyError: pass
        filepath = os.listdir("./videos")[0]
        await msgt.edit(file=nextcord.File(f"./videos/{filepath}"), content=f"Video Downloaded:\n{filepath}")
        notify(filepath, "Video Downloaded")
        os.remove(f"./videos/{filepath}")
    else: await interaction.send(f"Error:\n{errors[c]}")

def run(*args): 
    client.run(os.getenv("bottoken"), reconnect=True)
    notify("Error Occured Bot Runtime Ended", "Mr Sir")
    requests.post(os.getenv("uhohhook"), data={"content": f"Error Occured Bot Runtime Ended"})

