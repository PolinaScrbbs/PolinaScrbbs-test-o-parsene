from django.db import IntegrityError
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from rest_framework.response import Response
from rest_framework import status
import time
import re
import requests
from django.core.files.base import ContentFile

from .models import Product

def parsing_products(url, product_count):
    try:
        driver = uc.Chrome()
        
        driver.get(url)

        # Ждем, пока элементы загрузятся (примерно 10 секунд)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.iy5')))

        time.sleep(3)

        # Находим все div элементы с указанными классами
        div_elements = driver.find_elements(By.CSS_SELECTOR, '.iy5')

        created_count = 0

        # Извлекаем информацию о продуктах
        for index, div in enumerate(div_elements[:product_count]):
            name = div.find_element(By.CSS_SELECTOR, '.tsBody500Medium').text.strip()
            price = int(re.sub(r'[^\d]+', '', div.find_element(By.CSS_SELECTOR, '.c302-a1.tsHeadline500Medium.c302-c0').text.strip()))
            image_url = div.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
            discount = div.find_element(By.CSS_SELECTOR, '.tsBodyControl400Small.c302-a2.c302-a7.c302-b1').text.strip()[1:]

            try:
                # Загрузка изображения по URL
                response = requests.get(image_url)
                if response.status_code != 200:
                    raise Exception("Не удалось загрузить изображение")
                
                # Сохранение изображения в медиа-папку
                image_name = image_url.split('/')[-1]
                image_content = ContentFile(response.content)
                
                # Создание объекта Product с сохраненным изображением
                product = Product.objects.create(name=name, price=price, discount=discount)
                product.image.save(image_name, image_content)
                created = True

            except IntegrityError:
                # Обработка ошибки, если нарушается уникальное ограничение в базе данных (например, попытка создания продукта с уже существующим именем)
                print("Произошла ошибка IntegrityError: продукт с таким именем уже существует")
                continue
            
            except ValueError:
                # Обработка ошибки, если переданные значения некорректны (например, попытка передать неверный тип данных для цены)
                return Response("Произошла ошибка ValueError: некорректные значения для создания продукта", status=status.HTTP_400_BAD_REQUEST)
                
            except Exception as e:
                # Обработка других неожиданных ошибок
                return Response(f"Произошла неожиданная ошибка: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if created:
                created_count += 1
        
        return created_count

    except Exception as e:
        return Response(f"Произошла ошибка: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        driver.quit()