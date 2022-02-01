from django.contrib import admin

from evangelisation.models import Evangelisation,  Person, Site, Suivi, Image, Participant, Profile


admin.site.register(Evangelisation)
admin.site.register(Person)
admin.site.register(Site)
admin.site.register(Image)
admin.site.register(Suivi)
admin.site.register(Profile)
admin.site.register(Participant)

