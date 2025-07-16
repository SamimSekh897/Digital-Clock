"""A simple tkinter clock thst showa date + time. Sound plays only if the sound file exists and user leaves "sound ON". Compitable with playsound 1.2.2 (blocking call wrapped in a thread)"""
from time import strftime
import tkinter as tk
import threading
import os

try:
    from playsound import playsound
#pip install playsound 1.2.2
except ImportError:
    playsound=None
#Fallback if playsound


#Constants
WINDOW_TITLE="Digital Clock v3"
WINDOW_SIZE="450x230"
BG_COLOR="#000000"
DATE_BG="#222222"
DATE_FG="white"
TIME_FG="#FF0000"
SOUND_FILE="clockbeep.mp3"
#put your mp3/WAV in same folder
TICK_INTERVAL=1000 #milliseconds (=1sec)

#Helper functions
def safe_play_sound():
    '''Play the tick sound once(if enabled,file exists,playsound usable)'''
    if sound_state["on"] and playsound and os.path.exists(SOUND_FILE):
        threading.Thread(target=lambda:playsound(SOUND_FILE),daemon=True).start()

def update_clock():
    """Resfresh the labels every second."""
    date_string=strftime("%d %B %Y - %A")
    time_string=strftime("%I:%M:%S %p") #12-hour clock,swap %H for 24-hour

    date_label.config(text=date_string)
    time_label.config(text=time_string)

    safe_play_sound()
    root.after(TICK_INTERVAL,update_clock)

def toggle_sound():
    """Flip the global sound flag and update button text."""
    sound_state["on"] = not sound_state["on"]
    btn_sound.config(text=f"Sound: {'on' if sound_state['on'] else 'OFF'}")

theme={"dark":True}

def toggle_theme():
    if theme["dark"]:
        #Switch to light mode
        root.config(bg="white")
        date_label.config(bg="white",fg="black")
        time_label.config(bg="white",fg="black")
        btn_sound.config(bg="#ddd",fg="black")
        btn_theme.config(text="Switch to Dark Mode",bg="#dddddd",fg="black")
    else:
        #Switch to dark mode
        root.config(bg="#121212")
        date_label.config(bg="#121212",fg="white")
        time_label.config(bg="#121212",fg="#FF0000")
        btn_sound.config(bg="#333333",fg="white")
        btn_theme.config(text="Switch to Light Mode",bg="#333333",fg="white")

    theme["dark"]=not theme["dark"]

#GUI setup

root=tk.Tk()
root.title(WINDOW_TITLE)
root.geometry(WINDOW_SIZE)
root.config(bg=BG_COLOR)

#Date label
date_label=tk.Label(root,font=("consolas",20),fg=DATE_FG,bg=DATE_BG)
date_label.pack(pady=(25,5))

#Time label
time_label=tk.Label(root,font=("DS-Digital",60,"bold"),fg=TIME_FG,bg=BG_COLOR)
time_label.pack(expand=True)

#Sound toggle button
sound_state={"on":True} #mutable container so inner funcs can modify
btn_sound=tk.Button(root,text="Sound:ON",command=toggle_sound,bg="#444444",fg="white",width=10)
btn_sound.pack(pady=(10,5))

#Dark mode toggle button
btn_theme=tk.Button(root,text="Switch to Light Mode",command=toggle_theme,bg="#333333",fg="white")
btn_theme.pack(pady=(0,10))

#kick-off + mainloop
update_clock()
root.mainloop()