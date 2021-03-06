from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView, RedirectView
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken import views as authtokenviews

urlpatterns = [
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("", RedirectView.as_view(url='/show'), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("ohrkanal.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Cast urls
    path("api/api-token-auth/", authtokenviews.obtain_auth_token),
    path("docs/", include_docs_urls(title="API service")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # Uploads
    path("uploads/", include("filepond.urls", namespace="filepond")),
    # Cast
    path("", include("cast.urls", namespace="cast")),
    # Threadedcomments
    re_path(r"^show/comments/", include("fluent_comments.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
