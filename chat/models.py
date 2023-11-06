from django.db import models
from users.models import User
from django.template.defaultfilters import slugify
import random
import hashlib


class ChatRoom(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True, null=True, blank=True)
    description = models.CharField(max_length=200)
    last_message = models.TextField(max_length=280, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    sticky = models.BooleanField(default=False)
    invite = models.CharField(max_length=30, null=True, blank=True)

    users = models.ManyToManyField(User, related_name='rooms')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.title))
        if not self.invite:
            random_value = str(random.random())
            combined_value = self.title + random_value
            invite_key = hashlib.sha256(combined_value.encode()).hexdigest()[:30]
            self.invite = invite_key
            
        super().save(*args, **kwargs)
        return self


class ChatMessage(models.Model):
    text = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        room = self.room
        room.last_message = f'{self.user.username}: {self.text}'[:50]
        room.timestamp = self.timestamp
        room.save()
        return self
    

class PrivateChat(models.Model):
    last_message = models.CharField(max_length=280, null=True, blank=True)
    users = models.ManyToManyField(User, related_name='private')
    timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
    

class PrivateMessage(models.Model):
    text = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return self.text
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        room = self.room
        room.last_message = f'{self.user.username}: {self.text}'[:50]
        room.timestamp = self.timestamp
        room.save()
        return self