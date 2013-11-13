from django.contrib.auth.models import User
from django.db import models

class Constant(models.Model):
    user = models.ForeignKey(User,
        help_text = "User account this information belongs to",
    )

    tax_rate = models.FloatField(
        help_text = "Current tax rate",
    )

