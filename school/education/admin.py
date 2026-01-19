from django.contrib import admin

from .models import Group, Student, Subject, Classroom, Teacher, Lesson, Grade
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Classroom)
admin.site.register(Teacher)
admin.site.register(Lesson)
admin.site.register(Grade)
