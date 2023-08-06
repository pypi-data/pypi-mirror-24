import logging

from mailsave import save
from smtpd import SMTPServer


class MailSaveServer(SMTPServer):
    def __init__(self, host, port, dir, filename=None, save=True, extract_html=False):
        logging.basicConfig(level=logging.INFO)
        super().__init__((host, port), None)
        self.dir = dir
        self.filename = filename
        self.save = save
        self.extract_html = extract_html
        logging.info('Listening for mail on {}:{}'.format(host, port))

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        logging.info('Received mail from address {} from peer {}'.format(mailfrom, peer))
        if self.save:
            save(data, folder=self.dir, filename=self.filename, extract_html=self.extract_html)
