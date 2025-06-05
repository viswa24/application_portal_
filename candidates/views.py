from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CandidateSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import json

# Create your views here.

@api_view(['POST'])
def apply_candidate(request):
    print('apply_candidate view called')
    print('request.data:', request.data)
    print('request.FILES:', request.FILES)
    data = request.data.copy()
    files = request.FILES

    # Parse JSON for nested fields
    education_json = data.get('education_qualifications', '[]')
    work_json = data.get('work_experiences', '[]')
    try:
        education_list = json.loads(education_json)
    except Exception:
        education_list = []
    try:
        work_list = json.loads(work_json)
    except Exception:
        work_list = []

    # Attach files to the correct nested fields
    for i, edu in enumerate(education_list):
        cert_key = f'education_qualifications[{i}][certificate]'
        if cert_key in files:
            edu['certificate'] = files[cert_key]
        else:
            edu.pop('certificate', None)
    for i, work in enumerate(work_list):
        cert_key = f'work_experiences[{i}][certificate]'
        if cert_key in files:
            work['certificate'] = files[cert_key]
        else:
            work.pop('certificate', None)

    # Prepare serializer data
    serializer_data = data.dict()
    serializer_data['education_qualifications'] = education_list
    serializer_data['work_experiences'] = work_list

    serializer = CandidateSerializer(data=serializer_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('Serializer errors:', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
