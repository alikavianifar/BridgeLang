"""
URL configuration for CoreFolder project (BridgeLang).

Routes all incoming requests to the appropriate app-level URL
configurations. Includes sitemap, robots.txt, password reset,
and debug toolbar (development only).

For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from AppFolder.sitemaps import StaticViewSitemap
from BlogFolder.sitemaps import BlogSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AppFolder.urls')),
    path('blog/', include('BlogFolder.urls')),
    path('Lessons/', include('LessonsFolder.urls')),
    path('Accounts/', include('AccountsFolder.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path('robots.txt', include('robots.urls')),
    path('captcha/', include('captcha.urls')),
]

# Debug toolbar — only in development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = "CoreFolder.errors.error_400"  # (Bad Request)
handler403 = "CoreFolder.errors.error_403"  # (Permission Denied)
handler404 = "CoreFolder.errors.error_404"  # (Page Not Found)
handler500 = "CoreFolder.errors.error_500"  # (Server Error)