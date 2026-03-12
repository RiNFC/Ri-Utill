import time
import discord
import threading
import json
import pypresence
from pypresence import DiscordNotFound
import dotenv
import os


dotenv.load_dotenv()

client = discord.Client()

currently_in_voice_channel = False
timeinvc = 0
msgcount = 0
tstart = 0

if os.path.exists(".data"):
    with open(".data", "r") as f:
        data = json.load(f)
        timeinvc = data.get("timeinvc", 0)
        msgcount = data.get("msgcount", 0)
    os.remove(".data")


def rpc():
    global tstart
    global timeinvc
    global msgcount

    st = int(time.time())
    rpc = pypresence.Presence("1428085437213179954", pipe=0)
    rpc.connect()

    while True:
        try:
            rpc.update(
                state=f"{msgcount} messages sent today.",
                details=f"{timeinvc // 3600}h {(timeinvc % 3600) // 60}m {timeinvc % 60}s in VC Today.",
                small_image="bug",
                small_text="Drawn by Bug.",
                large_image="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXRyb2h0ZDJjczE5NWl4YWx6YWZ1MWJrZW5tcnFodXozdTlnbmxzbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/a0qcvETjmcHF1O1P9t/giphy.gif",
                large_text="W.O.P.R. is thinking all the time.",
                large_url="https://en.wikipedia.org/wiki/WarGames",
                start=st,
                buttons=[{
                        "label": "VRChat",
                        "url": "https://vrchat.com/home/user/usr_bd418c2c-216e-40cf-b072-26574d66f065"},

                        {"label": "null",
                        "url": "https://ri-rye.xyz"}])

        except DiscordNotFound:
            print("Discord closed. Waiting 60 seconds before reconnect...")
            time.sleep(60)

        time.sleep(5)

def cnt():
    global timeinvc
    global msgcount
    while True:
        if currently_in_voice_channel:
            timeinvc += 1
        if time.localtime().tm_hour == 0 and time.localtime().tm_min == 0:
            timeinvc = 0
            msgcount = 0
        time.sleep(1)


rpc_thread = threading.Thread(target=rpc)
cnt_thread = threading.Thread(target=cnt)

@client.event
async def on_ready():
    rpc_thread.start()
    cnt_thread.start()



@client.event
async def on_voice_state_update(member, before, after):
    global currently_in_voice_channel
    global vcstarttime
    global timeinvc
    if member.id == 263419445022687232:
        if after.channel is not None:
            currently_in_voice_channel = True
        else:
            currently_in_voice_channel = False


@client.event
async def on_message(message):
    global msgcount
    if message.author == client.user:
        msgcount += 1




def run(*args):
    global tstart
    tstart = args[1]
    client.run(os.getenv('disctoken'), reconnect=True)