from django.urls import path
from .views import MyNotificationList, NotificationCreateView

urlpatterns = [
    path('', MyNotificationList.as_view(), name='my-notifications'),
    path('create/', NotificationCreateView.as_view(), name='notification-create'),
]