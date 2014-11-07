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
        self.player = player
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
                             command=player.stop)
        playbtn = ttk.Button(self.bottomctrls, text="Play",
                             command=player.play)
        stopbtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        playbtn.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.bottomctrls.pack(side=tk.BOTTOM)

        prevbtn = ttk.Button(self.frame, text="<", command=player.previous)
        nextbtn = ttk.Button(self.frame, text=">", command=player.next_)
        plist = ttk.Treeview(self.frame)

        prevbtn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        plist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        nextbtn.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.frame.pack(fill=tk.BOTH, expand=True)
        self.is_fullscreen = False
        master.bind("<F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.end_fullscreen)

        player.add_status_changed_handler(self._update_info)
        player.add_song_changed_handler(self._update_info)

    def _update_info(self):
        LOG.debug('updating info')
        title = self.player.title()
        LOG.debug('Setting info to {}'.format(title))

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
    PiraTK(root, player)
    root.mainloop()


if __name__ == '__main__':
    main()
