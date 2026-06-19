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


class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = ['id', 'name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'username', 'school_class']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'username']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']


class ClassSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSubject
        fields = ['id', 'school_class', 'subject']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            'id',
            'school_class',
            'subject',
            'teacher',
            'weekday',
            'lesson_number'
        ]


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = [
            'id',
            'schedule',
            'description',
            'file',
            'created_at'
        ]


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = [
            'id',
            'student',
            'subject',
            'teacher',
            'value',
            'date'
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            'id',
            'student',
            'schedule',
            'date',
            'status'
        ]