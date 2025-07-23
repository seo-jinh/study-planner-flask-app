import os

# Environment variables = secret or configurable values that my program can pull from the system
# Look in the system’s environment variables and gets its values such as SECRET_KEY, EMAIL_USER, EMAIL_PASS
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')                  # Used by Flask-WTF and token generation
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # Optional, if using env for DB
    MAIL_SERVER = 'smtp.googlemail.com'                        # Gmail SMTP(Simple Mail Transfer Protocol) Tells to use Gmail to send mails
    MAIL_PORT = 587                                            # port number Gmail uses for sending email with TLS encryption
    MAIL_USE_TLS = True                                        # TLS (Transport Layer Security) encrypts the email as it’s sent Prevents hackers from intercepting your email while it's in transit
    MAIL_USERNAME = os.environ.get('EMAIL_USER')               # Gmail email
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')               # Gmail app password