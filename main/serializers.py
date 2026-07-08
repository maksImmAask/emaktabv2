from rest_framework import serializers
from .models import (
    Student,
    Teacher,
    SchoolClass,
    Subject,
    ClassSubject,
    Schedule,
    Homework,
    Grade,
    Attendance
)
from django.contrib.auth import get_user_model

User = get_user_model()
 


class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = ['id', 'name']

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    school_class = SchoolClassSerializer(read_only=True)

    school_class_id = serializers.PrimaryKeyRelatedField(
        queryset=SchoolClass.objects.all(),
        source="school_class",
        write_only=True,
    )

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="student"),
        source="user",
        write_only=True,
    )

    class Meta:
        model = Student
        fields = [
            "id",
            "username",
            "user_id",
            "school_class",
            "school_class_id",
        ]
class TeacherSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="teacher"),
        source="user",
        write_only=True,
    )

    class Meta:
        model = Teacher
        fields = [
            "id",
            "username",
            "user_id",
        ]
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']


class ClassSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSubject
        fields = ['id', 'school_class', 'subject']

class ScheduleSerializer(serializers.ModelSerializer):
    school_class = SchoolClassSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)

    school_class_id = serializers.PrimaryKeyRelatedField(
        queryset=SchoolClass.objects.all(),
        source="school_class",
        write_only=True
    )

    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source="subject",
        write_only=True
    )

    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        source="teacher",
        write_only=True
    )

    class Meta:
        model = Schedule
        fields = [
            "id",
            "school_class",
            "subject",
            "teacher",
            "school_class_id",
            "subject_id",
            "teacher_id",
            "weekday",
            "lesson_number",
        ]
class HomeworkSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer(read_only=True)

    schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all(),
        source="schedule",
        write_only=True
    )

    class Meta:
        model = Homework
        fields = [
            "id",
            "schedule",
            "schedule_id",
            "description",
            "file",
            "created_at",
        ]

class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    schedule = ScheduleSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)

    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        source="student",
        write_only=True,
    )

    schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all(),
        source="schedule",
        write_only=True,
        allow_null=True,
        required=False,
    )

    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        source="teacher",
        write_only=True,
    )

    class Meta:
        model = Grade
        fields = [
            "id",
            "student",
            "schedule",
            "teacher",
            "student_id",
            "schedule_id",
            "teacher_id",
            "value",
            "date",
        ]
class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    schedule = ScheduleSerializer(read_only=True)

    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        source="student",
        write_only=True
    )

    schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all(),
        source="schedule",
        write_only=True
    )

    class Meta:
        model = Attendance
        fields = (
            "id",
            "student",
            "schedule",
            "student_id",
            "schedule_id",
            "date",
            "status",
        )
from rest_framework import serializers


class StudentDashboardSerializer(serializers.Serializer):
    student = StudentSerializer()
    average_grade = serializers.FloatField()
    grades = GradeSerializer(many=True)
    attendance = AttendanceSerializer(many=True)
    schedule = ScheduleSerializer(many=True)
    homework = HomeworkSerializer(many=True)
class TeacherDashboardSerializer(serializers.Serializer):
    teacher = TeacherSerializer()

    stats = serializers.DictField()

    schedule = ScheduleSerializer(many=True)

    homework = HomeworkSerializer(many=True)

    classes = SchoolClassSerializer(many=True)

    subjects = SubjectSerializer(many=True)
class TeacherStudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    grade = serializers.IntegerField(allow_null=True)
    attendance = serializers.CharField(allow_null=True)
class TeacherJournalStudentSerializer(serializers.Serializer):
    student = serializers.IntegerField()
    grade = serializers.IntegerField()
    attendance = serializers.CharField()


class TeacherJournalSaveSerializer(serializers.Serializer):
    schedule_id = serializers.IntegerField()
    students = TeacherJournalStudentSerializer(many=True)
class DirectorDashboardSerializer(serializers.Serializer):
    stats = serializers.DictField()

    students = StudentSerializer(many=True)
    teachers = TeacherSerializer(many=True)

    grades = GradeSerializer(many=True)
    attendance = AttendanceSerializer(many=True)

    schedule = ScheduleSerializer(many=True)
    homework = HomeworkSerializer(many=True)

    classes = SchoolClassSerializer(many=True)
    subjects = SubjectSerializer(many=True)