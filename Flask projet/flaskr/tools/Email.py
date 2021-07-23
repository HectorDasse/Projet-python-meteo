import smtplib

def SendMail(Text):
    gmail_user = 'dassehector@gmail.com'
    gmail_password = 'fpitihvilemtfjlk'

    sent_from = "dassehector@gmail.com"
    to = 'hector.dasse@orange.fr'
    subject = 'OMG Super Important Message'
    body = Text

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, Text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')
