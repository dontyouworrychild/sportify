from django.contrib import admin
from .models import Competition, Federation, Participant

admin.site.register(Competition)
admin.site.register(Federation)
admin.site.register(Participant)