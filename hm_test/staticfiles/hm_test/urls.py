from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/doctor/', include('doctor.urls')),
    path('api/assistant/', include('assistant.urls')),
    path('api/patient/', include('patient.urls')),
    path('api/treatment/', include('treatment.urls')),
    path('api/report/', include('report.urls')),
    path('api/general-manager/', include('general_manager.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
