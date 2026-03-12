import mido
import subprocess
import sys
import os
import time

def run(*args):
    bbreak = False
    with mido.open_input("MIDI function 0") as port:
        print("Listening for MIDI messages...")
        for msg in port:
            msg: mido.Message
            match msg.dict()["control"]:
                case 1:
                    subprocess.Popen(
                        [sys.executable, "Addons/ytdownloader.py"],
                        creationflags=subprocess.CREATE_NO_WINDOW)
                case 2:
                    subprocess.Popen(
                        [sys.executable, "Addons/msgloaderopener.py"],
                        creationflags=subprocess.CREATE_NO_WINDOW)
                case 3:
                    os.startfile(r"C:\Users\Ri\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Spotify.lnk")

                case 4:
                    os.startfile(r"C:\Users\Ri\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\OBS Studio.lnk")
                
                case 5:
                    os.startfile(r"C:\Users\Ri\Documents\dc\DiscordChatExporter.exe")

                case 6:
                    os.startfile(r"C:\Program Files (x86)\Steam\steamapps\common\Half Sword Demo\HalfSwordUE5.exe")