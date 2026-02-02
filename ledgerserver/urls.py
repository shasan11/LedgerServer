from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/inventory/', include('inventory.urls')),
    path('api/master/', include('master.urls')),
    path('api/pos/', include('pos.urls')),
    path('api/purchase/', include('purchase.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/accounting/', include('accounting.urls')),
    path('api/crm/', include('crm.urls')),
    path('api/hrm/', include('hrm.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
