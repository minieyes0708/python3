# -*- coding=cp950 -*-
class miniSendMail:
    def __init__(self):
        self.server = 'ms22.hinet.net'
        self.from_  = 'chenvey2@gmail.com'
        self.to     = 'chenvey2@gmail.com'
    def send(self, subject, message):
        from smtplib import SMTP
        hinet = SMTP(self.server)
        hinet.sendmail(self.from_, self.to, u'\r\n'.join([
            'From: '    + self.from_,
            'To: '      + self.to,
            'Subject: ' + subject,
            '',
            message]).encode('big5'))
        hinet.quit()

if __name__ == '__main__':
    mail = miniSendMail()
    mail.send('test subject', 'Hello World')
