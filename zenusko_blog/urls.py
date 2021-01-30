
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('account/', include('account.urls', namespace='account')),
    path('account/', include('django.contrib.auth.urls')),
]
