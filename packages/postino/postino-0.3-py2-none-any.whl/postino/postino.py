# coding: utf-8
import functools
import os

from .config import load
from .constants import DEFAULT_STR_ENCODING
from .constants import DEFAULT_STR_ENCODING_ERRORS
from .construct import construct
from .send import send_message


CONFIG_PATH = os.path.expanduser(os.environ.get('POSTINO_CONFIG', '~/.postino'))


def postino_raw(
        text='',
        html='',
        subject='',
        to=[],
        cc=[],
        bcc=[],
        fromaddr=[],
        host='localhost',
        port=25,
        mode=None,
        login=None,
        password=None,
        encoding=DEFAULT_STR_ENCODING,
        encoding_errors=DEFAULT_STR_ENCODING_ERRORS):

    message, fromline, recipients = construct(
        text=text,
        html=html,
        subject=subject,
        to=to,
        cc=cc,
        bcc=bcc,
        fromaddr=fromaddr,
        encoding=encoding,
        encoding_errors=encoding_errors)

    send_message(
        message,
        recipients,
        fromline,
        host=host,
        port=port,
        mode=mode,
        login=login,
        password=password)


def Sender(**kwargs):
    return functools.partial(postino_raw, **kwargs)


default_sender = None


def reload_config(path=CONFIG_PATH):
    global default_sender
    default_sender = Sender(**load(path))


def postino(*args, **kwargs):
    if default_sender is None:
        reload_config()
    default_sender(*args, **kwargs)
