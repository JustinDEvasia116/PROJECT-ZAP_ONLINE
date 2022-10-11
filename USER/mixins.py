from django.conf import settings
from twilio.rest import Client
import random 

class MessageHandler:
    phone_number = None
    otp = None
    def __init__(self, phone_number, otp)->None:
        self.phone_number = phone_number
        self.otp = otp
        
    def sent_otp_on_phone(self):
        # Send OTP on phone
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

        message = client.messages.create(
                                        body='Your OTP for login is  '+str(self.otp),
                                        from_='+13605316403',
                                        to=self.phone_number
                                    )
        print(message.sid)
       
