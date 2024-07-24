import asyncio
import logging

from json import dumps
from pathlib import Path
from re import search

## python -m pip show tornado
## python -m pip install --upgrade pip tornado
import tornado.web


class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write(f"{self.settings.get('message')}\n")


def make_app(*args, **kwargs):
    return tornado.web.Application(
        [
            (r"/.*", HelloWorldHandler),
        ],
        debug=True,
        message=kwargs.get("message", "Hello, World!"),
    )


async def main(*args, **kwargs):
    name = f"{Path(__file__).name} - "
    logging.debug(f"{name} main - *args: {args}")
    logging.debug(f"{name} main - **kwargs: {kwargs}")

    app = make_app(**kwargs)
    app.listen(int(kwargs.get("port", 8888)))
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
