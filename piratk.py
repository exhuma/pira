import logging
import atexit
import tkinter as tk
import tkinter.ttk as ttk

import musicpd


LOG = logging.getLogger(__name__)


def cleanup(client):

    def disconnect():
        LOG.debug('Disconnecting from %s', client)
        client.close()
        client.disconnect()

    return disconnect


class FullscreenApp2(object):

    def __init__(self, master):
        self._master = master
        master.attributes('-zoomed', True)

        style = ttk.Style()
        style.configure("TButton",
                        foreground="green",
                        background='#000022',
                        relief="flat")
        style.map("TButton",
                  background=[('pressed', '#000055'),
                              ('active', '#000033')])
        style.configure("TFrame", background="#000022")
        style.configure("TTreeView",
                        fieldbackground="#000022",
                        background="#000022")

        self.frame = ttk.Frame(master)

        self.bottomctrls = ttk.Frame(master)
        stopbtn = ttk.Button(self.bottomctrls, text="Stop",
                             command=self._stop)
        playbtn = ttk.Button(self.bottomctrls, text="Play",
                             command=self._play)
        stopbtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        playbtn.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.bottomctrls.pack(side=tk.BOTTOM)

        prevbtn = ttk.Button(self.frame, text="<", command=self._previous)
        nextbtn = ttk.Button(self.frame, text=">", command=self._next)
        plist = ttk.Treeview(self.frame)

        prevbtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        plist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        nextbtn.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.frame.pack(fill=tk.BOTH, expand=True)
        self.is_fullscreen = False
        master.bind("<F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.end_fullscreen)

        self.client = musicpd.MPDClient()
        self.client.connect('localhost', 6600)
        self.client.repeat(1)
        self.client.play()
        atexit.register(cleanup(self.client))

    def _update_info(self):
        LOG.debug('updating info')
        info = self.client.currentsong()
        name = info.get('name', '?')
        title = info.get('title', '?')
        LOG.debug('Setting info to {} - {}'.format(name, title))

    def _play(self):
        LOG.info('Sending play command')
        self.client.play()
        self._update_info()

    def _stop(self):
        LOG.info('Sending stop command')
        self.client.stop()
        self._update_info()

    def _next(self):
        LOG.info('Sending next command')
        self.client.next()
        self._update_info()

    def _previous(self):
        LOG.info('Sending previous command')
        self.client.previous()
        self._update_info()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self._master.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def end_fullscreen(self, event=None):
        self.is_fullscreen = False
        self._master.attributes("-fullscreen", False)
        return "break"


logging.basicConfig(level=logging.DEBUG)
root = tk.Tk()
app = FullscreenApp2(root)
root.mainloop()
