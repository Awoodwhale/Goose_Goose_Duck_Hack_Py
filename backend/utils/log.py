import sys
import logging
from typing import Any


class Log:
    open_log = True


formatter = logging.Formatter(
    "[%(asctime)s] %(message)s", datefmt="%Y/%m/%d %I:%M:%S %p"
)
logger = logging.getLogger("ggd_hack_py")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


def log(message: Any, state="debug"):
    """打印日志

    :param message: 日志内容
    :type message: Any
    :param state: 日志级别, defaults to "debug"
    :type state: str, optional
    """
    if not Log.open_log:
        return
    if state == "debug":
        logger.debug(message)
    elif state == "info":
        logger.info(message)
    elif state == "warning":
        logger.warning(message)
    elif state == "error":
        logger.error(message)
