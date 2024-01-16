from django.conf import settings
from django.db import models
from .base_model import BaseModel
from .city import City


class Taker(BaseModel):
    def auto_number():
        latest = Taker.objects.latest('date_created')
        if latest == None:
            return 1
        else:
            return latest.number + 1

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number = models.IntegerField(unique=True, editable=False, default=auto_number)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    images = models.JSONField(null=True, blank=True)
    stop_donate = models.BooleanField(default=False)
