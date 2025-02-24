import logging
import math

import pychromecast
import pychromecast.controllers.media
import trakt

log = logging.getLogger(__name__)


class TraktScrobblerListener(object):
    def __init__(self, device: pychromecast.Chromecast):
        self.device = device
        log.debug('Created listener for %s', device.name)

    def new_media_status(self, status: pychromecast.controllers.media.MediaStatus):
        scrobble_args = {}

        if status.media_is_tvshow:
            scrobble_args['show'] = {
                'title': status.series_title
            }
            scrobble_args['episode'] = {
                'season': status.season,
                'number': status.episode
            }
        elif status.media_is_movie:
            scrobble_args['movie'] = {
                'title': status.title
            }
        else:
            return

        progress = 0
        if status.duration != 0:
            progress = math.ceil(((status.current_time or 0) / status.duration) * 100)
            if progress < 1:
                progress = 1
            elif progress > 100:
                progress = 100
            scrobble_args['progress'] = progress

        scrobble_action = None
        if progress == 100 or (status.player_is_idle and
                               status.idle_reason and status.idle_reason.upper() == 'FINISHED'):
            scrobble_action = 'stop'
        elif status.player_is_playing:
            scrobble_action = 'start'
        elif status.player_is_paused:
            scrobble_action = 'pause'

        if scrobble_action:
            resp = trakt.Trakt['scrobble'][scrobble_action](**scrobble_args)
            print('Scrobble ', scrobble_args, ('SUCCESS' if resp else 'FAILURE'))
