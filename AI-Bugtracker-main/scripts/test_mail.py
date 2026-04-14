import os
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv

def test_mail():
    load_dotenv()
    app = Flask(__name__)
    
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
    
    mail = Mail(app)
    
    with app.app_context():
        msg = Message("Test Email from AI Bug Tracker",
                      recipients=[app.config['MAIL_USERNAME']])
        msg.body = "This is a test email to verify SMTP configuration."
        
        print(f"Attempting to send email to {app.config['MAIL_USERNAME']}...")
        print(f"Using server: {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")
        print(f"Username: {app.config['MAIL_USERNAME']}")
        
        try:
            mail.send(msg)
            print("SUCCESS: Email sent successfully!")
        except Exception as e:
            print(f"FAILURE: Could not send email.")
            print(f"ERROR DETAILS: {str(e)}")

if __name__ == "__main__":
    test_mail()
