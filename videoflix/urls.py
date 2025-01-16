from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authentication/', include('registration_app.api.urls')),
    path('api/login/', include('login_app.api.urls')),
    path('api/profile/', include('profile_user_app.api.urls')),
    path('api/viewer/', include('profile_viewer_app.api.urls')),

] + staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
