from django.db import models
from django.conf import settings
from .base_model import BaseModel
from .taker import Taker


class Donate(BaseModel):
    taker = models.ForeignKey(Taker, on_delete=models.CASCADE, related_name="donates")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    donate = models.IntegerField()
    description = models.TextField(null=True, blank=True)
