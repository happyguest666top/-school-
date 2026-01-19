from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('education/', include('education.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
