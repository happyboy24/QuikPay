
from django.db import models
from django.conf import settings
from Quickpay import settings



class Notification(models.Model):
    CHANNEL_TYPE = (
    ('EMAIL', 'Email'),
    ('SMS', 'SMS'),
    )
    wallet=models.CharField(max_length=10, null=True, blank=True)
    reference = models.CharField(max_length=11, unique= True, blank=True, null=True)
    message = models.TextField()
    channel = models.CharField(max_length=10, choices= CHANNEL_TYPE, default='EMAIL')
    event_type = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


