import random

from django.db import models

from core.models import User

CODE_VOCABULARY = "jvnsdv438hv7ewrjoij3fijwue"


class TgUser(models.Model):
    telegram_chat_id = models.BigIntegerField()
    telegram_user_ud = models.BigIntegerField()
    username = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    verification_code = models.CharField(max_length=32)

    class Meta:
        verbose_name = "tg пользователь"
        verbose_name_plural = "tg пользователи"

    def set_verification_code(self):
        code = "".join([random.choice(CODE_VOCABULARY) for _ in range(12)])
        self.verification_code = code
