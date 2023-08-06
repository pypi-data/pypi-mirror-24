#!/usr/bin/env python3

import argparse
import asyncore
import re
import sys

from copy import deepcopy
from mailsave import __version__, save
from mailsave.smtp import MailSaveServer
from io import BytesIO


def main():
    parser = argparse.ArgumentParser(
        description='Dump mails into files. Can be used as a '
                    'replacement for sendmail or an SMTP server'
    )
    parser.add_argument(
        '--dir',
        default='.',
        help='Directory in which to save the mails.',
    )
    parser.add_argument(
        '--filename',
        default=None,
        help='Directory in which to save the mails. If not given, it will use the date '
             'like 2017-07-07_14-78-00.mbox You can use in your filename:'
             '{date} that will be replaced by the date, '
             '{from_} that will be replaced by the from address, '
             '{to} that will be replaced by the to address',
    )
    parser.add_argument(
        '-t',
        action='store_true',
        help='Unescape dots located at the start of a line. For instance, swiftmailer '
             'will espape dots at the start of a line (ie replace ``.`` by ``..``) '
             'before transferring the mail to sendmail because this is how sendmail '
             'expects to receive a mail. This allows mailsave to act as a drop in '
             'replacement for ``sendmail -t``'
    )
    parser.add_argument(
        '--no-save',
        dest='save',
        action='store_false',
        help='Do not save the email in the output folder. Usefull if you need something '
             'to act like sendmail but do not care about the email.'
    )
    parser.add_argument(
        '--extract-html',
        action='store_true',
        help='If the body of the message is in HTML or if it has an attachement in HTMl, '
             'extract it in a dedicated file. The file will be named after the mbox file. '
             'Only the extension will change'
    )
    parser.add_argument(
        '--server',
        action='store_true',
        default=False,
        help='Listen on a TPC socket for mails.',
    )
    parser.add_argument(
        '--port',
        type=int,
        default=2525,
        help='Port on which to listen. For server mode.',
    )
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='Host on which to listen. For server mode. Can be a hostnane like localhost '
             'or an ip address',
    )
    parser.add_argument(
        '--version',
        '-v',
        action='store_true',
        help='Print the version and exit',
    )

    # If -i or -ti is used, remove the -t option.
    args = deepcopy(sys.argv)
    ti_option = {'-i', '-it', '-ti'}
    opt_to_remove = set(args) & ti_option
    if len(opt_to_remove) > 0:
        args = [arg for arg in args if arg not in opt_to_remove]

    args, _ = parser.parse_known_args(args=args)

    if args.version:
        print(__version__)
    elif args.server:
        read_server(args)
    else:
        read_stdin(args)


def read_server(args):
    server = MailSaveServer(  # noqa
        args.host,
        args.port,
        args.dir,
        filename=args.filename,
        extract_html=args.extract_html,
        save=args.save
    )
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print('Quitting')


def read_stdin(args):
    content = BytesIO()
    try:
        for line in iter(sys.stdin.buffer.read, b''):
            content.write(line)

        content = content.getvalue()
        if args.t:
            content = re.sub(b'\n\.\.', b'\n.', content, re.M)

        if args.save:
            save(
                content,
                folder=args.dir,
                filename=args.filename,
                extract_html=args.extract_html
            )
    except KeyboardInterrupt:
        print('Quitting')


if __name__ == '__main__':
    main()
