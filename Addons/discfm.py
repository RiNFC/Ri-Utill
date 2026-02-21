import requests
import time
from Addons.notify import notify
import dotenv
import os

dotenv.load_dotenv()

def error_out():
    notify("Error Occured. Recommended Restart.", "Disc FM")


def compare_json(json1, json2):
    differences = []
    
    for key in json1.keys():
        if key in json2:
            if json1[key] != json2[key]:
                differences.append(key)
        else: differences.append(key)
    
    for key in json2.keys():
        if key not in json1:
            differences.append(key)
    
    return differences

class User():
    def __init__(self, display_name:str, username:str, bio:str, id:str, avatar_tag:str, banner_tag:str):
        self.display_name = display_name
        self.username = username
        self.bio = bio
        self.id = id
        self.avatar_tag = avatar_tag
        self.banner_tag = banner_tag

        self.json = {"display_name": display_name,
                     "username": username,
                     "bio": bio,
                     "id": id,
                     "avatar_tag": avatar_tag,
                     "banner_tag": banner_tag}
    
    def reload(self):
        response2 = requests.get(f"https://discord.com/api/v9/users/{self.id}/profile", headers={"authorization": os.getenv("disctoken")})
        try: resjson2 = response2.json()["user"]
        except: 
            return(False)

        self.display_name = resjson2["global_name"]
        self.username = resjson2["username"]
        self.bio = resjson2["bio"]
        self.id = resjson2["id"]
        self.avatar_tag = resjson2["avatar"]
        self.banner_tag = resjson2["banner"] if resjson2["banner"] is not None else resjson2["banner_color"]

        self.json = {"display_name": self.display_name,
                     "username": self.username,
                     "bio": self.bio,
                     "id": self.id,
                     "avatar_tag": self.avatar_tag,
                     "banner_tag": self.banner_tag}
        return(True)


        
def load_friends():
    friends = []
    response = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={"authorization": os.getenv("disctoken")})
    if response.status_code != 200:
        return(0)
    resjson = response.json()
    for usr in resjson:
        response2 = requests.get(f"https://discord.com/api/v9/users/{usr["id"]}/profile", headers={"authorization": os.getenv("disctoken")})
        if response2.status_code == 404:
            continue
        try: resjson2 = response2.json()["user"]
        except KeyError: continue
        user = User(
            resjson2["global_name"],
            resjson2["username"],
            resjson2["bio"],
            resjson2["id"],
            resjson2["avatar"],
            resjson2["banner"] if resjson2["banner"] is not None else resjson2["banner_color"]
        )
        friends.append(user)
        time.sleep(8)
    return(friends)


def run(*args):
    friends = load_friends()
    if friends == 0:
        print("1 point")
        error_out()
        return()

    notify("Friend List Loaded, Scanning Starting.", title="Disc FM")
    time.sleep(5)
    while not args[0].is_set():
        nfriends = []
        for friend in friends:
            friend : User
            friend_json = friend.json
            if not friend.reload():
                continue
            dif = compare_json(friend_json, friend.json)
            if len(dif) > 0:
                notify(f"{friend.display_name} has Changed the followings part of their Profile:\n{', '.join(dif)}", "Disc FM")
                requests.post(args[1], data={"content": f"{friend.display_name} Changed the following parts of their profile:\n{', '.join(dif)}"})
            nfriends.append(friend)
        
            time.sleep(8)
        
        friends = nfriends


    