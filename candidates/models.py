from django.db import models
from django.utils import timezone
import os

def candidate_upload_path(instance, filename, prefix):
    ext = filename.split('.')[-1]
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    candidate_id = instance.id if instance.id else 'new'
    base = os.path.splitext(filename)[0]
    return f"{prefix}/{candidate_id}_{timestamp}_{base}.{ext}"

def photo_upload_path(instance, filename):
    return candidate_upload_path(instance, filename, 'photos')

def signature_upload_path(instance, filename):
    return candidate_upload_path(instance, filename, 'signatures')

def certificate_upload_path(instance, filename):
    candidate_id = instance.candidate.id if instance.candidate_id else 'new'
    ext = filename.split('.')[-1]
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    base = os.path.splitext(filename)[0]
    return f"certificates/{candidate_id}_{timestamp}_{base}.{ext}"

def exp_certificate_upload_path(instance, filename):
    candidate_id = instance.candidate.id if instance.candidate_id else 'new'
    ext = filename.split('.')[-1]
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    base = os.path.splitext(filename)[0]
    return f"experience_certificates/{candidate_id}_{timestamp}_{base}.{ext}"

# Create your models here.

class Candidate(models.Model):
    POST_CHOICES = [
        ('CFO', 'CFO'),
        ('CEO', 'CEO'),
    ]
    name = models.CharField(max_length=100)
    post = models.CharField(max_length=3, choices=POST_CHOICES)
    date_of_birth = models.DateField(default='2000-01-01')
    email = models.EmailField(default='unknown@example.com')
    phone = models.CharField(max_length=15, default='Unknown')
    caste = models.CharField(max_length=50, default='Unknown')
    religion = models.CharField(max_length=50, default='Unknown')
    category = models.CharField(max_length=50, default='Unknown')
    permanent_line1 = models.CharField(max_length=255, default='Unknown')
    permanent_line2 = models.CharField(max_length=255, blank=True, default='')
    permanent_city = models.CharField(max_length=100, default='Unknown')
    permanent_district = models.CharField(max_length=100, default='Unknown')
    permanent_state = models.CharField(max_length=100, default='Unknown')
    permanent_pincode = models.CharField(max_length=10, default='Unknown')
    communication_line1 = models.CharField(max_length=255, default='Unknown')
    communication_line2 = models.CharField(max_length=255, blank=True, default='')
    communication_city = models.CharField(max_length=100, default='Unknown')
    communication_district = models.CharField(max_length=100, default='Unknown')
    communication_state = models.CharField(max_length=100, default='Unknown')
    communication_pincode = models.CharField(max_length=10, default='Unknown')
    same_as_permanent = models.BooleanField(default=False)
    experience_match = models.TextField(null=True, blank=True, default='')
    photo = models.ImageField(upload_to=photo_upload_path, null=True, blank=True)
    signature = models.ImageField(upload_to=signature_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.post})"

class EducationQualification(models.Model):
    CLASS_CHOICES = [
        ('First', 'First'),
        ('Second', 'Second'),
        ('Third', 'Third'),
    ]
    candidate = models.ForeignKey(Candidate, related_name='education_qualifications', on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    specialisation = models.CharField(max_length=100)
    board_institute = models.CharField(max_length=100)
    month_of_completion = models.CharField(max_length=20)
    year_of_completion = models.CharField(max_length=4)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    class_obtained = models.CharField(max_length=10, choices=CLASS_CHOICES)
    certificate = models.FileField(upload_to=certificate_upload_path, blank=True, null=True)

    def __str__(self):
        return f"{self.course} - {self.specialisation} ({self.candidate.name})"

class WorkExperience(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='work_experiences', on_delete=models.CASCADE)
    institution = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    tasks_duties = models.TextField()
    certificate = models.FileField(upload_to=exp_certificate_upload_path, blank=True, null=True)

    def __str__(self):
        return f"{self.institution} - {self.designation} ({self.candidate.name})"
