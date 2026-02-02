from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Групи
class GroupListView(ListView):
    model = Group
    template_name = "education/group_list.html"


class GroupDetailView(DetailView):
    model = Group
    template_name = "education/group_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.object

        context["students"] = group.student_set.select_related("user")
        context["lessons"] = group.lesson_set.select_related(
            "subject", "teacher__user", "classroom"
        ).order_by("day", "lesson_number")

        return context


class ScheduleView(ListView):
    model = Lesson
    template_name = "education/schedule.html"

    def get(self, request, *args, **kwargs):  # ⬅️⬅️
        request.session["last_group"] = kwargs["pk"]  # ⬅️⬅️
        return super().get(request, *args, **kwargs)  # ⬅️⬅️

    def get_queryset(self):
        # return Lesson.objects.filter(
        #     group_id=self.kwargs["group_id"]
        # ).order_by("day", "lesson_number")

        group_id = self.kwargs.get("group_id") or self.request.session.get("last_group") # ⬅️⬅️
        return Lesson.objects.filter(group_id=group_id).order_by("day", "lesson_number")# ⬅️⬅️




class StudentGradesView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = "education/grades.html"

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        return Grade.objects.filter(student=student)


class GradeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Grade
    fields = ("student", "lesson", "value")
    template_name = "education/grade_form.html"

    def test_func(self):
        return hasattr(self.request.user, "teacher")

    def form_valid(self, form):
        form.instance.teacher = self.request.user.teacher
        return super().form_valid(form)