import io
import time
from typing import Generator

try:
    from picamera2 import Picamera2 as Picamera
except:
    from picamera import Picamera


from image_providers.image_provider import ImageProvider


class PicameraImageProvider(ImageProvider):

    _picamera = None

    def __enter__(self):
        if PicameraImageProvider._picamera is None:
            PicameraImageProvider._picamera = Picamera()

        if not PicameraImageProvider._picamera.started:
            PicameraImageProvider._picamera.start()
            time.sleep(2)

        return super().__enter__()

    def frames(self) -> Generator[io.BytesIO, None, None]:
        try:
            stream = io.BytesIO()
            while True:
                PicameraImageProvider._picamera.capture_file(
                    stream, format='jpeg')
                stream.seek(0)

                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
        finally:
            PicameraImageProvider._picamera.stop()
