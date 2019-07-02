from feeduser.views import UsersList
from django.urls import path

app_name = 'feeduser'

urlpatterns = [
    path('', UsersList.as_view({'get': 'list'}), name='users_list'),
]
