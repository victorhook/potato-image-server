from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('date/<str:date>', views.date, name='date'),
    path('date/<str:date>/<str:img>', views.image, name='image'),
    path('date/next_image/<str:date>/<str:img>', views.next_image, 
         name='next_image'),
    path('date/prev_image/<str:date>/<str:img>', views.prev_image, 
         name='prev_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
