from pynput.keyboard import Key, KeyCode, Listener
from tkinter import *
from tkinter import messagebox
from pystray import MenuItem as item
import pystray
from PIL import Image
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from playsound import playsound
from win10toast import ToastNotifier
import json


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
toaster = ToastNotifier()

# make a way to save your previous settings even after you exit


def execute():
    ismute = volume.GetMute()
    if ismute == 0:
        if notify == "True":
            toaster.show_toast("Noxu",
                               "Muted",
                               icon_path="./assets/mute.ico",
                               duration=2,
                               threaded=True,
                               sound=False)
        volume.SetMute(1, None)

    else:
        if notify == "True":
            toaster.show_toast("Noxu",
                               "Unmuted",
                               icon_path="./assets/mute.ico",
                               duration=2,
                               threaded=True,
                               sound=False)
        volume.SetMute(0, None)
        if sound == "True":
            playsound('./assets/unmute.mp3', block=False)


def quit_window(icon, item):
    icon.stop()
    ListenerPress.stop()
    window.iconify()
    window.after(1, lambda: window.destroy())


def show_window(icon, item):
    icon.stop()
    window.deiconify()
    window.after(1, lambda: window.focus_force())


def hide_window():
    window.withdraw()
    image = Image.open('./assets/mute.ico')
    menu = (item('Open', show_window), item('Settings', settingwindow), item('Quit', quit_window))
    icon = pystray.Icon("name", image, "Noxu", menu)
    icon.run_detached()


COMBINATIONS = [
    {Key.shift, KeyCode(vk=65)}  # shift + a (see below how to get vks)
]


# The currently pressed keys (initially empty)
pressed_vks = set()


def get_vk(key):
    """
    Get the virtual key code from a key.
    These are used so case/shift modifications are ignored.
    """
    return key.vk if hasattr(key, 'vk') else key.value.vk


def is_combination_pressed(combination):
    """ Check if a combination is satisfied using the keys pressed in pressed_vks """
    return all([get_vk(key) in pressed_vks for key in combination])


def on_press(key):
    """ When a key is pressed """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.add(vk)  # Add it to the set of currently pressed keys

    for combination in COMBINATIONS:  # Loop though each combination
        if is_combination_pressed(combination):  # And check if all keys are pressed
            execute()  # If they are all pressed, call your function
            break  # Don't allow execute to be called more than once per key press


def on_release(key):
    """ When a key is released """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.remove(vk)  # Remove it from the set of currently pressed keys


ListenerPress = Listener(on_press=on_press, on_release=on_release)


ListenerPress.start()

window = Tk()
window.maxsize(800, 500)
window.iconbitmap('./assets/mute.ico')
window.resizable(False, False)
window.config(bg="#FC4445")
window.title("Noxu")

jsonfile = open("./assets/data.json", "r", encoding="utf-8")
data = json.load(jsonfile)
jsonfile.close()

notifycheck = BooleanVar()
soundcheck = BooleanVar()
sound = data["Sounds"]
notify = data["Notifications"]


# Text
title = Label(window, text="Noxu")
title.config(background="#FC4445", font=("Courier", 15), fg="white")
title.place(relx=0.37, rely=0)
description = Label(window, text="Mute All Applications With\n One Press")
description.config(background="#FC4445", font=("Courier", 8), fg="white")
description.place(x=5, y=25)
shortcut = Label(window, text="Shift+A")
shortcut.config(background="#FC4445", font=("Courier", 11), fg="white")
shortcut.place(relx=0.33, rely=0.48)
info = Label(window, text="*Program will continue to\nrun in the background,\neven if closed")
info.config(background="#FC4445", font=("Courier", 8), fg="white")
info.place(x=5, y=150)


# Button
def aboutwindow():
    messagebox.showinfo("About", "Created By $ky\n2022 Copyright")


aboutImage = PhotoImage(file="./assets/about.png")
about = Button(window, image=aboutImage, command=aboutwindow)
about.config(background="#FC4445", font=("Courier", 8), bd=0, fg="blue", activebackground="#FC4445")
about.place(x=0, y=0)

run = 1


def updatingjson():
    global sound, notify
    sound = str(soundcheck.get())
    notify = str(notifycheck.get())
    data["Sounds"] = sound
    data["Notifications"] = notify
    with open('./assets/data.json', 'w') as f:
        json.dump(data, f)
        sound = data["Sounds"]
        notify = data["Notifications"]
        f.close()


def settingwindow():
    global notifycheck, soundcheck, run
    settingWindow = Toplevel(window)
    settingWindow.title("Settings")
    settingWindow.geometry("210x100")
    settingWindow.iconbitmap('./assets/mute.ico')
    settingWindow.resizable(False, False)
    settingWindow.config(bg="#FC4445")
    save = Button(settingWindow, text="Save", command=settingWindow.destroy)
    save.config(background="#FC4445", font=("Courier", 10), fg="white", relief=None, bd=0, activebackground="#FC4445",
                activeforeground="white")
    save.place(relx=0.4, y=75)
    settingnoti = Checkbutton(settingWindow, text="Notification", variable=notifycheck, onvalue="True", offvalue="False",
                              height=0, width=0, command=updatingjson)
    settingnoti.config(background="#FC4445", activebackground="#FC4445", activeforeground="black", fg="black",
                       font=("Courier", 8))
    settingsound = Checkbutton(settingWindow, text="Sound", variable=soundcheck, onvalue="True", offvalue="False", height=0,
                               width=0, command=updatingjson)
    settingsound.config(background="#FC4445", activebackground="#FC4445", activeforeground="black", fg="black",
                        font=("Courier", 8))
    while run == 1:
        if notify == "True":
            settingnoti.select()
        if sound == "True":
            settingsound.select()
        run = 2
    settingnoti.place(relx=0.3, rely=0.3)
    settingsound.place(relx=0.3, rely=0.1)
    settingWindow.grab_set()


settingImage = PhotoImage(file="./assets/gear.png")
setting = Button(window, image=settingImage, command=settingwindow)
setting.config(background="#FC4445", font=("Courier", 8), bd=0, fg="blue", activebackground="#FC4445")
setting.place(x=183, y=0)


window.protocol('WM_DELETE_WINDOW', hide_window)
window.mainloop()

ListenerPress.join()
