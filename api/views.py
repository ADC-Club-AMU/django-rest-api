from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer
from .models import Faculty,Department,Event,Examination
from .serializers import FacultySerializer,DepartmentSerializer,EventSerializer,ExaminationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes # Djnago permission won't work with APIView
from django.http import Http404
from rest_framework import generics

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]


# To view Faculties

@permission_classes((permissions.AllowAny,)) # This decorator to be used with APIView
class FacultyList(APIView):
    """
    List all Faculties
    """

    def get(self, request, format=None):
        faculty = Faculty.objects.all()
        serializer = FacultySerializer(faculty, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,))  # This decorator to be used with APIView
class FacultyDetail(APIView):
    """
    Retrieve, Update or delete a faculty
    """

    def get_object(self,slug):
        try:
            faculty = Faculty.objects.get(slug=slug)
            return faculty
        except Faculty.DoesNotExist:
            raise Http404

    def get(self,request,slug,format=None):
        faculty = self.get_object(slug)
        serializer = FacultySerializer(faculty)
        return Response(serializer.data)


# To view Departments

class DepartmentList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


@permission_classes((permissions.AllowAny,))  # This decorator to be used with APIView
class DepartmentDetail(APIView):
    """
    Retrieve, Update or delete a faculty
    """

    def get_object(self,fac_slug,dep_slug):
        try:
            department = Department.objects.get(slug=dep_slug,faculty__slug=fac_slug)
            return department
        except Department.DoesNotExist:
            raise Http404

    def get(self,request,fac_slug,dep_slug,format=None):
        department = self.get_object(fac_slug,dep_slug)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)


# To view Univerity Events

@permission_classes((permissions.AllowAny,))  # This decorator to be used with APIView
class UniversityEventDetail(APIView):
    """
    Retrieve, Update or delete a faculty
    """

    def get_object(self,year,month,day):
        try:
            slug = f'{day}-{month}-{year}'
            event = Event.objects.filter(slug=slug)
            return event
        except Event.DoesNotExist:
            raise Http404

    def get(self,request,year,month,day,format=None):
        event = self.get_object(year,month,day)
        serializer = EventSerializer(event,many=True)
        return Response(serializer.data)


# To view Univerity Events

@permission_classes((permissions.AllowAny,))  # This decorator to be used with APIView
class FacultyEventDetail(APIView):
    """
    Retrieve, Update or delete a faculty
    """

    def get_object(self,faculty,year,month,day):
        try:
            slug = f'{day}-{month}-{year}'
            event = Event.objects.filter(slug=slug,faculty__slug=faculty)
            return event
        except Event.DoesNotExist:
            raise Http404

    def get(self,request,faculty,year,month,day,format=None):
        event = self.get_object(faculty,year,month,day)
        serializer = EventSerializer(event,many=True)
        return Response(serializer.data)


# To view Univerity Events

@permission_classes((permissions.AllowAny,))  # This decorator to be used with APIView
class ExaminationList(APIView):
    """
    Retrieve, Update or delete a faculty
    """

    def get_object(self,year,month,day):
        try:
            slug = f'{day}-{month}-{year}'
            exam = Examination.objects.filter(slug=slug)
            return exam
        except Examination.DoesNotExist:
            raise Http404

    def get(self,request,year,month,day,format=None):
        exam = self.get_object(year,month,day)
        serializer = ExaminationSerializer(exam,many=True)
        return Response(serializer.data)