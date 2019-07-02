from django.urls import path
from startpage.views import startpage

urlpatterns = [
    path('', startpage),
]
