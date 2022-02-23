from pynput import keyboard
from tkinter import *
from tkinter import messagebox
from pystray import MenuItem as item
import pystray
from PIL import Image
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from playsound import playsound
from plyer import notification

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

current = set()
COMBINATIONS = [
    {keyboard.Key.shift, keyboard.KeyCode(char='A')}
]
# Fix shift only being the key detected

def execute():
    ismute = volume.GetMute()
    if ismute == 0:
        if sound.get() or soundnormal:
            playsound('./assets/mute.mp3')
        volume.SetMute(1, None)
        if notify.get() or notifynormal:
            notification.notify(title="Noxu",
                                message="Muted",
                                app_icon='./assets/mute.ico',
                                timeout=5,
                                toast=True)
    else:
        volume.SetMute(0, None)
        if sound.get() or soundnormal:
            playsound('./assets/unmute.mp3')
        if notify.get() or notifynormal:
            notification.notify(title="Noxu",
                                message="Unmuted",
                                app_icon='./assets/mute.ico',
                                timeout=5,
                                toast=True)


def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()


def on_release(key):
    try:
        if any([key in COMBO for COMBO in COMBINATIONS]):
            current.remove(key)
    except KeyError:
        return


def quit_window(icon, item):
    icon.stop()
    Listener.stop()
    window.destroy()


def show_window(icon, item):
    icon.stop()
    window.deiconify()
    window.after(1, lambda: window.focus_force())


def hide_window():
    window.withdraw()
    image = Image.open('./assets/mute.ico')
    menu = (item('Open', show_window), item('Exit', quit_window),)
    icon = pystray.Icon("name", image, "Noxu", menu)
    icon.run()


Listener = keyboard.Listener(on_press=on_press, on_release=on_release)

Listener.start()

window = Tk()
window.maxsize(800, 500)
window.iconbitmap('./assets/mute.ico')
window.resizable(False, False)
window.config(bg="#FC4445")
window.title("Noxu")

notify = BooleanVar()
sound = BooleanVar()
soundnormal = True
notifynormal = True

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


def settingwindow():
    global notifynormal, soundnormal, run
    settingWindow = Toplevel(window)
    settingWindow.title("Settings")
    settingWindow.geometry("210x100")
    settingWindow.iconbitmap('./assets/mute.ico')
    settingWindow.resizable(False, False)
    settingWindow.config(bg="#FC4445")
    save = Button(settingWindow, text="Save", command=settingWindow.destroy)
    save.config(background="#FC4445", font=("Courier", 10), fg="white", relief=None, bd=0, activebackground="#FC4445", activeforeground="white")
    save.place(relx=0.4, y=75)
    notifynormal = False
    soundnormal = False
    settingnoti = Checkbutton(settingWindow, text="Notification", variable=notify, onvalue=True, offvalue=False, height=0, width=0)
    settingnoti.config(background="#FC4445", activebackground="#FC4445", activeforeground="black", fg="black", font=("Courier", 8))
    settingsound = Checkbutton(settingWindow, text="Sound", variable=sound, onvalue=True, offvalue=False, height=0, width=0)
    settingsound.config(background="#FC4445", activebackground="#FC4445", activeforeground="black", fg="black", font=("Courier", 8))
    while run == 1:
        settingnoti.select()
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

Listener.join()
