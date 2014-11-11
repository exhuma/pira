import logging
import atexit
import tkinter as tk

from pira.core_ui import TkWindow
from pira.player import MpdPlayer

import musicpd

LOG = logging.getLogger(__name__)


def cleanup(client):

    def disconnect():
        LOG.debug('Disconnecting from %s', client)
        client.close()
        client.disconnect()

    return disconnect


def main():
    logging.basicConfig(level=logging.DEBUG)

    # MPD setup
    mpd = musicpd.MPDClient()
    mpd.connect('localhost', 6600)
    atexit.register(cleanup(mpd))

    # Backend Player
    player = MpdPlayer(mpd)

    # Tk
    root = tk.Tk()
    root.config(cursor="none")
    root.attributes('-zoomed', True)
    root.geometry('{}x{}'.format(320, 240))
    app = TkWindow(root, player)
    app.toggle_fullscreen()

    # Begin playing
    player.init()
    root.mainloop()
