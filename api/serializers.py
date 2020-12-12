from django.contrib.auth.models import User
from .models import Faculty,Department,Event,Examination,EntranceExamination,Notice,Holiday
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    staff_of = serializers.StringRelatedField()
    class Meta:
        model = User
        fields = ['url', 'username', 'email','staff_of']

class FacultySerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField(many=True)
    events = serializers.StringRelatedField(many=True)
    examinations = serializers.StringRelatedField(many=True)
    class Meta:
        model = Faculty
        fields = ['title','description','image_url','department','events','examinations']

class DepartmentSerializer(serializers.ModelSerializer):
    events = serializers.StringRelatedField(many=True)
    examinations = serializers.StringRelatedField(many=True)
    class Meta:
        model = Department
        fields = ['title','description','image_url','faculty','events','examinations']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title','description','faculty','department','venue','start_time','end_time','slug']

class ExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        fields = ['subject','code','semester','exam_type','faculty','department','slug']

class EntranceExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntranceExamination
        fields = ['course','start_time','end_time','slug']

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['text','file_url','date_issued']

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ['title','slug']