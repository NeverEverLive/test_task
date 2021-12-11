from django.contrib import admin
from django.contrib.admin import ModelAdmin

from parking_spaces.models import *


@admin.register(ParkingSpace)
class ParkingSpacesAdmin(ModelAdmin):
    pass


@admin.register(Reservation)
class ParkingSpacesAdmin(ModelAdmin):
    pass
