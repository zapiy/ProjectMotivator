import string
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def email(val: str):
    if ' ' in val:
        return False
    elif len(val) not in range(4, 150):
        return False
    elif not EMAIL_REGEX.match(val):
        return False
    return True

def login(val: str):
    errors = []
    
    if not filter(
        lambda k: not (
            k in string.ascii_letters
            or k in string.digits
            or k in ['-', '_']
        ), val
    ):
        errors.append("Логин содержит не допустимые символы! (Доступно: верхний и нижний регистр, числа)")
    if len(val) not in range(4, 16):
        errors.append("Длина логина не может быть меньше 4 и превышать 15 символов")
    
    return errors

def password(val: str):
    errors = []
    
    if not any(filter(lambda k: k not in string.ascii_letters, val)):
        errors.append("В пароле должен быть хотя-бы один символ")
    if not any(filter(lambda k: k not in string.digits, val)):
        errors.append("В пароле должен быть хотя-бы одно число")
    if len(val) not in range(5, 26):
        errors.append("Длина пароля не может быть меньше 5 и превышать 25 символов")
    
    return errors
