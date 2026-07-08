from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    DirectorDashboardAPIView,
    StudentViewSet,
    TeacherDashboardAPIView,
    TeacherSaveJournalAPIView,
    TeacherStudentsAPIView,
    TeacherViewSet,
    SchoolClassViewSet,
    SubjectViewSet,
    ScheduleViewSet,
    HomeworkViewSet,
    GradeViewSet,
    AttendanceViewSet,
    StudentDashboardAPIView,
)

router = DefaultRouter()

router.register("students", StudentViewSet)
router.register("teachers", TeacherViewSet)
router.register("classes", SchoolClassViewSet)
router.register("subjects", SubjectViewSet)
router.register("schedules", ScheduleViewSet)
router.register("homework", HomeworkViewSet)
router.register("grades", GradeViewSet)
router.register("attendance", AttendanceViewSet)

urlpatterns = [
    path(
        "student/dashboard/",
        StudentDashboardAPIView.as_view(),
        name="student-dashboard",
    ),path(
    "teacher/dashboard/",
    TeacherDashboardAPIView.as_view(),
    name="teacher-dashboard",
),
    path(
        "teacher/students/",
        TeacherStudentsAPIView.as_view(),
        name="teacher-students",
    ),
    path(
        "teacher/save-journal/",
        TeacherSaveJournalAPIView.as_view(),
    ),
    path(
    "director/dashboard/",
    DirectorDashboardAPIView.as_view(),
),
    path("", include(router.urls)),
]