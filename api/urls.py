from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet,FacultyList,FacultyDetail,DepartmentList,DepartmentDetail,UniversityEventDetail,FacultyEventDetail,ExaminationList

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('faculty/',FacultyList.as_view(),name="faculty"),
    path('faculty/<slug>/',FacultyDetail.as_view(),name="faculty-detail"),
    path('department/',DepartmentList.as_view(),name="department-list"),
    path('department/<fac_slug>/<dep_slug>/',DepartmentDetail.as_view(),name="department-detail"),
    path('calendar/<year>/<month>/<day>/',UniversityEventDetail.as_view(),name="universityevent-detail"),
    path('calendar/<faculty>/<year>/<month>/<day>/',FacultyEventDetail.as_view(),name="facultyevent-detail"),
    path('calendar/examination/all/<year>/<month>/<day>/',ExaminationList.as_view(),name="examination-list")
]