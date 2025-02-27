import json
from django.db import models

class ReadInfo(models.Model):
    user = models.ForeignKey(
        "user.CustomUser", verbose_name="Kullanıcı", on_delete=models.CASCADE
    )
    read_time = models.DateTimeField(verbose_name="Okuma Anı", auto_now_add=True)

    def __str__(self):
        return f"{self.user} okudu ({self.read_time})"

class Message(models.Model):
    status = models.BooleanField(verbose_name="Okundu", default=False)
    content = models.TextField(verbose_name="Mesaj İçeriği",)
    readlist = models.ManyToManyField(ReadInfo, verbose_name="Okuyanlar", related_name="message_reads")
    author = models.ForeignKey(
        "user.CustomUser", verbose_name="Yazan", related_name="messages_written",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(verbose_name="Oluşturulma Anı", auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} by {self.author}"

    def set_json_data(self, data):
        self.content = json.dumps(data)

    def get_json_data(self):
        return json.loads(self.content)

class Chat(models.Model):
    messages = models.ManyToManyField(Message, verbose_name="Mesajlar", related_name="message_chat")
    members = models.ManyToManyField("user.CustomUser", verbose_name="Üyeler", related_name="chat_members")
    creator = models.ForeignKey(
        "user.CustomUser", verbose_name="Oluşturan", related_name="user_chats_created",
        on_delete=models.CASCADE
    )
    updator = models.ForeignKey(
        "user.CustomUser", verbose_name="Güncelleyen", related_name="user_chats_updated",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(verbose_name="Oluşturulma Anı", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Güncellenme Anı", auto_now=True)

    def __str__(self):
        return f"Chat {self.id} by {self.creator}"
