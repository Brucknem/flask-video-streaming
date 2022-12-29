import time
from typing import Generator
import io

from image_providers.image_provider import ImageProvider


class FallbackImageProvider(ImageProvider):
    imgs = [open(f, 'rb').read()
            for f in [f'images/{i}.jpg' for i in range(1, 4)]]

    def frames(self) -> Generator[io.BytesIO, None, None]:
        while True:
            yield FallbackImageProvider.imgs[int(time.time()) % 3]
            time.sleep(0.1)
