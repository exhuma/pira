import argparse
import atexit
import logging

from pira.core_ui import App
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
    parser.add_argument('--verbose', action='store_true',
                        help='Be verbse', default=False)
    parser.add_argument('--fs', action='store_true',
                        help='Run in full-screen.', default=False)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    # MPD setup
    mpd = musicpd.MPDClient()
    mpd.connect('localhost', 6600)
    atexit.register(cleanup(mpd))

    # Backend Player
    player = MpdPlayer(mpd)

    app = App(player, args.fs)

    # Begin playing
    player.init()

    app.run()
