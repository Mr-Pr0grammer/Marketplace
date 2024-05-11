from django.contrib.auth.models import User
from django.db import models


class UserComplaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.user}'

    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'