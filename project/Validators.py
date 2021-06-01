import re


def username_validation(username):
    return pattern_validation(username, r'^(?![-._])(?!.*[_.-]{2})[\w.-]{4,30}(?<![-._])$')


def password_validation(password):
    return pattern_validation(password, r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")


def email_validation(email):
    return pattern_validation(email, r"^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$")


def pattern_validation(value, pattern):
    return re.match(pattern, value) is not None and re.match(pattern, value).string == value
