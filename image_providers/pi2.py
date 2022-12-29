import io
import time
from typing import Generator, Union

from picamera2 import Picamera2 as Picamera
from libcamera import Transform


from image_providers.image_provider import ImageProvider
from singleton import Singleton


class Picamera2ImageProvider(ImageProvider, metaclass=Singleton):

    _picamera: Picamera = None

    def __init__(self) -> None:
        self.size = (1920, 1080)
        self.flip = True

        super().__init__()

    def start(self, resolution: str = None, flip: str = None, *args, **kwargs):
        if resolution is not None:
            self.size = (1920, 1080) if resolution == 'high' else (1296, 972)
        if flip is not None:
            self.flip = str(flip).lower() in ['yes', 'true', '']

        if Picamera2ImageProvider._picamera is None:
            Picamera2ImageProvider._picamera = Picamera()

        Picamera2ImageProvider._picamera.stop()
        video_config = Picamera2ImageProvider._picamera.create_video_configuration(
            transform=Transform(vflip=self.flip),
            main={"size": self.size},
            lores={"size": (320, 240)},
            encode="lores"
        )
        Picamera2ImageProvider._picamera.start(video_config)

        return super().start()

    def frames(self) -> Generator[io.BytesIO, None, None]:
        stream = io.BytesIO()
        try:
            while True:
                Picamera2ImageProvider._picamera.capture_file(
                    stream, format='jpeg')
                stream.seek(0)

                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
        except Exception as e:
            print(e)
        finally:
            print('Closing')
            stream.close()
            Picamera2ImageProvider._picamera.stop()
