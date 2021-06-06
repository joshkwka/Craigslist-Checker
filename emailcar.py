import smtplib
from email.message import EmailMessage

def send_email(receiving_email,message):
    email = EmailMessage()
    #enter real name:
    email['from'] = 'Craigslist Updater'
    email['to'] = receiving_email
    email['subject'] = 'Craigslist Update'

    content = ''
    for each in message:
        content += each
    email.set_content(content)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        #must enter real email and password for proper use
            #if you are uncomfortable inputting your information, 
            #you may create a new email and password for this project
        smtp.login(input('Sender Email: '), input('Password: '))
        smtp.send_message(email)
        print('email sent')


