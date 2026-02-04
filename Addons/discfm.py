import requests
import time
from pystray import Icon, Menu, MenuItem

def run(*args):
    icon = args[2]
    url = 'http://127.0.0.1:5000/notify'
    data = {'content': "balls"}
    response = requests.post(url, data=data)


    baseuserdata = []
    index = 0
    scanfirst = True
    scanindex = 0
    while not args[0].is_set():
        if index == 0:
            response = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={"authorization": args[1]})
            friends_json = response.json()
            for f in friends_json: print(f["user"]["username"])
            index += 1

        scanindex = 0
        for friend_json in friends_json:
            response2 = requests.get(f"https://discord.com/api/v9/users/{friend_json["user"]["id"]}/profile", headers={"authorization": args[1]})
            if response2.status_code != 200: 
                time.sleep(6)
                response2 = requests.get(f"https://discord.com/api/v9/users/{friend_json["user"]["id"]}/profile", headers={"authorization": args[1]})
                if response2.status_code != 200:
                    continue

            friend = response2.json()["user"]
            if scanfirst:
                baseuserdata.append(friend)
            if not scanfirst:
                if friend != baseuserdata[scanindex]:
                    icon.notify(f"{friend["global_name"]} has Changed their Profile")
                    requests.post("https://discord.com/api/webhooks/1465426251253809162/qmL1RfU4-4Oc6YjkU01ufbUb5LyqHlWk0r9I6xoFy0slxCYNUTPfcKt-y0hwZ4Q4NAmN", headers={"authorization": args[1]}, data={"content": f"Profile Change Detected for {friend["global_name"]}"})
                    baseuserdata.pop(scanindex)
                    baseuserdata.insert(scanindex, friend)
            scanindex += 1
            time.sleep(4)
        
        if scanfirst:
            icon.notify("Base Data Scan Complete, Profile change alerts active.")
        scanfirst = False
        
        time.sleep(30)

        if index > 3:
            index = 0