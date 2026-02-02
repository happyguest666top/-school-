from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Classroom)
admin.site.register(Teacher)
admin.site.register(Lesson)
admin.site.register(Grade)