from rest_framework import serializers
from subjects.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'code', 'name', 'teacher_id', 'prerequisitos']