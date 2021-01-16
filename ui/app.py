import tkinter as tk
import queue
from datetime import datetime
import threading
from components import Flash
from service import BluetoothService


class Clock:
    def __init__(self):
        self.time = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        # self.time = time.strftime('%H:%M:%S')
        self.mFrame = tk.Frame()
        # self.mFrame.pack(side=TOP, anchor=NW, expand=YES, fill=X)
        self.mFrame.pack(side=tk.TOP, anchor=tk.NW)
        self.watch = tk.Label(self.mFrame, bg='black', fg='white',
                           text=self.time, font=('times', 12, 'bold'))
        self.watch.pack()
        self.updateTimeLabel()


    def updateTimeLabel(self):
        self.time = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        self.watch.configure(text=self.time)
        self.mFrame.after(200, self.updateTimeLabel)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()


root = tk.Tk()
# set background to black
root.title('Aloha')
root.configure(bg='black')
root.geometry('1000x1000')

flash = Flash.Flash(root)


def callback():
    import time
    flash.write('Hello, Tony')
    # time.sleep(2)
    # flash.write('The current temperature inside is: 22 C')
    # flash.write('The current humidity inside is: 33.8')
    # time.sleep(2)


t = threading.Thread(target=callback)
t.daemon = True
t.start()
clock = Clock()
# Display current date and time
# datetime_label = Label(root, text=datetime.now(), bg="black", fg="white", font="none 24 bold")
# datetime_label.config(anchor='e')
# datetime_label.pack(side=TOP, anchor=NW)
# greeting_label = Label(root, text="Hello, Tony", bg='black', fg='white', font='none 24 bold')
# greeting_label.config(anchor=CENTER)
# greeting_label.pack()
# connected_devices = BluetoothService.list_connected_devices()
#
# for c in connected_devices:
#     print(c)

app = Application(master=root)
app.mainloop()
