from django.db import models


class HelloMessage(models.Model):
    """Model for storing hello world messages"""
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
