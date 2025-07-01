# models.py
from django.db import models
from django.contrib.auth.models import User

class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    image = models.ImageField(upload_to='user_cards/')
    text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"
