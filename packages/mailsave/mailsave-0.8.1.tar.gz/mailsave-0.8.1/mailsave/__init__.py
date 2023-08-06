import base64
import os
import re
import sys
import unicodedata

from datetime import datetime
from email import (
    charset as Charset,
    message_from_bytes,
    message_from_string,
)
from os.path import join


# Taken from https://github.com/django/django/blob/458e2fbfcc0a06d7d55ff5a1dcd79c91c64e8138/django/core/mail/message.py  # noqa
RFC5322_EMAIL_LINE_LENGTH_LIMIT = 998

#  From https://github.com/django/django/blob/458e2fbfcc0a06d7d55ff5a1dcd79c91c64e8138/django/core/mail/message.py#L24  # noqa
utf8_charset = Charset.Charset('utf-8')
utf8_charset.body_encoding = None  # Python defaults to BASE64
utf8_charset_qp = Charset.Charset('utf-8')
utf8_charset_qp.body_encoding = Charset.QP


__version__ = '0.8.1'


def save(content, folder='.', filename=None, extract_html=False):
    if isinstance(content, str):
        message = message_from_string(content)
    else:
        message = message_from_bytes(content)

    charset = utf8_charset
    if message['Content-Transfer-Encoding'] == 'base64':
        content = base64.b64decode(message.get_payload())
        # From https://github.com/django/django/blob/458e2fbfcc0a06d7d55ff5a1dcd79c91c64e8138/django/core/mail/message.py#L220  # noqa

        if any(len(l) > RFC5322_EMAIL_LINE_LENGTH_LIMIT for l in content.splitlines()):
            charset = utf8_charset_qp
        message.set_payload(content, charset=charset)

    message.set_charset(charset)

    to = message.get('To', None)
    from_ = message.get('from', None)
    subject = message.get('subject', None)

    try:
        os.makedirs(folder, exist_ok=True)
    except FileExistsError:
        print('{} is a file'.format(folder), file=sys.stderr)
    else:
        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = filename or '{date}.mbox'
        file_name = file_name.format(date=date, to=to, from_=from_, subject=subject)
        file_name = normalize_file_name(file_name)
        file_path = join(folder, file_name)

        with open(file_path, 'wb') as output:
            output.write(message.as_bytes())

    if extract_html:
        extract_html_from_message(message, file_path.replace('.mbox', '.html'))


def extract_html_from_message(message, file_name):
    payload = message.get_payload()
    if isinstance(payload, str) and is_part_html(message):
        save_html(payload, file_name)
    else:
        for part in message.walk():
            payload = part.get_payload(decode=True)
            if isinstance(payload, bytes) and is_part_html(part):
                save_html(payload, file_name)
                break


def is_part_html(part):
    return part['Content-Type'].startswith('text/html;')


def save_html(content, file_name):
    mode = 'wb' if isinstance(content, bytes) else 'w'
    with open(file_name, mode) as output:
        output.write(content)


def normalize_file_name(file_name):
    # From http://stackoverflow.com/a/295466
    file_name = unicodedata.normalize('NFKD', file_name)\
        .encode('ascii', 'ignore')\
        .decode('ascii')
    file_name = re.sub('[^\w\s\-\.@<>+]', '', file_name).strip().lower()
    return re.sub('[-\s]+', '-', file_name)
