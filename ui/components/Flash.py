from tkinter import *
import queue


class Flash(Toplevel):
    def __init__(self, root, **options):
        Toplevel.__init__(self, root, width=200, height=200, **options)
        self.overrideredirect(True)  # remove header from toplevel
        self.root = root
        self.attributes("-alpha", 0.0)  # set transparency to 100%
        self.queue = queue.Queue()
        self.update_me()

    def write(self, message):
        # insert message into the queue
        self.queue.put(message)

    def update_me(self):
        # This makes our tkinter widget threadsafe
        # http://effbot.org/zone/tkinter-threads.htm
        try:
            while 1:
                # get message from the queue
                message = self.queue.get_nowait()
                # if a message is received code will execute from here otherwise exception
                # http://stackoverflow.com/questions/11156766/placing-child-window-relative-to-parent-in-tkinter-pythons
                # set x coordinate of root
                x = self.root.winfo_rootx()
                # set y coordinate of root
                y = self.root.winfo_rooty()
                # get the height of root
                height = self.root.winfo_height()
                # get the width of root
                width = self.root.winfo_width()
                # place in the center of root
                self.geometry("+%d+%d" % (x + width / 2, y + height / 2))
                # fade in when a message is received
                self.fade_in()
                label_flash = Label(self, text=message, bg='black',
                                    fg='white', font=('times', 36, 'bold'))
                label_flash.pack(anchor='e')
                self.lift(self.root)

                def callback():
                    label_flash.after(2000, label_flash.destroy)
                    self.fade_away()

                label_flash.after(3000, callback)

        except queue.Empty:
            pass
        self.after(100, self.update_me)  # check queue every 100th of a second

    # http://stackoverflow.com/questions/3399882/having-trouble-with-tkinter-transparency
    def fade_in(self):
        alpha = self.attributes("-alpha")
        alpha = min(alpha + .01, 1.0)
        self.attributes("-alpha", alpha)
        if alpha < 1.0:
            self.after(10, self.fade_in)

    # http://stackoverflow.com/questions/22491488/how-to-create-a-fade-out-effect-in-tkinter-my-code-crashes
    def fade_away(self):
        alpha = self.attributes("-alpha")
        if alpha > 0:
            alpha -= .1
            self.attributes("-alpha", alpha)
            self.after(10, self.fade_away)
