from django.contrib import admin
from subjects.models import Subject

@admin.register(Subject)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'teacher_id']
