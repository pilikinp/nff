from .views import LogOut, Login, Registration
from django.urls import path

urlpatterns = [
    path('logout/', LogOut.as_view(), name='logout'),
    path('login/', Login.as_view(), name='login'),
    path('reg/', Registration.as_view(), name='registration'),
]
