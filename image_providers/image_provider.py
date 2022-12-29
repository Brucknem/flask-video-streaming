import io
import logging
import time
import threading
from typing import BinaryIO, Generator

from image_providers.image_provider_event import ImageProviderEvent


class ImageProvider:
    def __init__(self, *args, **kwargs) -> None:
        self._thread = None  # background thread that reads frames from camera
        self._frame = None  # current frame is stored here by background thread
        self._stop_thread = False
        self._last_access = 0  # time of last client access to the camera
        self._event = ImageProviderEvent()

    def get_frame(self):
        self._last_access = time.time()

        self._event.wait()
        self._event.clear()

        return self._frame

    def __enter__(self):
        self._last_access = time.time()
        self._thread = threading.Thread(
            target=lambda: self.background_thread())
        self._thread.start()
        self._event.wait()
        return self

    def __exit__(self, *args):
        pass

    def background_thread(self):
        frames_iterator = self.frames()
        for frame in frames_iterator:
            self._frame = frame
            self._event.set()
            time.sleep(0)

            if time.time() - self._last_access > 5:
                frames_iterator.close()
                logging.info('Stopping camera thread due to inactivity.')
                break

    def frames(self) -> Generator[io.BytesIO, None, None]:
        raise NotImplementedError('Subclass must implement this method')
