from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages', 
        verbose_name="Відправник"
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_messages', 
        verbose_name="Отримувач"
    )
    text = models.TextField("Текст повідомлення", blank=True, null=True)
    image = models.ImageField("Прикріплене фото", upload_to='chat_images/', blank=True, null=True)
    is_read = models.BooleanField("Прочитано", default=False)
    created_at = models.DateTimeField("Час відправки", auto_now_add=True)

    class Meta:
        verbose_name = "Повідомлення"
        verbose_name_plural = "Повідомлення"
        ordering = ['created_at']  # Хронологічний порядок у чаті

    def __str__(self):
        return f"Від {self.sender.username} до {self.receiver.username} ({self.created_at.strftime('%d.%m.%Y %H:%M')})"