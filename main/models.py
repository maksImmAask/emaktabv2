from django.db import models


class SchoolClass(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Student(models.Model):
    username = models.CharField(max_length=150, unique=True)
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='students'
    )

    def __str__(self):
        return self.username


class Teacher(models.Model):
    username = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.username


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ClassSubject(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.school_class} - {self.subject}"


class Schedule(models.Model):
    WEEKDAYS = (
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
    )

    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    weekday = models.IntegerField(choices=WEEKDAYS)
    lesson_number = models.IntegerField()

    class Meta:
        unique_together = ('school_class', 'weekday', 'lesson_number')

    def __str__(self):
        return f"{self.school_class} - {self.subject} ({self.lesson_number})"


class Homework(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField(upload_to='homework_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ДЗ: {self.schedule}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    value = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.value}"


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Присутствовал'),
        ('absent', 'Отсутствовал'),
        ('late', 'Опоздал'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'schedule', 'date')

    def __str__(self):
        return f"{self.student} - {self.schedule} - {self.date}"