from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('light-blue', 'Light Blue'),
    ('yellow', 'Yellow'),
    ('light-yellow', 'Light Yellow'),
    ('red', 'Red'),
    ('light-red', 'Light Red'),
    ('green', 'Green'),
    ('light-green', 'Light Green'),
    ('gray', 'Gray'),
    ('black', 'Black'),
    ('white', 'White')
]

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=20, choices=COLORS_CHOICES, default='light-blue')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    def delete(self, *args, **kwargs):
        owned = self.owned.all()
        if owned.exists():
            for room in owned:
                users = room.users.exclude(username=self.username).all()
                if users.exists():
                    room.transfer_ownership(new_owner=users[0])
                else: room.delete()
        super().delete(*args, **kwargs)