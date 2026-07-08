from django.utils import timezone
from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import DirectorDashboardSerializer
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
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Avg

from accounts.permissions import IsStudent

from .serializers import StudentDashboardSerializer, TeacherDashboardSerializer, TeacherJournalSaveSerializer, TeacherStudentSerializer
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
    IsAdmin,
    IsTeacherOrAdmin,
    ReadOnlyOrAdmin,
    ReadOnlyTeacherOrAdmin,
)
class BaseRoleViewSet(ModelViewSet):
    permission_classes = [ReadOnlyOrAdmin]

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


class HomeworkViewSet(BaseRoleViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [ReadOnlyTeacherOrAdmin]
class ScheduleViewSet(BaseRoleViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [ReadOnlyTeacherOrAdmin]


class GradeViewSet(BaseRoleViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [ReadOnlyTeacherOrAdmin]


class AttendanceViewSet(BaseRoleViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [ReadOnlyTeacherOrAdmin]
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg

from accounts.permissions import IsStudent

from .models import (
    Grade,
    Attendance,
    Schedule,
    Homework,
)

from .serializers import StudentDashboardSerializer


class StudentDashboardAPIView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):

        student = request.user.student_profile

        grades = Grade.objects.filter(
            student=student
        ).select_related(
            "student__user",
            "schedule__subject",
            "teacher__user",
            "schedule",
        )

        attendance = Attendance.objects.filter(
            student=student
        ).select_related(
            "student__user",
            "schedule__subject",
            "schedule__teacher__user",
            "schedule__school_class",
        )

        schedule = Schedule.objects.filter(
            school_class=student.school_class
        ).select_related(
            "school_class",
            "subject",
            "teacher__user",
        )

        homework = Homework.objects.filter(
            schedule__school_class=student.school_class
        ).select_related(
            "schedule__school_class",
            "schedule__subject",
            "schedule__teacher__user",
        )

        average = (
            grades.aggregate(
                average=Avg("value")
            )["average"]
            or 0
        )

        serializer = StudentDashboardSerializer(
            {
                "student": student,
                "average_grade": round(
                    average,
                    2,
                ),
                "grades": grades,
                "attendance": attendance,
                "schedule": schedule,
                "homework": homework,
            }
        )

        return Response(serializer.data)
class TeacherDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher = request.user.teacher_profile

        today = datetime.today().isoweekday()
        # Понедельник = 1
        # Вторник = 2
        # ...
        # Воскресенье = 7

        schedule = Schedule.objects.filter(
            teacher=teacher,
            weekday=today,
        ).select_related(
            "school_class",
            "subject",
            "teacher",
        ).order_by("lesson_number")

        homework = Homework.objects.filter(
            schedule__teacher=teacher
        ).select_related(
            "schedule",
            "schedule__subject",
        ).order_by("-created_at")[:10]

        classes = SchoolClass.objects.filter(
            schedule__teacher=teacher
        ).distinct()

        subjects = Subject.objects.filter(
            schedule__teacher=teacher
        ).distinct()

        stats = {
            "classes": classes.count(),

            "students": Student.objects.filter(
                school_class__in=classes
            ).count(),

            "lessons": schedule.count(),

            "homework": homework.count(),
        }

        serializer = TeacherDashboardSerializer(
            {
                "teacher": teacher,
                "stats": stats,
                "schedule": schedule,
                "homework": homework,
                "classes": classes,
                "subjects": subjects,
            }
        )

        return Response(serializer.data)
class TeacherStudentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        teacher = request.user.teacher_profile

        schedule_id = request.GET.get("schedule")

        if not schedule_id:
            return Response([])

        students = Student.objects.filter(
            school_class_id=schedule_id
        ).select_related("user")

        data = []

        for student in students:

            grade = Grade.objects.filter(
                teacher=teacher,
                student=student,
                schedule__subject_id=schedule_id,
                schedule__school_class_id=schedule_id
            ).order_by("-date").first()

            attendance = Attendance.objects.filter(
                student=student,
                schedule__teacher=teacher,
                schedule__subject_id=schedule_id,
                schedule__school_class_id=schedule_id,
            ).order_by("-date").first()

            data.append(
                {
                    "id": student.id,
                    "username": student.user.username,
                    "grade": grade.value if grade else None,
                    "attendance": (
                        attendance.status
                        if attendance
                        else None
                    ),
                }
            )

        serializer = TeacherStudentSerializer(
            data,
            many=True,
        )

        return Response(serializer.data)
class TeacherSaveJournalAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        teacher = request.user.teacher_profile

        serializer = TeacherJournalSaveSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        schedule = Schedule.objects.get(
            id=data["schedule_id"],
            teacher=teacher,
        )

        today = timezone.now().date()

        for item in data["students"]:

            student = Student.objects.get(
                id=item["student"]
            )

            Grade.objects.update_or_create(
                student=student,
                schedule=schedule,
                date=today,
                defaults={
                    "teacher": teacher,
                    "value": item["grade"],
                },
            )

            Attendance.objects.update_or_create(
                student=student,
                schedule=schedule,
                date=today,
                defaults={
                    "status": item["attendance"]
                },
            )

        return Response(
            {
                "message": "Журнал сохранён"
            }
        )
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class DirectorDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "stats": {
                "students": Student.objects.count(),
                "teachers": Teacher.objects.count(),
                "classes": SchoolClass.objects.count(),
                "subjects": Subject.objects.count(),
            },

            "students": Student.objects.all(),

            "teachers": Teacher.objects.all(),

            "grades": Grade.objects.select_related(
                "student__user",
                "teacher__user",
                "schedule__subject",
                "schedule__school_class",
            ),
            "attendance": Attendance.objects.select_related(
                "student__user",
                "schedule__subject",
            ),

            "schedule": Schedule.objects.select_related(
                "teacher__user",
                "subject",
                "school_class",
            ),

            "homework": Homework.objects.select_related(
                "schedule__subject",
            ),

            "classes": SchoolClass.objects.all(),

            "subjects": Subject.objects.all(),
        }

        serializer = DirectorDashboardSerializer(data)

        return Response(serializer.data)