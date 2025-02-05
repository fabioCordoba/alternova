from django.db import models
from django.db.models import CASCADE
from django.forms import ValidationError
from subjects.models import Subject
from users.models import User

class Registration(models.Model):
    student_id = models.ForeignKey(User, on_delete=CASCADE, null=True)
    subject_id = models.ForeignKey(Subject, on_delete=CASCADE, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    final_rating = models.DecimalField(max_digits=4, decimal_places=2)

    def clean(self):
        """Validar que el usuario tenga el rol de 'alumno' antes de guardar."""
        if self.student_id.rol != 'alumno':
            raise ValidationError("El usuario debe tener el rol de 'Alumno' para inscribirse en una materia.")

    def save(self, *args, **kwargs):
        self.clean()  # Ejecutar la validación antes de guardar
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('student_id', 'subject_id') 

    def __str__(self):
        return f"{self.student_id.username} inscrito en {self.subject_id}"