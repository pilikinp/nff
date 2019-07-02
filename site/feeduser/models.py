from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime, date


def date_transform(date_str, format_="%Y-%m-%d"):
    '''Преобразует строку формата 2001-01-01 в объект datetime'''
    return datetime.strptime(date_str, format_).date()


def calculate_age(born, format_="%Y-%m-%d"):
    '''
    Считает возраст по дате рождения
    :param born: дата рождения, datetime или str
    :param format_: формат строки для даты (в случае если передается строковое представление)
    :return:int
    '''
    today = date.today()
    if isinstance(born, date):
        pass
    elif isinstance(born, str):
        born = date_transform(born, format_=format_)
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class FeedUser(AbstractUser):
    '''Пользователь'''
    MALE = 'M'
    FEMALE = 'F'
    GENDER = ((MALE, 'male'), (FEMALE, 'female'))

    avatar = models.ImageField(
        upload_to='images/avatars/',
        null=True,
        blank=True
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        blank=True,
        default='N',
    )

    location = models.ForeignKey(
        'location.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        blank=True,
        default=True,
        db_index=True
    )

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar else None

    @property
    def age(self):
        return calculate_age(self.birth_date) if self.birth_date else None

    @property
    def as_dict(self):
        return {
            'id': self.pk,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'location': self.location,
            'avatar': self.avatar_url
        }

    def __str__(self):
        return f'{self.username} /{self.first_name} {self.last_name}/'


class ProducerProfile(models.Model):
    '''профиль для оказателя услуг - производителя продуктов'''
    user = models.OneToOneField(
        FeedUser,
        unique=True,
        on_delete=models.CASCADE,
        null=False,
    )

    phone = models.CharField(
        max_length=12,
        null=False,
        blank=False
    )

    snippet = models.TextField(
        max_length=512,
        blank=True,
        null=True
    )

    menu = models.ManyToManyField(
        'menu.Meal'
    )

    def data(self):
        return {key: val for key, val in self.__dict__.items() if not key.startswith('_')}

    def __str__(self):
        return f'{self.user.username} /{self.user.first_name} {self.user.last_name}/'


class ConsumerProfile(models.Model):
    '''профиль для заказчика'''
    user = models.OneToOneField(
        FeedUser,
        unique=True,
        on_delete=models.CASCADE,
        null=False,
    )

    phone = models.CharField(
        max_length=12,
        null=False,
        blank=False
    )

    snippet = models.TextField(
        max_length=512,
        blank=True,
    )

    def data(self):
        return {key: val for key, val in self.__dict__.items() if not key.startswith('_')}

    def __str__(self):
        return f'{self.user.username} /{self.user.first_name} {self.user.last_name}/'
