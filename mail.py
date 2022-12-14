import smtplib

SMTP_SERVER = "mail.gandi.net"
SMTP_PORT = 587
SMTP_USERNAME = "ultimate@benjamin-b.fr"
SMTP_PASSWORD = "In3>2&Op2+?"
EMAIL_FROM = "ultimate@benjamin-b.fr"
EMAIL_TO = "contact@benjamin-b.fr"
EMAIL_SUBJECT = "Test du module d'envoie de mail via Python"
EMAIL_MESSAGE = "The message here"

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
    smtp.starttls()
    smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
    message = 'Subject: {}\n\n{}'.format(EMAIL_SUBJECT, EMAIL_MESSAGE)
    #smtp.sendmail(                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               EMAIL_FROM, EMAIL_TO, message)

    print("test")

print("coucou")