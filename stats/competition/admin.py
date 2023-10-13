from django.contrib import admin
from .models import Competition, Federation, Game, Participant

admin.site.register(Competition)
admin.site.register(Federation)
admin.site.register(Game)
admin.site.register(Participant)