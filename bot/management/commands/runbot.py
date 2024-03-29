from django.conf import settings
from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory


class Command(BaseCommand):
    help = "run bot"
    offset = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle_user_without_verification(self, msg: Message, tg_user: TgUser):
        tg_user.set_verification_code()
        tg_user.save(update_fields=["verification_code"])
        self.tg_client.send_message(
            msg.chat.id, f"[verification code] {tg_user.verification_code}"
        )

    def fetch_tasks(self, msg: Message, tg_user: TgUser):
        gls = Goal.objects.filter(user=tg_user.user)
        if gls.count() > 0:
            resp_msg = [f"#{item.id} {item.title}" for item in gls]
            self.tg_client.send_message(msg.chat.id, "\n".join(resp_msg))
        else:
            self.tg_client.send_message(msg.chat.id, "[goals list is empty]")

    def fetch_task(self, msg: Message, tg_user: TgUser):
        data_category = []
        categories = GoalCategory.objects.filter(user=tg_user.user)
        if categories.count() > 0:
            resp_msg = [f"#{item.id} {item.title}" for item in categories]
            self.tg_client.send_message(msg.chat.id, "\n".join(resp_msg))
            for item in categories:
                data_category.append(item.title)
            self.create_task(msg, tg_user, data_category)
        else:
            self.tg_client.send_message(msg.chat.id, "[categories list is empty]")

    def create_task(self, msg: Message, tg_user: TgUser, data_category):
        response_categories = self.tg_client.get_updates(offset=self.offset, timeout=60)
        for item_categories in response_categories.result:
            categories_response = item_categories.message.text
        if "/cancel" in categories_response:
            self.tg_client.send_message(msg.chat.id, 'Отмена создания цели')
        if categories_response in data_category:
            self.tg_client.send_message(msg.chat.id, "Введите заголовок цели")
            response_goal = self.tg_client.get_updates(offset=self.offset + 1, timeout=60)
            for item in response_goal.result:
                goal_response = item.message.text
            if "/cancel" in goal_response:
                self.tg_client.send_message(msg.chat.id, 'Отмена создания цели')
            else:
                self.tg_client.send_message(msg.chat.id,
                                            f"Категория - {categories_response} Цель - {goal_response}")
                Goal.objects.create(category=categories_response, title=goal_response, user=tg_user.user)
        else:
            self.tg_client.send_message(msg.chat.id, "Такой категории нет, введите заново")

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if not msg.text:
            return
        elif "/goals" in msg.text:
            self.fetch_tasks(msg, tg_user)
        elif "/create" in msg.text:
            self.fetch_task(msg, tg_user)
        else:
            self.tg_client.send_message(msg.chat.id, "[unknown command]")

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_id=msg.from_.id,
            defaults={
                "tg_chat_id": msg.chat.id,
                "username": msg.from_.username,
            },
        )
        if created:
            self.tg_client.send_message(msg.chat.id, "[greeting]")

        if tg_user.user:
            self.handle_verified_user(msg, tg_user)
        else:
            self.handle_user_without_verification(msg, tg_user)

    def handle(self, *args, **kwargs):
        while True:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1
                self.handle_message(item.message)
