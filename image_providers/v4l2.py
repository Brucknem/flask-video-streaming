"""Requires python-v4l2capture module: https://github.com/gebart/python-v4l2capture"""

import io
from typing import Generator
from PIL import Image
import select
from image_providers.image_provider import ImageProvider
import v4l2capture


class V4L2ImageProvider(ImageProvider):

    def start(self, source: str = None, *args, **kwargs):
        self.source = source
        return super().start()

    def frames(self) -> Generator[io.BytesIO, None, None]:
        video = v4l2capture.Video_device(self.source)
        # Suggest an image size. The device may choose and return another if unsupported
        size_x = 640
        size_y = 480
        size_x, size_y = video.set_format(size_x, size_y)
        video.create_buffers(1)
        video.queue_all_buffers()
        video.start()
        stream = io.BytesIO()

        try:
            while True:
                # Wait for the device to fill the buffer.
                select.select((video,), (), ())
                image_data = video.read_and_queue()
                image = Image.frombytes("RGB", (size_x, size_y), image_data)
                image.save(stream, format="jpeg")

                yield stream.getvalue()

                stream.seek(0)
                stream.truncate()
        finally:
            video.close()
