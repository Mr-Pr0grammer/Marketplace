from django.contrib.auth.models import User
from django.db import models


class UserComplaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    def __str__(self):
        return f'От {self.user}'

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'