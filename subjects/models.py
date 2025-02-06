from django.db import models
from django.db.models import CASCADE
from users.models import User
import random
import string

def generate_code(name):
    initials = ''.join([word[0] for word in name.split()])[:3].upper()
    numbers = ''.join(random.choices(string.digits, k=3))
    return f"{initials}-{numbers}"

class Subject(models.Model):
    code = models.CharField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=255)
    teacher_id = models.ForeignKey(User, on_delete=CASCADE, null=True, related_name="subjects")
    prerequisitos = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='materias_dependientes')
    is_finalized = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
