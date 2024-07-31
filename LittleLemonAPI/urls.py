from django.urls import path
from . import views

urlpatterns = [
    path('menu-items/', views.menu_items),
    path('menu-items/<int:pk>', views.SingleMenuItem),
    path('throttle-check/', views.throttle_check),
    path('throttle-check-auth/', views.throttle_check_auth),
    path('me/', views.me),
    path('groups/managers/users', views.managers)
]