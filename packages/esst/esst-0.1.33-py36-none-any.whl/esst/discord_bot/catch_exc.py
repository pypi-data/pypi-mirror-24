# coding=utf-8
"""
Catches connection error in Discord bot
"""

import aiohttp
import websockets.exceptions

from esst.core import CTX, MAIN_LOGGER
from esst.utils.conn import wan_available

LOGGER = MAIN_LOGGER.getChild(__name__)


def _pass_exception(exc):
    LOGGER.error(exc)
    # LOGGER.exception('Discord bot error')
    if CTX.sentry:
        CTX.sentry.captureException(True)


def catch_exc(func):
    """
    Decorator to protect discord.client methods
    """

    async def _wrapper(*args, **kwargs):

        try:
            return await func(*args, **kwargs)
        except websockets.exceptions.InvalidHandshake as exc:
            _pass_exception(exc)
        except websockets.exceptions.InvalidState as exc:
            _pass_exception(exc)
        except websockets.exceptions.PayloadTooBig as exc:
            _pass_exception(exc)
        except websockets.exceptions.WebSocketProtocolError as exc:
            _pass_exception(exc)
        except websockets.exceptions.InvalidURI as exc:
            _pass_exception(exc)
        except (aiohttp.ClientError, ConnectionError, OSError, aiohttp.ClientOSError) as exc:
            wan_available()
            _pass_exception(exc)

    return _wrapper
