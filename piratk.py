import atexit
import logging
import socket
import tkinter as tk
import tkinter.ttk as ttk

import musicpd


LOG = logging.getLogger(__name__)


def update_local_ips(strvar):
    data = socket.getaddrinfo(socket.gethostname(), None, family=socket.AF_INET)
    first = data[0]
    strvar.set('IP: ' + first[4][0])


def cleanup(client):

    def disconnect():
        LOG.debug('Disconnecting from %s', client)
        client.close()
        client.disconnect()

    return disconnect


class BackendPlayer(object):

    def __init__(self, mpd_client):
        self.client = mpd_client
        self._handlers = {
            'song_changed': set(),
            'status_changed': set(),
        }

    def _song_changed(self):
        for handler in self._handlers['song_changed']:
            handler()

    def _status_changed(self):
        for handler in self._handlers['status_changed']:
            handler()

    def init(self):
        self.client.repeat(1)
        self.client.play()

    def add_song_changed_handler(self, fun):
        self._handlers['song_changed'].add(fun)

    def add_status_changed_handler(self, fun):
        self._handlers['status_changed'].add(fun)

    def previous(self):
        LOG.info('Sending previous command')
        self.client.previous()
        self._song_changed()

    def next_(self):
        LOG.info('Sending next command')
        self.client.next()
        self._song_changed()

    def play(self):
        LOG.info('Sending play command')
        self.client.play()
        self._song_changed()

    def stop(self):
        LOG.info('Sending stop command')
        self.client.stop()
        self._status_changed()

    def title(self):
        info = self.client.currentsong()
        name = info.get('name', '?')
        title = info.get('title', '?')
        return ' - '.join([name, title])


class PiraTK(object):

    def __init__(self, master, player):
        self._master = master
        self._player = player
        master.attributes('-zoomed', True)

        style = ttk.Style()
        style.configure("TLabel",
                        foreground="green",
                        background='#000022',
                        font="Symbol 24",
                        relief="flat")
        style.configure("TButton",
                        foreground="green",
                        background='#000022',
                        font="Symbol 24",
                        relief="flat")
        style.map("TButton",
                  background=[('pressed', '#000055'),
                              ('active', '#000033')])
        style.configure("TFrame", background="#000022")

        self._status_text = tk.StringVar()
        update_local_ips(self._status_text)
        self._song_label = tk.StringVar()
        self._song_label.set('piratk')
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
        label = ttk.Label(frame, textvariable=self._status_text)
        label.pack(side=tk.LEFT, fill=tk.X)
        frame.pack(fill=tk.X)
        return label

    def _setup_main_controls(self):
        frame = ttk.Frame(self._master)
        prevbtn = ttk.Button(frame, text="<", command=self._player.previous)
        nextbtn = ttk.Button(frame, text=">", command=self._player.next_)
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


def main():
    logging.basicConfig(level=logging.DEBUG)

    # MPD setup
    mpd = musicpd.MPDClient()
    mpd.connect('localhost', 6600)
    atexit.register(cleanup(mpd))

    # Backend Player
    player = BackendPlayer(mpd)

    # Tk
    root = tk.Tk()
    app = PiraTK(root, player)
    app.toggle_fullscreen()
    root.mainloop()


if __name__ == '__main__':
    main()
