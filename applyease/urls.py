"""
URL configuration for applyease project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    # Landing page
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),

    # Django admin
    path('admin/', admin.site.urls),

    # App URLs — HTML views
    path('accounts/', include('accounts.urls')),
    path('profile/', include('profiles.urls')),
    path('jobs/', include('jobs.urls')),
    path('tracker/', include('tracker.urls')),
    path('ai/', include('ai_tools.urls')),
    path('admin-dashboard/', include('dashboard.urls')),
    path('mock-forms/', include('mock_forms.urls')),

    # API URLs
    path('api/jobs/', include('jobs.api_urls')),
    path('api/applications/', include('tracker.api_urls')),
    path('api/ai/', include('ai_tools.api_urls')),
    path('api/', include('profiles.api_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
