"""needforfeed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from feeduser.views import UsersList, ProducersList, ConsumersList
from menu.views import MealsList, ProductsList, CategoriesList
from orders.views import OrdersList

router = DefaultRouter()

router.register('users', UsersList)
router.register('consumers', ConsumersList)
router.register('chefs', ProducersList)
router.register('meals', MealsList)
router.register('products', ProductsList)
router.register('categories', CategoriesList)
router.register('orders', OrdersList)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view(url='http://127.0.0.1:8080')),

    path('api_v1_auth/', include('auth.endpoints')),

    path('api_v1/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
