from tkinter import *
import queue
from datetime import datetime
import threading
from components import Flash
from service import BluetoothService
import sys

def onEscape(event=None):
	print('Goodbye')
	sys.exit()


class Clock:
    def __init__(self):
        self.time = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        # self.time = time.strftime('%H:%M:%S')
        self.mFrame = Frame()
        # self.mFrame.pack(side=TOP, anchor=NW, expand=YES, fill=X)
        self.mFrame.pack(side=TOP, anchor=NW)
        self.watch = Label(self.mFrame, bg='black', fg='white',
                           text=self.time, font=('times', 12, 'bold'))
        self.watch.pack()
        self.updateTimeLabel()


    def updateTimeLabel(self):
        self.time = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        self.watch.configure(text=self.time)
        self.mFrame.after(200, self.updateTimeLabel)


class RefreshLabel:
    def __init__(self, side, anchor, generator_callback, refresh_time=200):
        self.refresh_time = refresh_time
        self.generator_callback = generator_callback
        self.message = self.generator_callback()
        self.mFrame = Frame()
        self.mFrame.pack(side=side, anchor=anchor)
        self.dynamic_label = Label(self.mFrame, bg='black', fg='white',
                                   text=self.message, font=('times', 12, 'bold'))
        self.update()

    def update(self):
        self.message = self.generator_callback()
        self.dynamic_label.configure(text=self.message)
        self.mFrame.after(self.refresh_time, self.update)

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()


root = Tk()
# NOTE: bind escape key to ("-fullscreen", False)
root.attributes("-fullscreen", True)
root.title('Aloha')
root.configure(bg='black')
root.geometry('500x500')
root.bind('<Escape>', onEscape)  

flash = Flash.Flash(root)


def callback():
    flash.write('Hello, Tony')


def update_clock():
    return datetime.now().strftime("%B %d, %Y %H:%M:%S")


t = threading.Thread(target=callback)
t.daemon = True
t.start()
clock = RefreshLabel(side=TOP, anchor=NW,
                     generator_callback=update_clock)

clock_test = Clock()
# Display current date and time
# datetime_label = Label(root, text=datetime.now(), bg="black", fg="white", font="none 24 bold")
# datetime_label.config(anchor='e')
# datetime_label.pack(side=TOP, anchor=NW)
# greeting_label = Label(root, text="Hello, Tony", bg='black', fg='white', font='none 24 bold')
# greeting_label.config(anchor=CENTER)
# greeting_label.pack()
#connected_devices = BluetoothService.list_connected_devices()
#device_label_txt = 'No bluetooth devices found'
#if len(connected_devices) > 0:
	# for now, just assume a single connected device
#	single_device = connected_devices[0]
#	device_label_txt = 'Bluetooth device connected: ' + single_device.get('Name')

# display name of connected device
#connected_device_label = Label(root, text='', bg='black', fg='white', font='none 24 bold')


app = Application(master=root)
app.mainloop()
