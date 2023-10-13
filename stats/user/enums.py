from dataclasses import dataclass

TOKEN_TYPE_CHOICE = (
    ("password_reset", "PASSWORD_RESET"),
)

ROLE_CHOICE = (
    ("admin", "ADMIN"),
    ("coach", "COACH"),
    ("organizator", "ORGANIZATOR"),
    ("president", "PRESIDENT")
)

@dataclass
class TokenEnum:
    PASSWORD_RESET = "PASSWORD_RESET"


@dataclass
class SystemRoleEnum:
    ADMIN = "ADMIN"
    COACH = "COACH"
    ORGANIZATOR = "ORGANIZATOR"
    PRESIDENT = "PRESIDENT"

