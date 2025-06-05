from rest_framework import serializers
from .models import Candidate, EducationQualification, WorkExperience
import re

class EducationQualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationQualification
        fields = ['course', 'specialisation', 'board_institute', 'month_of_completion', 'year_of_completion', 'percentage', 'class_obtained', 'certificate']

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ['institution', 'designation', 'from_date', 'to_date', 'tasks_duties', 'certificate']

class CandidateSerializer(serializers.ModelSerializer):
    education_qualifications = EducationQualificationSerializer(many=True, required=False)
    work_experiences = WorkExperienceSerializer(many=True, required=False)

    class Meta:
        model = Candidate
        fields = [
            'id', 'name', 'post', 'date_of_birth', 'email', 'phone', 'caste', 'religion', 'category',
            'permanent_line1', 'permanent_line2', 'permanent_city', 'permanent_district', 'permanent_state', 'permanent_pincode',
            'communication_line1', 'communication_line2', 'communication_city', 'communication_district', 'communication_state', 'communication_pincode',
            'same_as_permanent', 'education_qualifications', 'work_experiences',
            'experience_match', 'photo', 'signature'
        ]

    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_phone(self, value):
        if not re.match(r"^\+?1?\d{9,15}$", value):
            raise serializers.ValidationError("Enter a valid phone number.")
        return value

    def validate_experience_match(self, value):
        words = value.split()
        if len(words) > 100:
            raise serializers.ValidationError("Experience match description should not exceed 100 words.")
        return value

    def validate_photo(self, value):
        if value and value.size > 200 * 1024:  # 200KB
            raise serializers.ValidationError("Photo size should not exceed 200KB.")
        return value

    def validate_signature(self, value):
        if value and value.size > 50 * 1024:  # 50KB
            raise serializers.ValidationError("Signature size should not exceed 50KB.")
        return value

    def create(self, validated_data):
        education_data = validated_data.pop('education_qualifications', [])
        work_data = validated_data.pop('work_experiences', [])
        candidate = Candidate.objects.create(**validated_data)
        for edu in education_data:
            EducationQualification.objects.create(candidate=candidate, **edu)
        for work in work_data:
            WorkExperience.objects.create(candidate=candidate, **work)
        return candidate

    def update(self, instance, validated_data):
        education_data = validated_data.pop('education_qualifications', [])
        work_data = validated_data.pop('work_experiences', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.education_qualifications.all().delete()
        instance.work_experiences.all().delete()
        for edu in education_data:
            EducationQualification.objects.create(candidate=instance, **edu)
        for work in work_data:
            WorkExperience.objects.create(candidate=instance, **work)
        return instance 