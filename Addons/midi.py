import mido
import subprocess
import sys

def run(*args):
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