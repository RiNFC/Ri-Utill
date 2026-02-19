import requests
import json
import time
import dotenv
import os


dotenv.load_dotenv()

def merge_every_25(lst):
    result = []
    for i in range(0, len(lst), 10):
        chunk = lst[i:i+10]
        merged = "\n".join(map(str, chunk))
        result.append(merged)
    return result


name = input("name: ")


with open("discord_messages.json", "r", encoding="utf8") as file:
    data = json.load(file)



def postwebhs(webhook: str):
    endstr = ""
    for msg in data["messages"]:
        endstr = endstr + f"{msg["author"]["name"]} {msg["timestamp"]}:  {msg["content"]}\n"


    for c in merge_every_25(endstr.split("\n")):
       requests.post(webhook, data={"content": c})
       time.sleep(5)


resp = requests.post("https://discord.com/api/v9/guilds/1452494902217805998/channels", json={"type":0,"name":name,"permission_overwrites":[],"parent_id":"1473513350087315592"}, headers={"authorization": os.getenv("mptoken")})

time.sleep(3)

datat = resp.json()

webhookdata = requests.post(f"https://discord.com/api/v9/channels/{datat["id"]}/webhooks", json={"name": name}, headers={"authorization": os.getenv("mptoken")}).json()

time.sleep(3)

webhookurl = webhookdata["url"]

postwebhs(webhook=webhookurl)





os.remove("discord_messages.json")
