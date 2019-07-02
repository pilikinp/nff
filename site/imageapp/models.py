from django.db import models


# Create your models here.

class ImageMeal(models.Model):
    image = models.ImageField(
        upload_to='image/meal/',
        default='default.png'
    )
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.url

    @property
    def url(self):
        return self.image.url
