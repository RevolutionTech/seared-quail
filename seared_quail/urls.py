"""
:Created: 5 May 2015
:Author: Lucas Connors

"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from socketio import sdjango

from menu.views import MenuView
from order.views import (
    redirect_authenticated,
    LoginView,
    logout,
    KitchenView,
    update_orders,
    complete_order,
)


sdjango.autodiscover()


urlpatterns = [
    url(r"^socket\.io", include(sdjango.urls)),
    url(r"^admin/", admin.site.urls),
    url(r"^$", csrf_exempt(MenuView.as_view()), name="menu"),
    url(r"^login/?$", redirect_authenticated(LoginView.as_view()), name="login"),
    url(r"^logout/?$", logout, name="logout"),
    url(r"^kitchen/?$", login_required(KitchenView.as_view()), name="kitchen"),
    url(r"^kitchen/update/?$", update_orders, name="update_orders"),
    url(r"^kitchen/completeorder/?$", complete_order, name="complete_order"),
]

# Add media folder to urls when DEBUG = True
if settings.DEBUG:
    urlpatterns.append(
        url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT})
    )
