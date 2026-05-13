from django.db import models

from QuickPay import settings


# Create your models here.

class Notification(models.Model):

    CHANNEL_TYPE = (
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
    )

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    # Since we have create() in the notification app and the method
    # takes user as an arguement, making notification model to have
    # user as one of its variables will tight couple notification
    # and user to some extent although reduced the tight coupling a bit
    # by having a general services folder where all the individual
    # services are utilized. We will remove the extra coupling by removing the user
    # as one of its variables.

    wallet = models.CharField(max_length=10, blank=True, null=True)
    reference = models.CharField(max_length=40, unique=True, blank=True, null=True)
    message = models.TextField()
    channel = models.CharField(max_length=10, choices=CHANNEL_TYPE, default='EMAIL')
    event_type = models.CharField(max_length=50)
    is_read= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

