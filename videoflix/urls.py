from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('videoflix_backend/admin/', admin.site.urls),
    path('videoflix_backend/api/authentication/', include('registration_app.api.urls')),
    path('videoflix_backend/api/login/', include('login_app.api.urls')),
    path('videoflix_backend/api/profile/', include('profile_user_app.api.urls')),
    path('videoflix_backend/api/viewer/', include('profile_viewer_app.api.urls')),
    path('videoflix_backend/api/videos/', include('content_app.api.urls')),
]

# Statische Dateien für Debug-Modus hinzufügen
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += debug_toolbar_urls()
