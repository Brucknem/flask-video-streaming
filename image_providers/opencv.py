import io
import pathlib
from typing import Generator
import cv2
import numpy as np

from image_providers.image_provider import ImageProvider


class OpenCVImageProvider(ImageProvider):

    def start(self, source: str = None, *args, **kwargs):
        self.source = pathlib.Path('videos').joinpath(str(source))
        return super().start()

    def frames(self) -> Generator[io.BytesIO, None, None]:
        capture = cv2.VideoCapture(str(self.source))

        while True:
            # read current frame
            _, img = capture.read()

            if img is None:
                img = np.random.randint(
                    0, 255, size=(512, 512, 3), dtype=np.uint8)

            # encode as a jpeg image and return it
            img = cv2.imencode('.jpg', img)[1].tobytes()

            yield img
