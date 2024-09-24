from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from web.extensions import mail

"""  """

import requests
from threading import Thread
from flask import current_app, render_template

""" mailtrap using python request """
def send_mail_0(subject, sender, recipients, text_body, html_body):
    def send_async_email(app, subject, sender, recipients, text_body, html_body):
        try:
            with app.app_context():
                token = app.config['MAILTRAP_API_KEY']
                
                # Mailtrap API endpoint
                url = 'https://sandbox.api.mailtrap.io/api/send'

                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }

                # Prepare email data
                data = {
                    "from": {"email": sender, "name": "Mailtrap Test"},
                    "to": [{"email": email} for email in recipients],
                    "subject": subject,
                    "text": text_body,
                    "html": html_body,
                    "category": "Integration Test"
                }

                # Send email
                response = requests.post(url, headers=headers, json=data)

                if response.status_code == 200:
                    print('Success, email sent!')
                else:
                    print(f'Email Error->: {response.text}')

        except Exception as e:
            print(f'Email Error->: {e}')
            return f"{e}"

    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), subject, sender, recipients, text_body, html_body)
    ).start()


""" mailtrap using mailtrap openai_client """
import mailtrap as mt
def send_mail_1(subject, sender, recipients, text_body, html_body):
    def send_async_email(app, subject, sender, recipients, text_body, html_body):
        try:
            with app.app_context():
                token = app.config['MAILTRAP_API_KEY']
                print(token)
                # Create Mailtrap Mail object
                mail = mt.Mail(
                    sender=mt.Address(email=sender, name="Intellect"),
                    to=[mt.Address(email=email) for email in recipients],
                    subject=subject,
                    text=text_body,
                    html=html_body
                )

                # Create MailtrapClient and send email
                openai_client = mt.MailtrapClient(token=token)
                openai_client.send(mail)

                print('Success, email sent!')
        except Exception as e:
            print(f'Email Error->: {e}')
            return f"{e}"

    # Start sending email in a separate thread
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), subject, sender, recipients, text_body, html_body)
    ).start()
""" ====================================== """

def send_mail(subject, sender, recipients, text_body, html_body):
    def send_async_email(app, msg):
        try:
            with app.app_context():
                mail.send(msg)
                print(f'success, email sent!')
        except Exception as e:
            print(f'Email Error->: {e}')
            return f"{e}"

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    msg.body = text_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def reset_email(user):
    token = user.make_token(token_type="reset_password")
    send_mail(
        '[Techa] . Reset Your Password',
        sender="hackers@techa.tech",
        recipients=[user.email],
        text_body=render_template('email/forgot.txt', user=user, token=token),
        html_body=render_template('email/forgot.html', user=user, token=token)
    )

def verify_email(user):
    token = user.make_token(token_type="verify_email")
    send_mail(
        '[Techa] . Verifications',
        sender="hackers@techa.tech",
        recipients=[user.email],
        text_body=render_template('email/verify.txt', user=user, token=token),
        html_body=render_template('email/verify.html', user=user, token=token)
    )

def confirm_email(user):
    token = user.make_token(token_type="confirm_email")
    send_mail(
        '[Techa] . Verifications',
        sender="hackers@techa.tech",
        recipients=[user.email],
        text_body=render_template('email/verify.txt', user=user, token=token),
        html_body=render_template('email/verify.html', user=user, token=token)
    )



