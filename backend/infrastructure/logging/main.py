from logging import getLogger, ERROR, StreamHandler
from sys import stdout

from pythonjsonlogger import jsonlogger


def setup_logging() -> None:
    """
    Setup the root logger configuration.

    - Setup handler and log format.
    - Configure the root logger logging level and handler.
    """
    handler = StreamHandler(stream=stdout)

    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s '
        '%(filename)s %(lineno)s %(user_id)s %(event_type)s',
        rename_fields={'name': 'logger_name'}
    )

    handler.setFormatter(formatter)

    root = getLogger()
    root.setLevel(level=ERROR)
    root.addHandler(hdlr=handler)
