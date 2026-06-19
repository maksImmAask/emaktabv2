from rest_framework.viewsets import ModelViewSet

from .models import (
    Student,
    Teacher,
    SchoolClass,
    Subject,
    Schedule,
    Homework,
    Grade,
    Attendance,
)

from .serializers import (
    StudentSerializer,
    TeacherSerializer,
    SchoolClassSerializer,
    SubjectSerializer,
    ScheduleSerializer,
    HomeworkSerializer,
    GradeSerializer,
    AttendanceSerializer,
)

from accounts.permissions import (
    IsAdminRole,
    IsManagerOrAdmin,
    ReadOnlyOrAdminWrite
)


class BaseRoleViewSet(ModelViewSet):
    permission_classes = [ReadOnlyOrAdminWrite]


class StudentViewSet(BaseRoleViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherViewSet(BaseRoleViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class SchoolClassViewSet(BaseRoleViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer


class SubjectViewSet(BaseRoleViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ScheduleViewSet(BaseRoleViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsManagerOrAdmin]


class HomeworkViewSet(BaseRoleViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer


class GradeViewSet(BaseRoleViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsManagerOrAdmin]


class AttendanceViewSet(BaseRoleViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsManagerOrAdmin]