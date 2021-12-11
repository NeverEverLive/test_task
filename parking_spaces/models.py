from itertools import chain

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class ParkingSpace(models.Model):

    class Meta:
        verbose_name = 'Space'
        verbose_name_plural = 'Spaces'

    def __str__(self):
        return f'ID: {self.id}'

    def save(self, *args, **kwargs):
        if ParkingSpace.objects.all().count() < 2:
            return super(ParkingSpace, self).save(*args, **kwargs)

        raise ValidationError("Too many records")


class Reservation(models.Model):
    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    start_date = models.DateField()
    end_date = models.DateField()
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.PROTECT)
    client = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self,  *args, **kwargs):
        start_date = self.start_date
        end_date = self.end_date
        space = self.parking_space
        queryset1 = Reservation.objects.filter(start_date__range=(start_date, end_date), parking_space=space).exclude(pk=self.pk)
        queryset2 = Reservation.objects.filter(end_date__range=(start_date, end_date), parking_space=space).exclude(pk=self.pk)
        queryset = list(chain(queryset1, queryset2))
        if queryset:
            raise ValidationError("Records conflicts")
        else:
            return super(Reservation, self).save(*args, **kwargs)

    def __str__(self):
        return f'ID {self.id}: space №{self.parking_space.id} reserved by {self.client.username} ' \
               f'from {self.start_date} to {self.end_date}'
