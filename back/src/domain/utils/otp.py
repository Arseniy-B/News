import secrets
import string

from src.domain.exceptions import ValidationError


# class Otp(str):
#     def __new__(cls, value: str):
#         value = str(value) 
#
#         if len(value) != 6:
#             raise ValidationError("Otp")
#
#         instance = super().__new__(cls, value)
#         return instance

Otp = str

def generate_otp_code(length: int = 6) -> Otp:
    digits = string.digits
    return Otp("".join(secrets.choice(digits) for _ in range(length)))

