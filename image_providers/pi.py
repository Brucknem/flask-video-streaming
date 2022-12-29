import io
import time
from typing import Generator, Union

from picamera import Picamera


from image_providers.image_provider import ImageProvider


class PicameraImageProvider(ImageProvider):

    _picamera = None

    def start(self, resolution: str = 'wide', flipped: bool = True, * args, **kwargs):
        size = (1296, 972)
        if resolution == 'high':
            size = (1920, 1080)

        if PicameraImageProvider._picamera is None:
            PicameraImageProvider._picamera = Picamera()

        PicameraImageProvider._picamera.stop()
        video_config = PicameraImageProvider._picamera.create_video_configuration(
            main={"size": size},
            lores={"size": (320, 240)},
            encode="lores"
        )
        PicameraImageProvider._picamera.start(video_config)

        return super().start()

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
