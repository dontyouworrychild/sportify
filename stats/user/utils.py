import base64
import os
import pyotp

from .enums import SystemRoleEnum
from .models import User

def is_admin_user(user:User)->bool:
    """
    Check an authenticated user is an admin or not
    """
    return user.is_admin or SystemRoleEnum.ADMIN in user.roles
    

def send_sms(phone_number:str, message:str):
    """Integrate with your sms service."""
    print(message)
    return


def validate_phone_number(phone_number:str):
        """Need to add some logic here, tipo check if it starts +7 degen siyakty"""
        return phone_number
        

def generate_otp()->int:
    totp = pyotp.TOTP(base64.b32encode(os.urandom(16)).decode('utf-8'))
    otp = totp.now()
    return otp