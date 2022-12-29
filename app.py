#!/usr/bin/env python
import io
import pathlib
from typing import Generator
from flask import Flask, render_template, Response, request, redirect, url_for

import image_providers

available_videos = [pathlib.Path(*file.parts[1:]) for file in pathlib.Path(
    'videos').iterdir() if file.is_file()]

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    provider = request.args.get('provider', 'fallback')
    source = request.args.get('source', None)
    available_providers = image_providers.availables.keys()
    return render_template('index.html', provider=provider, source=source, providers=list(available_providers), sources=available_videos)


def gen(provider: str, **kwargs) -> Generator[io.BytesIO, None, None]:
    """Video streaming generator function."""
    yield b'--frame\r\n'

    with image_providers.select(provider)(**kwargs) as image_provider:
        while True:
            frame = image_provider.get_frame()
            yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed/')
def fallback_video_feed():
    return redirect(url_for('video_feed', provider='fallback'))


@app.route('/video_feed/<provider>')
def video_feed(provider: str):
    """Video streaming route. Put this in the src attribute of an img tag."""

    return Response(gen(provider, **request.args),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
