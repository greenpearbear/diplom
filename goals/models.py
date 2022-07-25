from django.db import models
from django.utils import timezone

from core.models import User


class DateModelMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class GoalCategory(DateModelMixin):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Goal(DateModelMixin):

    STATUS = [
        ("1", "К выполнению"),
        ("2", "В работе"),
        ("3", "Выполнено"),
        ('4', "Архив")
    ]

    PRIORITY = [
        ("1", "Низкий"),
        ("2", "Средний"),
        ("3", "Высокий"),
        ('4', "Критический")
    ]

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, verbose_name='Категория', on_delete=models.PROTECT)
    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.CharField(verbose_name='Описание', max_length=1023)
    status = models.CharField(max_length=1, choices=STATUS, default='execution')
    priority = models.CharField(max_length=1, choices=PRIORITY, default='middle')
    due_date = models.DateField()
