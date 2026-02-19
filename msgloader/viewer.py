import json
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os



with open('discord_messages.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


root = tk.Tk()
root.title("Discord Messages Visualization")


root.geometry("600x400")


top_frame = ttk.Frame(root)
top_frame.pack(fill="x", padx=10, pady=5)


search_entry = ttk.Entry(top_frame, font=("Arial", 12))
search_entry.pack(fill="x", expand=True, side="left", padx=10)


def highlight_search():
    search_terms = search_entry.get().lower().split("-")
    if search_terms[len(search_terms)-1] == "": search_terms.pop(len(search_terms)-1)
    

    text_widget.tag_remove("highlight", "1.0", "end")
    
    if search_terms:
       
        for term in search_terms:
            start_pos = "1.0"
            while True:
               
                start_pos = text_widget.search(term, start_pos, nocase=True, stopindex="end")
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(term)}c"
                text_widget.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos

        text_widget.tag_configure("highlight", background="yellow", foreground="black")


search_entry.bind("<KeyRelease>", lambda event: highlight_search())


frame = ttk.Frame(root)
frame.pack(fill="both", expand=True)


text_widget = tk.Text(frame, wrap="word", font=("Arial", 10), state="normal", height=20, width=80)
text_widget.pack(side="left", fill="both", expand=True)


scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
scrollbar.pack(side="right", fill="y")


text_widget.configure(yscrollcommand=scrollbar.set)


for message in data['messages']:
    author = message['author']['name']
    timestamp = message['timestamp']
    content = message['content']
    timestamp = datetime.fromisoformat(timestamp[:-6]).strftime('%Y-%m-%d %H:%M:%S')

    full_message = f"{timestamp} - {author}: {content}\n"

    text_widget.insert(tk.END, full_message)


text_widget.config(state="disabled")


root.mainloop()

os.remove("discord_messages.json")