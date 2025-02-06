from django.db import models
from django.db.models import CASCADE
from django.forms import ValidationError
from subjects.models import Subject
from users.models import User

class Registration(models.Model):
    student_id = models.ForeignKey(User, on_delete=CASCADE, null=True, related_name="registrations")
    subject_id = models.ForeignKey(Subject, on_delete=CASCADE, null=True, related_name="registrations")
    registration_date = models.DateTimeField(auto_now_add=True)
    final_rating = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    def clean(self):
        if self.student_id.rol != 'alumno':
            raise ValidationError("El usuario debe tener el rol de 'Alumno' para inscribirse en una materia.")
        # Obtener los prerequisitos de la materia que intenta inscribir
        # prerequisites = self.subject_id.prerequisitos.all()

        # for prereq in prerequisites:
        #     if not Registration.objects.filter(student_id=self.student_id, subject_id=prereq, final_rating__gte=3.0).exists():
        #         raise ValidationError(f"No puedes inscribirte en {self.subject_id} sin haber aprobado {prereq}.")

    def save(self, *args, **kwargs):
        self.clean()  
        super().save(*args, **kwargs)
    
    def is_approved(self):
        return self.final_rating is not None and self.final_rating >= 3.0

    class Meta:
        unique_together = ('student_id', 'subject_id') 

    def __str__(self):
        return f"{self.student_id.username} inscrito en {self.subject_id}"