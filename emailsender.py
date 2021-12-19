import smtplib


class EmailSender:
    def __init__(self, sender_mail, sender_mail_password, **kwargs):
        """This Method Takes Sender Email And Password To Login In Your Email Account"""
        self.email_providers = {"aol": "smtp.aol.com",
                                "comcast": {"server":"smtp.comcast.net","port": 587},
                                "icloud": {"server":"smtp.mail.me.com","port": 587},
                                "gmail": {"server":"smtp.gmail.com","port": 587},
                                "outlook": {"server":"smtp-mail.outlook.com","port": 587},
                                "yahoo": {"server":"smtp.mail.yahoo.com","port": 587},
                                }
        self.from_email = sender_mail
        self.password = sender_mail_password
        for key in kwargs:
            if key == "email_provider" and kwargs[key] in self.email_providers:
                self.smtp_link = self.email_providers[kwargs[key]]["server"]
                self.port = self.email_providers[kwargs[key]]["port"]

    def email_send(self, recipient_mail, subject, message):
        postman = smtplib.SMTP(host=self.smtp_link, port=self.port)
        postman.starttls()
        postman.login(user=self.from_email, password=self.password)
        postman.sendmail(from_addr=self.from_email, to_addrs=recipient_mail
                         , msg=f"Subject:{subject}\n\n{message}")
        postman.close()
