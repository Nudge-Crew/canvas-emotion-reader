import logging
import sys

log = logging.getLogger(__name__)

IS_DEV = False


def init(debug):
    global IS_DEV
    IS_DEV = debug
    if debug:
        if not log.handlers:
            log.setLevel(logging.DEBUG)
            formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(module)s: %(message)s", datefmt="%H:%M:%S")
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)

            log.addHandler(handler)
