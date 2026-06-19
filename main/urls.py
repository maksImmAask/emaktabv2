from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StudentViewSet,
    TeacherViewSet,
    SchoolClassViewSet,
    SubjectViewSet,
    ScheduleViewSet,
    HomeworkViewSet,
    GradeViewSet,
    AttendanceViewSet,
)

router = DefaultRouter()

router.register('students', StudentViewSet)
router.register('teachers', TeacherViewSet)
router.register('classes', SchoolClassViewSet)
router.register('subjects', SubjectViewSet)
router.register('schedules', ScheduleViewSet)
router.register('homework', HomeworkViewSet)
router.register('grades', GradeViewSet)
router.register('attendance', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]