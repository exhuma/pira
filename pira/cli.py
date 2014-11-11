import argparse
import atexit
import logging
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


def parse_args():
    parser = argparse.ArgumentParser(description='PI Radio')
    parser.add_argument('--fs', action='store_true',
                        help='Run in full-screen.', default=False)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)

    # MPD setup
    mpd = musicpd.MPDClient()
    mpd.connect('localhost', 6600)
    atexit.register(cleanup(mpd))

    # Backend Player
    player = MpdPlayer(mpd)

    # Tk
    root = tk.Tk()
    if args.fs:
        root.config(cursor="none")
        root.attributes('-zoomed', True)
    else:
        root.geometry('{}x{}'.format(320, 240))

    app = TkWindow(root, player)

    if args.fs:
        app.toggle_fullscreen()

    # Begin playing
    player.init()
    root.mainloop()
