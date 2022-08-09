from datetime import datetime

from rest_framework import serializers


def check_date_deadline(value):
    now = datetime.now()
    if value < datetime.date(now):
        raise serializers.ValidationError('Дедлайн не может быть раньше сегодняшней даты')
