import logging
import time

import pychromecast

from traktcast.trakt import configure_trakt_client
from traktcast.hulu import HuluHandler
from traktcast.scrobble import TraktScrobblerListener

VIDEO_DEVICE_TYPES = ['Chromecast', 'Chromecast Ultra']

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('traktcast').setLevel(logging.DEBUG)

    configure_trakt_client()

    devices, service_browser = pychromecast.get_chromecasts()
    video_devices = (device for device in devices if device.model_name in VIDEO_DEVICE_TYPES)

    for device in video_devices:
        device.wait()

        device.register_handler(HuluHandler(device))
        device.media_controller.register_status_listener(TraktScrobblerListener(device))

    while True:
        time.sleep(0.01)
