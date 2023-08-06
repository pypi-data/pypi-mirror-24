=========
Mail Save
=========

Save emails to a file. It can be used as a replacement for sendmail or a SMTP server.

You can install it with ``pip install mailsave`` or ``pip install --user mailsave``

You can also use the single `file version <https://framagit.org/Jenselme/mailsave/tree/master/dist/mailsave.py>`__. Since mailsave only needs the standard library, you don't have anything to install.

It is different from other tools like `maildump <https://pypi.org/project/maildump/>`__ because:

- It is very minimalist: no Web or GUI interface, just files.
- It can be used instead of sendmail.

To use in place of sendmail, just put the path to the ``mailsave`` executable instead of the sendmail one. For instance, in a ``php.ini`` file:

::

    sendmail_path = /home/jenselme/.virtualenvs/test/bin/mailsave --dir mails

To use as an SMTP server, launch it like this:

::

    mailsave --server --dir mails

Then you can send it emails with the SMTP protocol:

::

    swaks --to user@example.com --server localhost --port 2525 --add-header "X-Custom-Header: Swaks-Tested"

To view the full help, use:

::

    mailsave --help


Written for Python 3.5+.
