from django.db import models
from django.urls import reverse

class Product(models.Model):

    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    discount = models.CharField(max_length=4, blank=True, verbose_name='Скидка')
    image = models.ImageField(upload_to='products/', blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

