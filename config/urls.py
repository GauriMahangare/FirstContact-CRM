from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

admin.site.site_header = "FirstContact admin"
admin.site.site_title = "FirstContact admin"
admin.site.site_url = "http://console.firstcontact.com/"
admin.site.index_title = "FirstContact administration"
admin.empty_value_display = "**Empty**"

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path(
        "pricing/",
        TemplateView.as_view(template_name="pages/pricing.html"),
        name="pricing",
    ),
    path(
        "contactus/",
        TemplateView.as_view(template_name="pages/ContactUs.html"),
        name="contactus",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # User management
    path("users/", include("firstcontact_crm.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path(
        "organisation/",
        include("organisation.urls", namespace="organisation"),
    ),
    path("payment/", include("payment.urls", namespace="payment")),
    path("invitations/", include("invitations.urls", namespace="invitations")),
    path("teams/", include("teams.urls", namespace="teams")),
    path("leads/", include("leads.urls", namespace="leads")),
    path("category/", include("category.urls", namespace="category")),
    path("product/", include("product.urls", namespace="product")),
    path("product-category/", include("prodCategory.urls", namespace="prodCategory")),
    path(
        "product-manufacturer/",
        include("prodManufacturer.urls", namespace="prodManufacturer"),
    ),
    path("quote/", include("quote.urls", namespace="quote")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

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

admin.autodiscover()
admin.site.enable_nav_sidebar = False
