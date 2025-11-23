from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/chats/', include('chats.urls')),  # your chats app
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout endpoints
]
