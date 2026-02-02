from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, PostImage

from django.urls import reverse_lazy


class PostListView(ListView):
    model = Post
    ordering = ["-created_at"]
    template_name = "blog/post_list.html"
    paginate_by = 5 # ⬅️⬅️


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get(self, request, *args, **kwargs): # ⬅️⬅️
        post_id = str(kwargs["pk"])
        viewed = request.session.get("viewed_posts", [])

        if post_id not in viewed:
            self.get_object().views += 1
            self.get_object().save()
            viewed.append(post_id)
            request.session["viewed_posts"] = viewed

        return super().get(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ("title", "content")
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Зберігаємо всі завантажені фото
        images = self.request.FILES.getlist("images")
        for img in images:
            PostImage.objects.create(post=self.object, image=img)

        return response


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ("text",)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs["pk"]
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs): # ⬅️⬅️
        if request.session.get("commented"):
            return HttpResponse("Ти вже залишав коментар зараз 😅")

        request.session["commented"] = True
        request.session.set_expiry(60)  # 1 хв
        return super().dispatch(request, *args, **kwargs)
