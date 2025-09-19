from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # A classe está vazia por enquanto, mas está pronta para receber novos campos,
    # como 'time_torcido', se for necessário depois.
    pass
