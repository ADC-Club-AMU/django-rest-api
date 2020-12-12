from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer
from .models import Faculty,Department,Event,Examination,EntranceExamination,Notice,Holiday
from .serializers import (FacultySerializer,DepartmentSerializer,EventSerializer,
                            ExaminationSerializer,EntranceExaminationSerializer,NoticeSerializer,HolidaySerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes # Djnago permission won't work with APIView
from django.http import Http404
from rest_framework import generics
from bs4 import BeautifulSoup
from django.http import JsonResponse

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
    Retrieve a faculty
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
    """
    Retrieve deaprtments list
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


@permission_classes((permissions.AllowAny,))  # This decorator to be used with APIView
class DepartmentDetail(APIView):
    """
    Retrieve a department
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
    Retrieve all events in university on a particular day
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
    Retrieve all events in a faculty on a particular day
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


# To view Examinations in departments

@permission_classes((permissions.AllowAny,))  # This decorator to be used with APIView
class ExaminationList(APIView):
    """
    Retrieve all examinations on a day
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


# To view Entrance Examination

@permission_classes((permissions.AllowAny,))  # This decorator to be used with APIView
class EntranceExaminationList(APIView):
    """
    Retrieve all entrance examinations in an year
    """
    def get_object(self,year):
        try:
            exam = EntranceExamination.objects.filter(year=year)
            return exam
        except EntranceExamination.DoesNotExist:
            raise Http404

    def get(self, request,year, format=None):
        exam = self.get_object(year)
        serializer = EntranceExaminationSerializer(exam, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class NoticeList(APIView):
    """
    Retrieve all notices
    """
    def get(self, request, format=None):
        notice = Notice.objects.all()
        serializer = NoticeSerializer(notice, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class HolidaysByMonthList(APIView):
    """
    Retrieve all holidays by month
    """
    def get_object(self,year,month):
        try:
            holidays = Holiday.objects.filter(year=year,month=month)
            return holidays
        except Holiday.DoesNotExist:
            raise Http404

    def get(self,request,year,month,format=None):
        holidays = self.get_object(year,month)
        serializer = HolidaySerializer(holidays,many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class HolidaysByYearList(APIView):
    """
    Retrieve all holidays by year
    """
    import json

    def get_object(self,year):
        try:
            holidays = Holiday.objects.filter(year=year)
            return holidays
        except Holiday.DoesNotExist:
            raise Http404

    def get(self,request,year,format=None):
        holidays = self.get_object(year)
        serializer = HolidaySerializer(holidays,many=True)
        return Response(serializer.data)


"""
WebScraping News
"""

def get_html_content():
    import requests
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    url = f'https://beta.amu.ac.in/news'
    html_content = requests.get(url).text
    return html_content

@permission_classes((permissions.AllowAny,))
class NewsView(APIView):
    def get(self,request,*args,**kwargs):
        import json
        import re
        html_content = get_html_content()
        soup = BeautifulSoup(html_content, 'html.parser')
        c = soup.findAll("div", {"class": "default-heading"})
        response_data = []
        base_url = "https://beta.amu.ac.in/"
        for x in c:
            match = re.search(r'\bh3\b',str(x))
            if match:
                heading = str(x).split('href="')[1].split('>')[1].split('<')[0]
                news_url = "{}{}".format(base_url,str(x).split('href="')[1].split('"')[0])
                date = str(x).split('href="')[1].split('class="date-admin">')[1].split('<')[0]
                dict_data = {"heading":heading,"news_url":news_url,"date":date}
                response_data.append(dict_data)
        return Response(response_data)


        