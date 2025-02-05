from django.contrib import admin
from registrations.models import Registration

@admin.register(Registration)
class RegistrationsAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'subject_id', 'registration_date', 'final_rating']
