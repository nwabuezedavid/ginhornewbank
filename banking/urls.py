from django.contrib import admin
from django.urls import include
from django.urls import path
from app.views import home
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)