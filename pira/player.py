"""
This module abstracts away the details of the MPD backend, and provides the
player API used by the front-end.
"""

import logging

LOG = logging.getLogger(__name__)


class MpdPlayer(object):

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
        self._song_changed()

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
