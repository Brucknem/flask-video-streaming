import logging
from types import ModuleType
from typing import Dict
import image_providers.fallback
from image_providers.image_provider import ImageProvider

availables: Dict[str, ImageProvider] = {
    'fallback': image_providers.fallback.FallbackImageProvider}

try:
    import image_providers.pi
    availables['pi'] = image_providers.pi.PicameraImageProvider
except Exception as e:
    logging.warn(e)

try:
    import image_providers.pi2
    availables['pi2'] = image_providers.pi2.Picamera2ImageProvider
except Exception as e:
    logging.warn(e)

try:
    import image_providers.opencv
    availables['opencv'] = image_providers.opencv.OpenCVImageProvider
except Exception as e:
    logging.warn(e)

try:
    import image_providers.v4l2
    availables['v4l2'] = image_providers.v4l2.V4L2ImageProvider
except Exception as e:
    logging.warn(e)


def select(name: str) -> type[ImageProvider]:
    try:
        return availables[name]
    except Exception as e:
        logging.error(
            f'Camera {name} not supported. Using fallback camera. ({e})')
        return availables['fallback']
