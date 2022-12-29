import io
import time
from typing import Generator, Union

from picamera2 import Picamera2 as Picamera


from image_providers.image_provider import ImageProvider


class Picamera2ImageProvider(ImageProvider):

    _picamera: Picamera = None

    def __init__(self, width: int = 1200, height: int = 900, framerate: int = 30, *args, **kwargs) -> None:
        self.width = width,
        self.height = height
        self.framerate = framerate

        ImageProvider.__init__(self, *args, **kwargs)

    def __enter__(self):
        if Picamera2ImageProvider._picamera is None:
            Picamera2ImageProvider._picamera = Picamera()

        Picamera2ImageProvider._picamera.resolution = self.width, self.height
        Picamera2ImageProvider._picamera.framerate = self.framerate

        if not Picamera2ImageProvider._picamera.started:
            Picamera2ImageProvider._picamera.start()
            time.sleep(2)

        return super().__enter__()

    def frames(self) -> Generator[io.BytesIO, None, None]:
        try:
            stream = io.BytesIO()
            while True:
                Picamera2ImageProvider._picamera.capture_file(
                    stream, format='jpeg')
                stream.seek(0)

                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
        finally:
            Picamera2ImageProvider._picamera.stop()
