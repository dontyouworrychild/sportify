from dataclasses import dataclass
from django.utils.translation import gettext_lazy as _

SPORT_TYPES = (
    ("karate", _("Karate")),
    ("taekwondo", _("Taekwondo")),
    ("judo", _("Judo")),
    ("jiu-jitsu", _("Jiu-Jitsu")),
    # Add more sports here as needed
)

TOKEN_TYPE_CHOICE = (
    ("PASSWORD_RESET", _("PASSWORD_RESET")),
)

ROLE_CHOICE = (
    ("admin", _("ADMIN")),
    ("coach", _("COACH")),
    ("organizator", _("ORGANIZATOR")),
    ("president", _("PRESIDENT"))
)

AGE_CATEGORY_CHOICE = (
    ("16-17", "16-17"),
    ("14-15", "14-15"),
    ("12-13", "12-13"),
    ("10-11", "10-11"),
    ("8-9", "8-9"),
    ("6-7", "6-7")
)

WEIGHT_CATEGORY_CHOICE = (
    ("44kg", "44kg"),
    ("48kg", "48kg"),
    ("52kg", "52kg"),
    ("56kg", "56kg"),
    ("60kg", "60kg"),
    ("64kg", "64kg"),
    ("68kg", "68kg"),
    ("72kg", "72kg"),
    ("76kg", "76kg")
)

REGIONS = (
    ("abai_region", _("Abai region")),
    ("akmola_region", _("Akmola region")),
    ("aktobe_region", _("Aktobe Region")),
    ("almaty_city", _("Almaty city")),
    ("almaty_region", _("Almaty region")),
    ("astana_city", _("Astana city")),
    ("atyrau_region", _("Atyrau region")),
    ("baikonur_city", _("Baikonur city")),
    ("east_kazakhstan_region", _("East Kazakhstan region")),
    ("jambyl_region", _("Jambyl region")),
    ("jetisu_region", _("Jetisu region")),
    ("karaganda_region", _("Karaganda region")),
    ("kostanay_region", _("Kostanay region")),
    ("kyzylorda_region", _("Kyzylorda region")),
    ("mangystau_region", _("Mangystau region")),
    ("north_kazakhstan_region", _("North Kazakhstan region")),
    ("pavlodar_region", _("Pavlodar region")),
    ("shymkent_city", _("Shymkent city")),
    ("turkistan_region", _("Turkistan region")),
    ("ulytau_region", _("Ulytau region")),
    ("west_kazakhstan_region", _("West Kazakhstan region"))
)

@dataclass
class TokenEnum:
    PASSWORD_RESET = _("PASSWORD_RESET")


@dataclass
class SystemRoleEnum:
    ADMIN = _("admin")
    COACH = _("coach")
    ORGANIZATOR = _("organizator")
    PRESIDENT = _("president")

