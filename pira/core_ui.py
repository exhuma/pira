import logging
import socket
import tkinter as tk
import tkinter.ttk as ttk

LOG = logging.getLogger(__name__)


def update_local_ips(strvar):
    data = socket.getaddrinfo(socket.gethostname(), None, family=socket.AF_INET)
    first = data[0]
    strvar.set('IP: ' + first[4][0])


class TkWindow(object):

    def __init__(self, master, player):
        self._master = master
        self._player = player

        style = ttk.Style()
        style.configure("Small.TLabel",
                        foreground="yellow",
                        background='#000022',
                        font="Symbol 10",
                        relief="flat")
        style.configure("TLabel",
                        foreground="green",
                        background='#000022',
                        font="Symbol 12",
                        padding=5,
                        relief="flat")
        style.configure("TButton",
                        foreground="green",
                        background='#000022',
                        font="Symbol 24",
                        relief="raised")
        style.map("TButton",
                  background=[('pressed', '#000055'),
                              ('active', '#000033')])
        style.configure("TFrame", background="#000022")

        self._status_text = tk.StringVar()
        update_local_ips(self._status_text)
        self._song_label = tk.StringVar()
        self._song_label.set('PI Radio')
        self._setup_header()
        self._setup_main_controls()
        self._setup_bottom_controls()
        self._setup_footer()

        self.is_fullscreen = False
        master.bind("<F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.end_fullscreen)

        player.add_status_changed_handler(self._update_info)
        player.add_song_changed_handler(self._update_info)

    def _setup_header(self):
        frame = ttk.Frame(self._master)
        label = ttk.Label(frame, textvariable=self._song_label)
        label.pack(side=tk.LEFT, fill=tk.X)
        frame.pack(fill=tk.X)
        return label

    def _setup_footer(self):
        frame = ttk.Frame(self._master)
        label = ttk.Label(frame,
                          textvariable=self._status_text,
                          justify=tk.CENTER,
                          padding=10,
                          style="Small.TLabel")
        label.pack(side=tk.LEFT, fill=tk.X)
        frame.pack(fill=tk.X)
        return label

    def _setup_main_controls(self):
        frame = ttk.Frame(self._master)
        prevbtn = ttk.Button(frame, text="<",
                             command=self._player.previous)
        nextbtn = ttk.Button(frame, text=">",
                             command=self._player.next_)
        prevbtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        nextbtn.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        frame.pack(fill=tk.BOTH, expand=True)

    def _setup_bottom_controls(self):
        # Bottom Controls
        self.bottomctrls = ttk.Frame(self._master)
        stopbtn = ttk.Button(self.bottomctrls, text="Stop",
                             command=self._player.stop)
        playbtn = ttk.Button(self.bottomctrls, text="Play",
                             command=self._player.play)
        stopbtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        playbtn.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.bottomctrls.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def _update_info(self):
        LOG.debug('updating info')
        title = self._player.title()
        LOG.debug('Setting info to {}'.format(title))
        self._song_label.set(title)

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self._master.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def end_fullscreen(self, event=None):
        self.is_fullscreen = False
        self._master.attributes("-fullscreen", False)
        return "break"


class App(object):

    def __init__(self, player, fs):
        self._fs = fs
        self._player = player

        # Tk
        self._root = tk.Tk()
        if fs:
            self._root.config(cursor="none")
            self._root.attributes('-zoomed', True)
        else:
            self._root.geometry('{}x{}'.format(320, 240))

        window = TkWindow(self._root, player)

        if fs:
            window.toggle_fullscreen()

    def run(self):
        self._root.mainloop()
