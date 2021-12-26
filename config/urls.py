from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI

from account.controllers import account_controller
from commerce.controllers import commerce_controller, order_controller

api = NinjaAPI()
api.add_router('auth', account_controller)
api.add_router('', commerce_controller)
api.add_router('order', order_controller)

urlpatterns = [
    path('api/', api.urls),
    path('admin/', admin.site.urls),
]

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
